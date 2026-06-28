from pathlib import Path
import time

from pdfvoice import PDFVoice


pdf = PDFVoice(

    Path.home() /
    "pdfvoice" /
    "TecnicasPromptFinalPDF.pdf"

)

# -------------------------

pdf.prepare()

pdf.summary()

pdf.list()

# -------------------------

print("Generando capítulo 1...")

pdf.generate(1)

# -------------------------

print("Reproduciendo...")

pdf.play(1)

time.sleep(5)

print(pdf.status())

# -------------------------

print("Pausa")

pdf.pause()

time.sleep(2)

# -------------------------

print("Continuar")

pdf.resume()

time.sleep(5)

# -------------------------

print("Velocidad 1.30x")

pdf.speed(1.30)

time.sleep(5)

# -------------------------

print("Avanzando 20 segundos")

pdf.seek(20)

time.sleep(5)

# -------------------------

print("Estado:")

print(pdf.status())

# -------------------------

pdf.stop()

pdf.close()

print("Fin de prueba.")
