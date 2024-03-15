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
$ ./python interleave -h

usage: interleave [-h] DEST PAGES FILES [FILES ...]

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

# Web API usage

This repo also includes a Flask HTTP API for hosting a server that interleaves PDFs.
See the following files to better understand the devops:

- `default.conf`: nginx reverse proxy configuration
    - serves output PDFs from a directory (docker volume)
    - serves static content from `html/`
    - routes `/api/<foo>` into the Flask app, stripping away the `/api` prefix.
- `docker-compose.yml`: describes a setup with nginx and Flask running side-by-side
    - defines env vars necessary to run the Flask app
    - sets up docker volumes so nginx and Flask both work with the same output directory
    - mounts `html/` into the nginx container
    - this is a dev workflow setup
        - the entire source tree is bind-mounted into the `jerrington/interleave-it` container
        - the entrypoint (normally the production `run` script) is overridden to use `debug`
          instead
        - upshot: editing the Python code will automatically restart the API server thanks to
          Flask's built-in debug runner, nginx will see changes immediately to HTML files due to
          the bind-mount.

To run the dev setup, it suffices to do the following:

- Build the interleave-it container: `docker build -t jerrington/interleave-it .`
- Run the docker-compose project: `docker-compose up`
- Edit static content under `html/` and the backend code under `interleave/`.
- The server runs on port 8080 (on the host), so visit `http://localhost:8080`.
- Use the bundled script `interleave-remote` to use curl to upload PDFs to test the interleaving
  API.
