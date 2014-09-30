# -- coding: utf-8 --
"""
 src/console.py
 An interactive shell for the planet_express project.

 The intended invocation is from the planet_express/ folder :
   $ ./console
   >>>          

 Jim Mahoney | mahoney@marlboro.edu | Nov 2012 | MIT License
"""

from utilities import project_path

# planet_express.py is in in the project_path folder.
import sys
sys.path.insert(0, project_path)
from planet_express import *

# Create a "context" variable
c = app.test_request_context()
c.push()

print "Welcome to planet_express."

