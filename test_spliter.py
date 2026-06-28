from core.extractor import PDFExtractor
from core.splitter import ChapterSplitter

pdf = PDFExtractor("TecnicasPromptFinalPDF.pdf")

texto = pdf.extract()

sp = ChapterSplitter(texto)

sp.load()

sp.detect()

sp.build()

sp.summary()
