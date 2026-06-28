from pdfvoice import PDFVoice

pdf = PDFVoice()

pdf.open("TecnicasPromptFinalPDF.pdf")

print()

for chapter in pdf.chapters():

    print(chapter.number, "-", chapter.title)

print()

pdf.play()

input("ENTER -> siguiente")

pdf.next()

input("ENTER -> velocidad 1.5x")

pdf.speed(1.5)

input("ENTER -> pausa")

pdf.pause()

input("ENTER -> continuar")

pdf.resume()

input("ENTER -> cerrar")

pdf.close()
