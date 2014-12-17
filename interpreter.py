class interpreter:
    """
    Base interpreter class. Must override __init__() and __next__(self) for the
    interpreter to work.

    To run in Python 2, replace the __next__(self) functions with next(self)

    Interpreters are built as generators.  Each call of next() interprets the
    next statement.  The current languages can all be interpreted token by
    token, so this works well, and allows for stepping and debugging.
    Calling run() will execute the remainder (or all) of the source code
    without printing the program state.
    """
    
    def run(self):
        self.deb = False
        for i in self:
            pass
            
    def __iter__(self):
        return self

    def debug(self):
        print(self)


#Branded exceptions 
class interpreterError(Exception):
    pass
        
        
        
        

