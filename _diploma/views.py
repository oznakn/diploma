from uuid import uuid4

import io

from unicode_tr import unicode_tr

from django.shortcuts import render
from django.http import FileResponse

from django_tex.shortcuts import compile_template_to_pdf

from PyPDF2 import PdfWriter, PdfReader

def index(request):
    return render(request, "index.html")

def create_diploma(request):
    name = request.GET.get('name', None)

    if name is None:
        name = ""

    print(name)

    name = "Sn. " + name

    stamp_pdf = compile_template_to_pdf(
        "diploma.tex", {"name": unicode_tr(name).title()}
    )

    reader = PdfReader("layer1.pdf")
    layer1_page = reader.pages[0]

    reader = PdfReader(io.BytesIO(stamp_pdf))
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

    pdf_name = f"pdftemp/{uuid4()}.pdf"

    with open(pdf_name, "wb") as fp:
        writer.write(fp)

    response = FileResponse(open(pdf_name, "rb"), content_type="application/pdf")
    response['Content-Disposition'] = 'filename="diploma.pdf"'
    return response
