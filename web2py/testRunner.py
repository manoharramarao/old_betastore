#!/usr/bin/python
"""
Runs all tests that exist in the tests directories.

The class should have a name based on the file's path, like this:
FilenameDirectory -> DefaultTasksModel

for example:
applications/app/tests/controllers/default.py
is
class DefaultController(unittest.TestCase)

BEWARE that the name is NOT in plural (controllers->Controller)

Execute with:
>   python web2py.py -S appname -M -R testRunner.py


02/03/2009
Jon Vlachoyiannis
jon@emotionull.com

"""

import unittest
import glob
import sys

suite = unittest.TestSuite()

# get all files with tests
test_files = glob.glob('applications/'+'experiment'+'/tests/*/*.py')

if not len(test_files):
    raise Exception("No files found for app: " + sys.argv[2])

# Bring all unit tests in and their controllers/models/whatever
for test_file in test_files:
    execfile(test_file, globals())

    # Create the appropriate class name based on filename and path
    # TODO: use regex
    filename =  str.capitalize(test_file.split("/")[-1][:-3])
    directory =  str.capitalize(test_file.split("/")[-2][:-1])

    suite.addTest(unittest.makeSuite(globals()[filename+directory]))

    # Load the to-be-tested file
    execfile("applications/"+'experiment'+"/"+directory.lower()+"s/"+filename.lower()+".py", globals())


db = test_db # Use the test database for all tests

unittest.TextTestRunner(verbosity=2).run(suite)