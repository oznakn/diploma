from PyPDF2 import PdfWriter, PdfReader


reader = PdfReader("layer1.pdf")
layer1_page = reader.pages[0]

reader = PdfReader("layer2.pdf")
layer2_page = reader.pages[0]

writer = PdfWriter()

reader = PdfReader("diploma.pdf")

for index in list(range(0, len(reader.pages))):
    content_page = reader.pages[index]
    mediabox = content_page.mediabox

    content_page.merge_page(layer1_page)
    content_page.merge_page(layer2_page)
    content_page.mediabox = mediabox
    writer.add_page(content_page)

with open("result.pdf", "wb") as fp:
    writer.write(fp)
