"""
mpv_player.py

Controla mpv mediante IPC (JSON).
"""

from __future__ import annotations

import json
import socket
import subprocess
import time
from pathlib import Path

import config
import utils

from .base import BasePlayer


class MPVPlayer(BasePlayer):

    def __init__(self):

        self.process = None

        self.socket_path = config.MPV_SOCKET

        self.start()

    # ----------------------------------------------------------

    def start(self):

        """
        Inicia mpv en modo idle.
        """

        if self.process is not None:

            return

        utils.info("Iniciando MPV...")

        self.process = subprocess.Popen(

            [

                config.MPV_BIN,

                "--idle=yes",

                "--no-terminal",

                f"--input-ipc-server={self.socket_path}",

            ],

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL,

        )

        # Esperar a que cree el socket

        for _ in range(30):

            if Path(self.socket_path).exists():

                utils.ok("MPV listo.")

                return

            time.sleep(0.1)

        raise RuntimeError("MPV no creó el socket IPC.")

    # ----------------------------------------------------------

    def _send(self, command):

        """
        Envía un comando JSON a mpv.
        """

        sock = socket.socket(

            socket.AF_UNIX,

            socket.SOCK_STREAM,

        )

        sock.connect(self.socket_path)

        payload = {

            "command": command

        }

        sock.sendall(

            (json.dumps(payload) + "\n").encode()

        )

        sock.recv(4096)

        sock.close()

    # ----------------------------------------------------------

    def play(self, audio):

        utils.info(f"Reproduciendo {audio}")

        self._send(

            [

                "loadfile",

                str(audio),

                "replace"

            ]

        )

    # ----------------------------------------------------------

    def pause(self):

        self._send(

            [

                "set_property",

                "pause",

                True

            ]

        )

    # ----------------------------------------------------------

    def resume(self):

        self._send(

            [

                "set_property",

                "pause",

                False

            ]

        )

    # ----------------------------------------------------------

    def stop(self):

        self._send(

            [

                "stop"

            ]

        )

    # ----------------------------------------------------------

    def speed(self, value):

        self._send(

            [

                "set_property",

                "speed",

                float(value)

            ]

        )

    # ----------------------------------------------------------

    def seek(self, seconds):

        self._send(

            [

                "seek",

                seconds,

                "relative"

            ]

        )

    # ----------------------------------------------------------

    def position(self):

        self._send(

            [

                "get_property",

                "playback-time"

            ]

        )

    # ----------------------------------------------------------

    def duration(self):

        self._send(

            [

                "get_property",

                "duration"

            ]

        )

    # ----------------------------------------------------------

    def quit(self):

        if self.process is None:

            return

        self._send(

            [

                "quit"

            ]

        )

        self.process.wait()

        self.process = None

        utils.ok("MPV cerrado.")
