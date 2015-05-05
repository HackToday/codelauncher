import argparse
from flask import Flask, render_template, request
from runcode import runcode
app = Flask(__name__)

default_c_code = """#include <stdio.h>

int main(int argc, char **argv)
{
    printf("Hello C World!!\\n");
    return 0;
}    
"""

default_py_code = """import sys
import os

if __name__ == "__main__":
    print "Hello Python World!!"
"""

default_ruby_code = """

if __FILE__ == $0
    puts "Hello Ruby World!"
end

"""
default_rows = "15"
default_cols = "60"

@app.route("/")
@app.route("/runc", methods=['POST', 'GET'])
def runc():
    if request.method == 'POST':
        code = request.form['code']
        run = runcode.RunCCode(code)
        rescompil, resrun = run.run_c_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_c_code
        resrun = 'No result!'
        rescompil = ''
    return render_template("main.html",
                           code=code,
                           target="runc",
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows, cols=default_cols)

@app.route("/py")
@app.route("/runpy", methods=['POST', 'GET'])
def runpy():
    if request.method == 'POST':
        code = request.form['code']
        run = runcode.RunPyCode(code)
        rescompil, resrun = run.run_py_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_py_code
        resrun = 'No result!'
        rescompil = "No compilation for Python"
        
    return render_template("main.html",
                           code=code,
                           target="runpy",
                           resrun=resrun,
                           rescomp=rescompil,#"No compilation for Python",
                           rows=default_rows, cols=default_cols)

@app.route("/rb")
@app.route("/runrb", methods=['POST', 'GET'])
def runrb():
    if request.method == 'POST':
        code = request.form['code']
        run = runcode.RunRubyCode(code)
        rescompil, resrun = run.run_rb_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_ruby_code
        resrun = 'No result!'
        rescompil = "No compilation for Ruby"

    return render_template("main.html",
                           code=code,
                           target="runrb",
                           resrun=resrun,
                           rescomp=rescompil,#"No compilation for Python",
                           rows=default_rows, cols=default_cols)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help='Web Server Listen Host')
    parser.add_argument('--port', default=5003, help='Web Server Running Port')
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
