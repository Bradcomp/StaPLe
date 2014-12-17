"""
StaPLe token classes.  
"""

from interpreter import interpreterError

class token:
    def __init__(self):
        self.tokType = None
        self.token = None
        self.registerOp = False
    def __add__(self, other):
        if type(self) == type(other):
            return type(self)(self.token + other.token, False)
        raise interpreterError("Tried to add incompatible types!")
    def __sub__(self, other):
        if type(self) == type(other):
            return type(self)(self.token - other.token, False)
        raise interpreterError("Tried to subtract incompatible types!")
    def __mul__(self, other):
        if type(self) == type(other):
            return type(self)(self.token * other.token, False)
        raise interpreterError("Tried to multiply incompatible types!")
    def __truediv__(self, other):
        if type(self) == type(other):
            try:
                return type(self)(self.token//other.token, False)
            except ZeroDivisionError:
                raise interpreterError("Tried to divide by zero!")
        raise interpreterError("Tried to divide incompatible types!")
    def __mod__(self, other):
        if type(self) == type(other):
            try:
                return type(self)(self.token % other.token, False)
            except ZeroDivisionError:
                raise interpreterError("Tried to modulo by zero!")
        raise interpreterError("Tried to mod incompatible types!")
    def __pow__(self, other):
        if type(self) == type(other):
            return type(self)(self.token ** other.token, False)
        raise interpreterError("Tried to pow incompatible types!")
    def __lt__(self, other):
        if type(self) == type(other):
            return boolean(self.token < other.token, False)
        raise interpreterError("Invalid comparison")
    def __le__(self, other):
        if type(self) == type(other):
            return boolean(self.token <= other.token, False)
        raise interpreterError("Invalid comparison")
    def __eq__(self, other):
        return boolean(type(self) == type(other) and
                       self.token == other.token, False)
    def __ge__(self, other):
        if type(self) == type(other):
            return boolean(self.token >= other.token, false)
        raise interpreterError("Invalid comparison")
    def __gt__(self, other):
        if type(self) == type(other):
            return boolean(self.token > other.token, False)
        raise interpreterError("Invalid comparison")
    def __ne__(self, other):
        return boolean(type(self) != type(other) or
                       self.token != other.token)
    def __bool__(self):
        return bool(self.token)
    def __repr__(self):
        return "< " +  str(self.tokType) + ": " + str(self.token) + " >"
    def __str__(self):
        return str(self.token)

class number(token):
    def __init__(self, token, registerOp):
        self.tokType = "Number"
        self.token = int(token)
        self.registerOp = registerOp
        
class string(token):
    def __init__(self, token, registerOp):
        self.tokType = "String"
        self.token = token.rstrip()
        self.registerOp = registerOp
    def __sub__(self, other):
        raise interpreterError("Tried to subtract a string!")
    def __mul__(self, other):
        raise interpreterError("Tried to multiply a string!")
    def __truediv__(self, other):
        raise interpreterError("Tried to divide a string!")
    def __mod__(self, other):
        raise interpreterError("Tried to mod a string!")
    def __pow__(self, other):
        raise interpreterError("Tried to pow a string!")

class boolean(token):
    def __init__(self, token, registerOp):
        self.tokType = "Boolean"
        if not token or token == "False":
            self.token = False
        else:
            self.token = True
        self.registerOp = registerOp
    def __add__(self, other):
        if isinstance(other, boolean):
            return boolean(self.token or other.token, False)
        else:
            return other if self.token else self
    def __sub__(self, other):
        raise interpreterError("Tried to subtract a boolean!")
    def __mul__(self, other):
        if not self.token:
            return boolean(False, False)
        return other
    def __pow__(self, other):
        if not self.token:
            return boolean(False, False)
        return other
    
class command(token):
    def __init__(self, token, registerOp):
        self.tokType = "Command"
        self.token = token.strip()
        self.registerOp = registerOp
    def __add__(self, other):
        raise interpreterError("Tried to add a command!")
    def __sub__(self, other):
        raise interpreterError("Tried to subtract a command!")
    def __mul__(self, other):
        raise interpreterError("Tried to multiply a command!")
    def __truediv__(self, other):
        raise interpreterError("Tried to divide a command!")
    def __mod__(self, other):
        raise interpreterError("Tried to mod a command!")
    def __pow__(self, other):
        raise interpreterError("Tried to pow a command!")
    def __lt__(self, other):
        raise interpreterError("Command is unorderable!")
    def __le__(self, other):
        raise interpreterError("Command is unorderable!")
    def __gt__(self, other):
        raise interpreterError("Command is unorderable!")
    def __ge__(self, other):
        raise interpreterError("Command is unorderable!")
    
    
class stack(token):
    def __init__(self, token, registerOp):
        self.tokType = "Stack"
        self.token = token
        self.registerOp = registerOp
    def pop(self):
        return self.token.pop()
    def __sub__(self, other):
        raise interpreterError("Tried to subtract a stack!")
    def __mul__(self, other):
        raise interpreterError("Tried to multiply a stack!")
    def __truediv__(self, other):
        raise interpreterError("Tried to divide a stack!")
    def __mod__(self, other):
        raise interpreterError("Tried to mod a stack!")
    def __pow__(self, other):
        raise interpreterError("Tried to pow a stack!")
    def __lt__(self, other):
        raise interpreterError("Stack is unorderable!")
    def __le__(self, other):
        raise interpreterError("Stack is unorderable!")
    def __gt__(self, other):
        raise interpreterError("Stack is unorderable!")
    def __ge__(self, other):
        raise interpreterError("Stack is unorderable!")
