from core.extractor import PDFExtractor
from core.splitter import ChapterSplitter
from core.chapter_writer import ChapterWriter

pdf = PDFExtractor("TecnicasPromptFinalPDF.pdf")

texto = pdf.extract()

sp = ChapterSplitter(texto)

sp.load()

sp.detect()

chapters = sp.build()

writer = ChapterWriter("capitulos")

writer.write(chapters)
