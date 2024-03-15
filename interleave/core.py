import pypdf

def interleave(destination, pages_per_copy, inputs):
    assert len(inputs) > 0, \
        "there is at least one input file"

    readers = [pypdf.PdfReader(p) for p in inputs]

    page_count = len(readers[0].pages)

    assert all(len(x.pages) == page_count for x in readers),\
        "all input PDFs have the same number of pages"

    writer = pypdf.PdfWriter()

    for page_index in range(0, page_count, pages_per_copy):
        pages = (page_index, page_index + pages_per_copy)
        for reader in readers:
            writer.append(fileobj=reader, pages=pages)

    writer.write(destination)
