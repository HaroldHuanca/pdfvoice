"""
mpv_player.py

Reproductor basado en MPV utilizando JSON IPC.

Características:

- Inicio diferido (lazy loading)
- Reinicio automático
- Limpieza del socket
- Comunicación mediante JSON
- API sencilla para PDFVoice
"""

from __future__ import annotations

import json
import socket
import subprocess
import time
import stat

from pathlib import Path

import config
import utils

from .base import BasePlayer
from core.logger import get_logger


class MPVPlayer(BasePlayer):
    """
    Controlador de MPV mediante JSON IPC.
    """

    STOPPED = "STOPPED"
    STARTING = "STARTING"
    READY = "READY"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"

    # ---------------------------------------------------------

    def __init__(self, socket_path: str | None = None):

        self.socket_path = (
            socket_path
            if socket_path is not None
            else config.MPV_SOCKET
        )

        self.process = None

        self.current_file = None

        self.state = self.STOPPED


    # ---------------------------------------------------------

    def _cleanup_socket(self):

        sock = Path(self.socket_path)

        try:

            if sock.exists():

                mode = sock.stat().st_mode

                if stat.S_ISSOCK(mode):

                    sock.unlink()

        except Exception:

            pass

    # ---------------------------------------------------------

    def start(self):
        """
        Inicia MPV si aún no existe.
        """

        if config.MPV_BIN is None:

            raise RuntimeError(
                "No se encontró MPV instalado."
            )

        # MPV ya está funcionando
        if self.process is not None:

            if self.process.poll() is None:

                return

        self._cleanup_socket()

        get_logger().info("Iniciando MPV...")

        self.state = self.STARTING

        self.process = subprocess.Popen(

            [

                config.MPV_BIN,

                "--idle=yes",

                "--no-terminal",

                "--force-window=no",

                f"--input-ipc-server={self.socket_path}",

            ],

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL,

        )

        socket_file = Path(self.socket_path)

        timeout = time.time() + 5

        while time.time() < timeout:

            # MPV murió antes de arrancar
            if self.process.poll() is not None:

                raise RuntimeError(
                    "MPV terminó inesperadamente."
                )

            if socket_file.exists():

                self.state = self.READY

                get_logger().ok("MPV listo.")

                return

            time.sleep(0.05)

        raise RuntimeError(
            "MPV no creó el socket IPC."
        )

    # ---------------------------------------------------------

    def _ensure_running(self):

        print("process =", self.process)

        if self.process is not None:
            print("poll =", self.process.poll())

        if self.process is None:

            print("START()")

            self.start()

            return

        if self.process.poll() is not None:

            print("RESTART()")

            self.start()

    # ---------------------------------------------------------

    def _connect(self):
        """
        Devuelve un socket conectado a MPV.

        Reintenta varias veces antes de fallar.
        """

        self._ensure_running()

        last_error = None

        for _ in range(20):

            try:

                sock = socket.socket(
                    socket.AF_UNIX,
                    socket.SOCK_STREAM,
                )

                sock.connect(self.socket_path)

                return sock

            except (
                ConnectionRefusedError,
                FileNotFoundError,
                OSError,
            ) as e:

                last_error = e

                time.sleep(0.10)

        raise RuntimeError(
            f"No fue posible conectar con MPV: {last_error}"
        )


    # ---------------------------------------------------------

    def _send(self, payload: dict):
        """
        Envía un comando JSON a MPV y devuelve la respuesta.

        Parameters
        ----------
        payload:
            Diccionario JSON compatible con el protocolo IPC de MPV.

        Returns
        -------
        dict | None
            Respuesta de MPV.
        """

        sock = self._connect()

        try:

            message = json.dumps(payload) + "\n"

            sock.sendall(message.encode("utf-8"))

            data = b""

            while not data.endswith(b"\n"):

                chunk = sock.recv(4096)

                if not chunk:
                    break

                data += chunk

            if not data:

                return None
            try:

                return json.loads(data.decode("utf-8"))

            except json.JSONDecodeError:

                return None

        finally:

            sock.close()

    # ---------------------------------------------------------

    def _command(self, *args):
        """
        Envía un comando a MPV.

        Ejemplo:

            _command("stop")

            _command("loadfile", "audio.wav", "replace")
        """

        response = self._send(

            {

                "command": list(args)

            }

        )

        if response is None:

            raise RuntimeError(
                "MPV no devolvió respuesta."
            )

        if response.get("error") != "success":

            raise RuntimeError(

                f"MPV respondió: {response}"

            )

        return response

    # ---------------------------------------------------------

    def _get_property(self, name):
        """
        Obtiene una propiedad de MPV.

        Ejemplo:

            playback-time

            duration

            pause

            volume
        """

        response = self._send(

            {

                "command": [

                    "get_property",

                    name

                ]

            }

        )

        if response is None:

            return None

        if response.get("error") != "success":

            return None

        return response.get("data")

    # ---------------------------------------------------------

    def _set_property(self, name, value):
        """
        Cambia una propiedad de MPV.

        Ejemplo:

            speed

            volume

            pause
        """

        return self._command(

            "set_property",

            name,

            value,

        )

    # ---------------------------------------------------------

    def is_running(self):
        """
        Indica si MPV sigue vivo.
        """

        return (

            self.process is not None

            and

            self.process.poll() is None

        )

    # ---------------------------------------------------------

    def status(self):
        """
        Devuelve el estado REAL de MPV.
        """

        running = self.is_running()

        if not running:

            state = self.STOPPED

        else:

            idle = self._get_property("idle-active")

            paused = self._get_property("pause")

            if idle:

                state = self.READY

            elif paused:

                state = self.PAUSED

            else:

                state = self.PLAYING

        self.state = state

        return {

            "state": state,

            "running": running,

            "current": self.current_file,

            "position": self._get_property("playback-time"),

            "duration": self._get_property("duration"),

            "paused": self._get_property("pause"),

            "speed": self._get_property("speed"),

            "volume": self._get_property("volume"),

        }

    # ---------------------------------------------------------

    def play(self, audio):
        """
        Reproduce un archivo de audio.
        """

        audio = str(audio)

        get_logger().info(f"Reproduciendo:\n{audio}")

        self._command(

            "loadfile",

            audio,

            "replace",

        )

        self.current_file = audio

        time.sleep(0.05)

        self.state = self.PLAYING

    # ---------------------------------------------------------

    def pause(self):
        """
        Pausa la reproducción.
        """

        self._set_property(

            "pause",

            True,

        )

        self.state = self.PAUSED

    # ---------------------------------------------------------

    def resume(self):
        """
        Reanuda la reproducción.
        """

        self._set_property(

            "pause",

            False,

        )

        self.state = self.PLAYING

    # ---------------------------------------------------------

    def stop(self):
        """
        Detiene el audio actual.
        """

        self._command("stop")

        self.current_file = None

        self.state = self.READY

    # ---------------------------------------------------------

    def seek(self, seconds):
        """
        Desplaza la reproducción.

        seconds > 0  -> adelante

        seconds < 0  -> atrás
        """

        self._command(

            "seek",

            float(seconds),

            "relative",

        )

    # ---------------------------------------------------------

    def seek_absolute(self, second):
        """
        Ir a un segundo específico.
        """

        self._command(

            "seek",

            float(second),

            "absolute",

        )

    # ---------------------------------------------------------

    def restart(self):
        """
        Reinicia el audio desde el inicio.
        """

        self.seek_absolute(0)

    # ---------------------------------------------------------

    def speed(self, value):
        """
        Cambia la velocidad.
        """

        self._set_property(

            "speed",

            float(value),

        )

    # ---------------------------------------------------------

    def volume(self, value):
        """
        Cambia el volumen.
        """

        value = max(

            0,

            min(

                100,

                int(value),

            ),

        )

        self._set_property(

            "volume",

            value,

        )

    # ---------------------------------------------------------

    def mute(self):

        self._set_property(

            "mute",

            True,

        )

    # ---------------------------------------------------------

    def unmute(self):

        self._set_property(

            "mute",

            False,

        )

    # ---------------------------------------------------------

    def toggle_pause(self):
        """
        Alterna pausa/reproducción.
        """

        paused = self._get_property(

            "pause"

        )

        self._set_property(

            "pause",

            not paused,

        )

        if paused:

            self.state = self.PLAYING

        else:

            self.state = self.PAUSED

    # ---------------------------------------------------------

    def position(self):
        """
        Devuelve el segundo actual.
        """

        value = self._get_property("playback-time")

        if value is None:

            return 0.0

        return float(value)

    # ---------------------------------------------------------

    def duration(self):
        """
        Devuelve la duración total.
        """

        value = self._get_property("duration")

        if value is None:

            return 0.0

        return float(value)

    # ---------------------------------------------------------

    def remaining(self):
        """
        Tiempo restante.
        """

        pos = self.position()

        dur = self.duration()

        if pos is None or dur is None:

            return None

        return dur - pos

    # ---------------------------------------------------------

    def finished(self):
        """
        Indica si terminó el audio.
        """

        pos = self.position()

        dur = self.duration()

        if pos is None:

            return False

        if dur is None:

            return False

        idle = self._get_property("idle-active")

        if idle:

            return True

        return pos >= (dur - 0.5)

    # ---------------------------------------------------------

    def wait_until_finished(self, interval=0.25):
        """
        Espera hasta que el audio termine.
        """

        while True:

            if not self.is_running():

                break

            status = self.status()

            if status["state"] == self.READY:

                break

            time.sleep(interval)

    # ---------------------------------------------------------

    def quit(self):
        """
        Cierra MPV correctamente.
        """

        if self.process is None:

            return

        try:

            if self.process.poll() is None:

                self._command("quit")

                self.process.wait(timeout=5)

        except Exception:

            try:

                self.process.kill()

            except Exception:

                pass

        self.process = None

        self.current_file = None

        self.state = self.STOPPED

        self._cleanup_socket()

        get_logger().ok("MPV cerrado.")

    # ---------------------------------------------------------

    def restart_player(self):
        """
        Reinicia completamente MPV.
        """

        self.quit()

        self.start()

    # ---------------------------------------------------------

    def __del__(self):

        try:

            self.quit()

        except Exception:

            pass


    def is_playing(self):

        return self.status()["state"] == self.PLAYING

    def is_paused(self):

        return self.status()["state"] == self.PAUSED

    def is_ready(self):

        return self.status()["state"] == self.READY

