StaPLe
======

Stack Processing Language
See StaPLe.py and http://esolangs.org/wiki/StaPLe for full documentation.

Built for Python 3, minor changes to StaPLe.py will allow it to run on Python 2(I think):
  1. Change ____next____(self) to next(self)
  2. Add from ____future____ import print_function to the top of the file.
I haven't tried this yet so I will update once I do.

To use the interpreter, you can run StaPLE in IDLE or import it into the python command line.  The interpret(string) command can be used to interpret a StaPLe string.  The class has a parseFile(filename) method that can be used as well.

At a future point, I will update so it can be called straight from the command line.
