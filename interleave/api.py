import os
import sys
import hashlib

from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    jsonify,
    send_from_directory,
)
from werkzeug.utils import secure_filename

from .core import interleave

app = Flask(__name__)

def die(*args):
    app.logger.critical(*args)
    sys.exit(1)

app.config['UPLOAD_DIR'] = os.environ.get('UPLOAD_DIR') \
    or die('missing environment variable UPLOAD_DIR')
app.config['OUTPUT_DIR'] = os.environ.get('OUTPUT_DIR') \
    or die('missing environment variable OUTPUT_DIR')
app.config['MAX_CONTENT_LENGTH'] = os.environ.get('MAX_CONTENT_LENGTH') \
    or 32 * 1024 * 1024 # MiB expressed as bytes
app.config['OUTPUT_BASE_URL'] = os.environ.get('OUTPUT_BASE_URL') \
    or None

@app.route('/interleave/<path:filename>')
def interleave_output(filename, methods=['GET']):
    return send_from_directory(app.config['OUTPUT_DIR'], filename)

@app.route('/interleave', methods=['POST'])
def interleave_route():
    ### GET AND VALIDATE INPUTS ###

    pages_per_copy = request.form.get('pages_per_copy')
    if not pages_per_copy:
        return jsonify({
            'message': 'missing requires query string parameter `pages_per_copy`',
        }), 400

    try:
        pages_per_copy = int(pages_per_copy)
    except:
        return jsonify({
            'message': 'pages_per_copy failed must parse as an integer',
        }), 400

    if 'files[]' not in request.files:
        return jsonify({
            'message': 'missing `files` argument'
        }), 400
    files = request.files.getlist('files[]')

    output_filename = request.form.get('output_name') or ''
    output_filename = secure_filename(output_filename).removesuffix('.pdf')

    ### DO THE THING ###

    md5_hash = hashlib.md5()
    # ^ calculate a hash of the filenames to serve as an output filename
    saved_filepaths = []
    # ^ the safe filepaths we compute
    for file in files:
        safe_filename = secure_filename(file.filename)
        filepath = os.path.join(
            app.config['UPLOAD_DIR'],
            safe_filename,
        )
        app.logger.info('saving ' + filepath)
        file.save(filepath)
        saved_filepaths.append(filepath)
        md5_hash.update(safe_filename.encode('utf-8'))

    output_filename += md5_hash.hexdigest()[:8] + '.pdf'

    interleave(
        os.path.join(app.config['OUTPUT_DIR'], output_filename),
        pages_per_copy,
        saved_filepaths,
    )

    result_url = \
        app.config['OUTPUT_BASE_URL'] + output_filename \
        if app.config['OUTPUT_BASE_URL'] else \
        url_for(
            'interleave_output',
            _external=True,
            filename=output_filename,
        )

    accept_header = request.headers.get('Accept');
    if 'application/json' in accept_header:
        return jsonify({ 'result': result_url });
    else:
        return redirect(result_url)

if __name__ == '__main__':
    from os import environ
    host, port = environ['BIND'].split(':')
    app.run(host=host, port=port, debug=True)
