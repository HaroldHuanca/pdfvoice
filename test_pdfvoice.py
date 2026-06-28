from pathlib import Path
import time

from pdfvoice import PDFVoice

pdf = PDFVoice(
    Path.home() /
    "Descargas" /
    "tesis.pdf"
)

pdf.prepare()

print()

pdf.list()

print()

pdf.play(1)

time.sleep(5)

pdf.pause()

time.sleep(2)

pdf.resume()

time.sleep(5)

print(pdf.status())

pdf.close()
