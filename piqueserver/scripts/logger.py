#!/usr/bin/env python3

import inspect

def log(id):
    frame = inspect.stack()[1].frame
    filename = frame.f_code.co_filename
    lineno = frame.f_code.co_firstlineno
    fnname = frame.f_code.co_name
    
    with open("{}.branchcover.txt".format(filename), "a+") as fd:
        fd.write("{{\"filename\"=\"{}\", \"lineno\"=\"{}\", \"fnname\"=\"{}\", \"branch\"=\"{}\"}}\n".format(filename, lineno, fnname, id))
