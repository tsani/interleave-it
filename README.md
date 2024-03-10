# interleave-it

This solves a very specific problem that I have. Maybe it solves yours too.

## The problem

I teach a large class and administer tests in class. Students are sitting shoulder-to-shoulder, so
to mitigate looking over the neighbour's shoulder, multiple exam versions are created.
Suppose two are created, called A and B.

I also use Crowdmark, whose support for multiple exam version is lacking: for each exam version,
one creates separate assessments in Crowdmark. Crowdmark then generates the unique exam booklet
files per version. We thus have, for example, `A.pdf` and `B.pdf` with (say) 1000 pages each,
assuming 200 students with 10 pages per exam copy.

If we send these to the printer as-is, we get a stack of exams for version A and a stack of exams
for version B. These must then be interleaved manually during distribution so adjacent students get
different copies. Booooooo.

Interleave-it does the interleaving digitially. Supply as many PDFs as you like and it will combine
them into a single PDF, with the copies interleaved.

Restrictions:

- Each PDF file must have exactly the same number of pages.
- The number of pages per copy must be the same across exam versions.

# Command-line usage

```bash
$ ./python -m venv .
$ pip install -r requirements.txt
$ source bin/activate
$ ./python interleave.py -h

usage: interleave.py [-h] DEST PAGES FILES [FILES ...]

Combines multiple (crowdmark) PDFs into a single one, interleaving the copies.
Each input PDF file must have the same number of copies, and each exam copy
must have the same number of pages, across versions.

positional arguments:
  DEST        The destination file (will be overwritten)
  PAGES       The number of pages per individual booket.
  FILES       The PDF files to interleave

options:
  -h, --help  show this help message and exit

$ python interleave.py combined-versions.pdf 10 version1.pdf version2.pdf
```
