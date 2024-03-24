import argparse

from .core import interleave

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

