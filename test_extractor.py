from core.extractor import PDFExtractor

import utils

utils.ensure_directories()

utils.check_dependencies()

pdf = PDFExtractor("LineasInvestigacion.pdf")

texto = pdf.extract()

print()

print(texto)

print()

pdf.preview()
