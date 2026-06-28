"""
controller.py

Controlador de alto nivel para PDFVoice.
"""

from __future__ import annotations

from pdfvoice import PDFVoice


class PDFController:

    def __init__(self, pdf):

        self.pdf = PDFVoice(pdf)

        self.pdf.prepare()

    # -------------------------------------------------

    def list(self):

        self.pdf.list()

    # -------------------------------------------------

    def play(self, number=None):

        if number is None:

            number = self.pdf.project.current_chapter + 1

        self.pdf.play(number)

    # -------------------------------------------------

    def pause(self):

        self.pdf.pause()

    # -------------------------------------------------

    def resume(self):

        self.pdf.resume()

    # -------------------------------------------------

    def stop(self):

        self.pdf.stop()

    # -------------------------------------------------

    def next(self):

        self.pdf.next()

    # -------------------------------------------------

    def previous(self):

        self.pdf.previous()

    # -------------------------------------------------

    def speed(self, value):

        self.pdf.speed(float(value))

    # -------------------------------------------------

    def volume(self, value):

        self.pdf.volume(int(value))

    # -------------------------------------------------

    def seek(self, seconds):

        self.pdf.seek(float(seconds))

    # -------------------------------------------------

    def generate(self, chapter):

        self.pdf.generate(chapter)

    # -------------------------------------------------

    def generate_all(self):

        self.pdf.generate_all()

    # -------------------------------------------------

    def status(self):

        s = self.pdf.status()

        print()

        print("=" * 50)

        for k, v in s.items():

            print(f"{k:12}: {v}")

        print("=" * 50)

    # -------------------------------------------------

    def close(self):

        self.pdf.close()
