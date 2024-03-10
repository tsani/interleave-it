import pypdf
import argparse

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

def main():
    parser = argparse.ArgumentParser(
        description="Combines multiple (crowdmark) PDFs into a single one, "
            "interleaving the copies. Each input PDF file must have the same "
            "number of copies, and each exam copy must have the same number "
            "of pages, across versions.",
    )
    parser.add_argument(
        "DEST",
        help="The destination file (will be overwritten)",
    )
    parser.add_argument(
        "PAGES",
        type=int,
        help="The number of pages per individual booket.",
    )
    parser.add_argument(
        "FILES",
        nargs='+',
        help="The PDF files to interleave",
    )
    args = parser.parse_args()

    interleave(args.DEST, args.PAGES, args.FILES)

if __name__ == '__main__':
    main()
