#!/usr/bin/env python3

import sys
import inspect
import json

def log(id, passthru=None):
    frame = inspect.stack()[1].frame
    filename = frame.f_code.co_filename
    lineno = frame.f_code.co_firstlineno
    fnname = frame.f_code.co_name
    
    with open("{}.branchcover.txt".format(filename), "a+") as fd:
        fd.write("{{\"filename\"=\"{}\", \"lineno\"=\"{}\", \"fnname\"=\"{}\", \"branch\"=\"{}\"}}\n".format(filename, lineno, fnname, id))
    
    return passthru

def count(filename, fnname):
    branches = set()
    
    with open("{}.branchcover.txt".format(filename), "r") as fd:
        for line in fd.readlines(): 
            dictobj = json.loads(line.strip().replace("=", ":"))
            if dictobj['fnname'] == fnname:
                branches.add(dictobj['branch'])
    
    return len(branches), sorted(branches)

if __name__ == '__main__':
    print(count(sys.argv[1], sys.argv[2]))
