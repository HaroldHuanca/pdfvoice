"""
app.py

Aplicación TUI principal de PDFVoice.
"""

from __future__ import annotations

from pathlib import Path

from controller import Controller

from tui.screen import Screen
from tui.layout import Layout

from tui.header import Header
from tui.chapterlist import ChapterList
from tui.statusbar import StatusBar
from tui.helpbar import HelpBar

from tui.input import InputHandler


class App:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self, pdf):

        self.pdf = Path(pdf)

        # -------------------------
        # Backend
        # -------------------------

        self.controller = Controller(self.pdf)

        # -------------------------
        # Pantalla
        # -------------------------

        self.screen = Screen()

        self.layout = Layout()

        # -------------------------
        # Widgets
        # -------------------------

        self.header = Header()

        self.chapterlist = ChapterList()

        self.status = StatusBar()

        self.helpbar = HelpBar()

        # -------------------------
        # Entrada
        # -------------------------

        self.input = InputHandler()

        # -------------------------

        self.running = True

    # ==========================================================
    # Preparar proyecto
    # ==========================================================

    def load(self):

        self.controller.prepare()

        project = self.controller.project

        # Header

        self.header.update(

            project.pdf_file.name,

            project.chapter_count,

        )

        # Lista

        self.chapterlist.set_chapters(

            project.chapters

        )

        # Estado inicial

        self.refresh_status()

    # ==========================================================
    # Refrescar información
    # ==========================================================

    def refresh_status(self):

        try:

            status = self.controller.status()

        except Exception:

            status = {

                "state": "STOPPED",

                "position": 0,

                "duration": 0,

                "speed": 1.0,

            }

        self.status.update(

            status["state"],

            status["position"],

            status["duration"],

            status["speed"],

        )

    # ==========================================================
    # Redibujar pantalla
    # ==========================================================

    def draw(self):

        rows, cols = self.screen.size()

        self.layout.update(

            rows,

            cols,

        )

        self.screen.clear()

        # ------------------------------------

        self.header.draw(

            self.screen,

            self.layout.header,

        )

        # ------------------------------------

        self.chapterlist.draw(

            self.screen,

            self.layout.content,

        )

        # ------------------------------------

        self.status.draw(

            self.screen,

            self.layout.status,

        )

        # ------------------------------------

        self.helpbar.draw(

            self.screen,

            self.layout.help,

        )

        # ------------------------------------

        self.screen.refresh()

    # ==========================================================
    # Actualización general
    # ==========================================================

    def update(self):

        self.refresh_status()

        self.draw()



    # ==========================================================
    # Reproducción
    # ==========================================================

    def play_selected(self):
        """
        Reproduce el capítulo seleccionado.
        """

        number = self.chapterlist.selected + 1

        self.controller.goto(number)

        self.controller.play()

    # ----------------------------------------------------------

    def pause_resume(self):
        """
        Alterna entre pausa y reproducción.
        """

        state = self.controller.state

        if state == "PLAYING":

            self.controller.pause()

        elif state == "PAUSED":

            self.controller.resume()

    # ----------------------------------------------------------

    def stop(self):

        self.controller.stop()

    # ==========================================================
    # Navegación
    # ==========================================================

    def move_up(self):

        self.chapterlist.move_up()

        self.controller.goto(

            self.chapterlist.selected + 1

        )

    # ----------------------------------------------------------

    def move_down(self):

        self.chapterlist.move_down()

        self.controller.goto(

            self.chapterlist.selected + 1

        )

    # ----------------------------------------------------------

    def next(self):

        self.controller.next()

        self.chapterlist.selected = (

            self.controller.current_chapter() - 1

        )

    # ----------------------------------------------------------

    def previous(self):

        self.controller.previous()

        self.chapterlist.selected = (

            self.controller.current_chapter() - 1

        )


    # ==========================================================
    # Velocidad
    # ==========================================================

    def speed_up(self):

        value = self.controller.speed_value

        value += 0.10

        if value > 3.0:

            value = 3.0

        self.controller.speed(value)

    # ----------------------------------------------------------

    def speed_down(self):

        value = self.controller.speed_value

        value -= 0.10

        if value < 0.50:

            value = 0.50

        self.controller.speed(value)


    # ==========================================================
    # Seek
    # ==========================================================

    def seek_forward(self):

        self.controller.app.player.seek(15)

    # ----------------------------------------------------------

    def seek_backward(self):

        self.controller.app.player.seek(-15)


    # ==========================================================
    # Salida
    # ==========================================================

    def quit(self):

        self.running = False

        self.controller.close()


    # ==========================================================
    # Entrada
    # ==========================================================

    def handle_input(self, key):

        action = self.input.read(key)

        if action == self.input.MOVE_UP:

            self.move_up()

        elif action == self.input.MOVE_DOWN:

            self.move_down()

        elif action == self.input.PLAY:

            self.play_selected()

        elif action == self.input.PAUSE:

            self.pause_resume()

        elif action == self.input.NEXT:

            self.next()

        elif action == self.input.PREVIOUS:

            self.previous()

        elif action == self.input.SPEED_UP:

            self.speed_up()

        elif action == self.input.SPEED_DOWN:

            self.speed_down()

        elif action == self.input.SEEK_FORWARD:

            self.seek_forward()

        elif action == self.input.SEEK_BACKWARD:

            self.seek_backward()

        elif action == self.input.QUIT:

            self.quit()

    # ==========================================================
    # Inicialización
    # ==========================================================

    def start(self):
        """
        Inicializa la interfaz.
        """

        self.screen.start()

        self.load()

        self.update()

    # ==========================================================
    # Finalización
    # ==========================================================

    def close(self):
        """
        Cierra la aplicación limpiamente.
        """

        try:

            self.controller.close()

        except Exception:

            pass

        self.screen.stop()



    # ==========================================================
    # Bucle principal
    # ==========================================================

    def run(self):
        """
        Ejecuta la aplicación.
        """

        try:

            self.start()

            #
            # Queremos refrescar la pantalla varias veces
            # por segundo aunque el usuario no pulse teclas.
            #

            self.screen.window.timeout(150)

            while self.running:

                #
                # Actualizar widgets
                #

                self.update()

                #
                # Leer teclado
                #

                key = self.screen.key()

                #
                # Si timeout() expiró
                #

                if key == -1:
                    continue

                #
                # Procesar acción
                #

                self.handle_input(key)

        finally:

            self.close()
