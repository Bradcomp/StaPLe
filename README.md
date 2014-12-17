StaPLe
======

Stack Processing Language
See StaPLe.py and http://esolangs.org/wiki/StaPLe for full documentation.

Built for Python 3, minor changes to StaPLe.py will allow it to run on Python 2:

Add the following code at the top of the file
```python
from __future__ import print_function
```
Change the signature of the next method from 
```python
def __next__(self):
```
to 
```python 
def next(self):
```

To use the interpreter, you can run StaPLE in IDLE or import it into the python command line.  The interpret(string) command can be used to interpret a StaPLe string.  The class has a parseFile(filename) method that can be used to porcess  code from a source file.

At a future point, I will update so it can be called straight from the command line.
