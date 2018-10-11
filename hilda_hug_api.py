#!/usr/bin/env python3
import os
import sys
import tempfile

from falcon import HTTP_500
import hug
import sh

PARSER_PATH = '/opt/hilda'
PARSER_EXECUTABLE = 'hilda.sh'
OUTPUT_SUFFIX = 'hilda'

# TODO: hilda-docker: add sentence-splitter as preprocessing
# TODO: hug template: use temp files for input and output
# TODO: hug template: allow file upload in POST body, e.g. curl -XPOST foo.com/parse < input.txt > output.parsed

@hug.response_middleware()
def process_data(request, response, resource):
    """This is a middleware function that gets called for every request a hug API processes.
    It will allow Javascript clients on other hosts / ports to access the API (CORS request).
    """
    response.set_header('Access-Control-Allow-Origin', '*')


@hug.post('/parse', output=hug.output_format.file)
def call_parser(body, response):
    parser = sh.Command(os.path.join(PARSER_PATH, PARSER_EXECUTABLE))

    if 'input' in body:
        input_file_content = body['input']
        with tempfile.NamedTemporaryFile() as input_file:
            input_file.write(input_file_content)
            input_file.flush()
            try:
                parser_stdout = parser(input_file.name, _cwd=PARSER_PATH)
                #~ import pudb; pudb.set_trace()
                output_filepath = "{0}.{1}".format(input_file.name, OUTPUT_SUFFIX)
                return output_filepath

            except sh.ErrorReturnCode_1 as err:
                response.status = HTTP_500
                trace = str(err.stderr, 'utf-8')
                error_msg = "{0}\n\n{1}".format(err, trace).encode('utf-8')

                with tempfile.NamedTemporaryFile() as error_file:
                    error_file.write(error_msg)
                    error_file.flush()
                    return error_file.name

    else:
        return {'body': body}
