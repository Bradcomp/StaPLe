"""
StaPLe - The stack processing language
An esoteric stacked based programming language.
Everything is a stack.  Everything is data.  Everything is code.

There are two stacks, the code stack and the data stack, along with a single
register.

The stacks are untyped, the two stacks and the register can all store 
any type of data.  It would even be possible to use the register as an
additional stack if you so desired.

Stack values are terminated with a semicolon - even if you are inside a user
defined stack.

There are no named variables, only the register
There are no named functions, only []

You can push and pop to either stack, depending on what stack is currently
selected.  The flip command changes the current stack. The current stack is
initialized to the data stack, which is not the code stack. 

The code stack is populated by the source code, with the last commands in the
code being the first to be executed. REMEMBER THE ORDER - Right to Left.

Code execution begins by popping the code stack, then executing the command that
was popped.  If the item popped is not a command, it will be pushed on to the
currently active stack.

Beware the infinite loop! - 1; flip; would run forever.

Execution ends when the code stack is empty.

The warp command swaps the code stack and the data stack. Warping does not
change the current stack.

New stacks can be created with square brackets [].  You can push to and pop
from created stacks using <- and ->.  Subroutines can be executed by
constructing a stack and then calling eval, which unwraps the new stack and
pushes it onto the code stack.

You can prepend a command with R to access the register instead of the
current stack.In the case of multi - parameter functions, the FIRST value
popped will be from the register.

Prepending a word with " will set it off as a string.  Strings continue until
the next semicolon.

There is no escape.

I should probably talk about truthy and falsey. It works how you probably expect
it to.

Unless noted, assume the operations operate on the current stack.
Types 
    Number (Integer only for now)
    String 
    Boolean - True, False
    Command
    Stack (Composite type)
    
Main Stack Operations
    push - from register
    pop - to register
    swap - 
    dup
    rot - swap the top of the two stacks
    flip
    warp
    drain - empty the current stack
    
Arithmetic Operations 
    + - * / % ^

Boolean Operations
    < > <= >= == ! && ||

Stack Definition Opertions
    [] - Create an empty stack
    <- - push to stack
    -> - pop from stack
    eval - Drain the stack onto the code stack
    unwrap - if the top of the current stack is a stack,
             pop and add the contents to the current stack

Flow Control
    if - Pop two values from current stack.If the value is truthy, eval the
         command, otherwise drop it.  
    ife - Pop three values from current stack.  Eval the second if the first
          is truthy, third if falsy.
    If an if statement gets a stack as its first parameter, something will
    happen that results in the stack being evaluated and the result being
    used to determine which code to run.  I think we can push the optional
    else block, then the if block, then the if or ife command onto the current
    stack, then puch a swap onto the command stack, then eval the parameter.
    Assuming the programmer set things up right, the results from the parameter
    will end up on top of the current stack, get swapped with the if / ife
    command, and evaluated as expected.  It would definitely be possible to
    modify the stack in the course of evaluating the parameter.
    
IO
    get getc put putc
"""

import copy
from interpreter import *
from tokens import *


class staple(interpreter):
    language = "staple"
    def __init__(self):
        self.commands = {'push'  : self.pushFromReg,
                         'pop'   : self.popToReg,
                         'swap'  : self.swap,
                         'dup'   : self.dup,
                         'drop'  : self.drop,
                         'rot'   : self.rot,
                         'flip'  : self.flip,
                         'warp'  : self.warp,
                         'drain' : self.drain,
                         '+'     : self.add,
                         '-'     : self.subtract,
                         '*'     : self.multiply,
                         '/'     : self.divide,
                         '%'     : self.modulo,
                         '^'     : self.exp,
                         '>'     : self.gt,
                         '<'     : self.lt,
                         '>='    : self.gte,
                         '<='    : self.lte,
                         '=='    : self.eq,
                         '!'     : self.logicalNot,
                         '&&'    : self.andAnd,
                         '||'    : self.orOr,
                         '<-'    : self.pushToToken,
                         '->'    : self.popFromToken,
                         'eval'  : self.evl,
                         'unwrap': self.unwrap,
                         'if'    : self.iff,
                         'ife'   : self.ife,
                         'get'   : self.get,
                         'getc'  : self.getc,
                         'put'   : self.put,
                         'putc'  : self.putc,
                        }
        self.stackOne = []
        self.stackTwo = []
        self.register = None
        self.codeStack = self.stackOne
        self.currentStack = self.stackTwo

    #Execution functions and helpers
    def __next__(self):
        while True:
            try:
                cmd = self.codeStack.pop()
            except IndexError:
                raise StopIteration
            if isinstance(cmd, token):
                self.execute(cmd)
            else:
                print(self.codeStack)
                print(self.currentStack)
                print(self.register)
            return
        
    def execute(self, cmd):
        if isinstance(cmd, command):
            self.commands[cmd.token](cmd)
        elif cmd.registerOp:
            self.register = cmd
        else:
            self.currentStack.append(cmd)
        
    def getOne(self, registerOp):
        if registerOp:
            a, self.register = self.register, None
        else:
            try:
                a = self.currentStack.pop()
            except:
                raise interpreterError("Pop from an empty stack!")
        return a
    
    def getTwo(self, registerOp):
        if registerOp:
            a, self.register = self.register, None
        else:
            try:
                a = self.currentStack.pop()
            except:
                raise interpreterError("Pop from an empty stack!")
        try:
            b = self.currentStack.pop()
        except:
            raise interpreterError("Pop from an empty stack!")
        return a, b

    def checkForStack(self, cmd, a, b):
        if isinstance(a, stack) or isinstance(b, stack):
            self.codeStack.append(cmd)
            self.eval(a)
            self.eval(b)
            return False
        return True

    def apstend(self, stak, tok):
        if isinstance(tok, stack):
            stak.extend(tok.token)
        else:
            stak.append(token)
        
    def __str__(self):
        return "tbd"
    
    #Parsing functions
    def parseFile(self, filename):
        codeGen = (tokStr.lstrip() for tokStr in open(filename, 'r').read().split(";"))
        self.parseList(codeGen, self.codeStack)

    def parseList(self, gen, stak):
        for tokStr in gen:
            token = self.getToken(tokStr, gen)
            if token is not None:
                stak.append(token)
        
    def getToken(self, tokStr, codeGen):
        registerOp = False
        if tokStr == "" or tokStr[0] == '#':
            return None
        if tokStr[0] == 'R':
            registerOp = True
            tokStr = tokStr[1:]
        if tokStr[0] == '"':
            return string(tokStr[1:], registerOp)
        if tokStr[0] == '[':
            return self.makeStack(tokStr, codeGen, registerOp)
        if tokStr.isdigit():
            return number(tokStr, registerOp)
        if tokStr == "True" or tokStr == "False":
            return boolean(tokStr, registerOp)
        if tokStr in self.commands:
            return command(tokStr, registerOp)
        #This ain't Python that notifies you of every little thing!
        #Invalid tokens will just get dropped
        #raise interpreterError("Lexer Error: invalid token")
        return None
                
    def makeStack(self, tokStr, codeGen, registerOp):
        stackToken = []
        tokStr = tokStr[1:]
        while tokStr.strip() != ']':
            token = self.getToken(tokStr, codeGen)
            if token is not None:
                stackToken.append(token)
            tokStr = next(codeGen)
        return stack(stackToken, registerOp)

    #These functions implement the language tokens
    #Stack operations
    def pushFromReg(self, cmd):
        if self.register is not None and not cmd.registerOp:
            self.currentStack.append(self.register)
            self.register = None

    def popToReg(self, cmd):
        if not cmd.registerOp:
            try:
                self.register = self.currentStack.pop()
            except:
                self.register = None

    def pushToToken(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if isinstance(b, stack):
            b.token.append(a)
            if cmd.registerOp:
                self.register = b
            else:
                self.currentStack.append(b)
        else:
            raise interpreterError("Push to a non-stack object.")

    def popFromToken(self, cmd):
        if cmd.registerOp:
            if isinstance(self.register, stack):
                try:
                    a = self.register.pop()
                except:
                    raise interpreterError("Pop from an empty stack!")
                self.currentStack.append(a)
        else:
            try:
                if isinstance(self.currentStack[-1], stack):
                    a = self.currentStack[-1].pop()
                else:
                    raise interpreterError("Pop from a non-stack object")
            except:
                raise interpreterError("Pop from an empty stack!")
            self.register = a
                
    def swap(self, cmd):
        if not cmd.registerOp:
            a, b = self.getTwo(False)
            self.currentStack.extend([a, b])

    def dup(self, cmd):
        if not cmd.registerOp:
            try:
                #Use copy because Python passes by reference
                self.currentStack.append(copy.deepcopy(self.currentStack[-1]))
            except:
                raise interpreterError("Can't dup an empty stack!")

    def drop(self, cmd):
        self.getOne(cmd.registerOp)
            
    def rot(self, cmd):
        if cmd.registerOp:
            a, b = self.getTwo(cmd.registerOp)
            self.currentStack.append(a)
            self.register = b
        else:
            try:
                a, b = self.stackOne.pop(), self.stackTwo.pop()
                self.stackOne.append(b)
                self.stackTwo.append(a)
            except:
                raise interpreterError("Pop from an empty stack!")
            
    def flip(self, cmd):
        if self.stackOne == self.currentStack:
            self.currentStack = self.stackTwo
        else:
            self.currentStack = self.stackOne

    def warp(self, cmd):
        if self.stackOne == self.codeStack:
            self.codeStack = self.stackTwo
        else:
            self.codeStack = self.stackOne

    def drain(self, cmd):
        if cmd.registerOp:
            self.register = None
        else:
            while self.currentStack != []:
                self.currentStack.pop()

    #Flow Control
    def evl(self, cmd):
        a = self.getOne(cmd.registerOp)
        if isinstance(a, stack) and not a:
            a = boolean("False", cmd.registerOp)
        if a is not None:
            self.apstend(self.codeStack, a)

    def unwrap(self, cmd):
        if not cmd.registerOp and isinstance(self.currentStack[-1],stack):
            try:
                a = self.currentStack.pop()
            except:
                raise interpreterError("Pop from an empty stack!")
            self.currentStack.extend(a.token)

    def iff(self, cmd):
        cond, a = self.getTwo(cmd.registerOp)
        if isinstance(cond, stack):
            self.codeStack.append(cmd)
            self.codeStack.extend(cond.token)
            self.currentStack.append(a)
        else:
            if cond:
                self.apstend(self.codeStack, a)

    def ife(self, cmd):
        cond, a = self.getTwo(cmd.registerOp)
        if isinstance(cond, stack):
            self.codeStack.append(cmd)
            self.codeStack.extend(cond.token)
            self.currentStack.append(a)
        else:
            b = self.getOne(False)
            if cond:
                self.apstend(self.codeStack, a)
            else:
                self.apstend(self.codeStack, b)
                
            
    #Arithmetic Operations
    def add(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if cmd.registerOp:
            register = a + b
        else:
            self.currentStack.append(a + b)

    def subtract(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if cmd.registerOp:
            register = b - a
        else:
            self.currentStack.append(b - a)

    def multiply(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if cmd.registerOp:
            register = b * a
        else:
            self.currentStack.append(b * a)

    def divide(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if cmd.registerOp:
            register = b / a
        else:
            self.currentStack.append(b / a)

    def modulo(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if cmd.registerOp:
            register = b % a
        else:
            self.currentStack.append(b % a)

    def exp(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if cmd.registerOp:
            register = b ** a
        else:
            self.currentStack.append(b ** a)

    #Boolean operations
    def lt(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if self.checkForStack(cmd, a, b):
            if cmd.registerOp:
                register = boolean(b<a, False)
            else:
                self.currentStack.append(boolean(b<a, False))

    def gt(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if self.checkForStack(cmd, a, b):
            if cmd.registerOp:
                register = boolean(b>a, False)
            else:
                self.currentStack.append(boolean(b>a, False))

    
    def lte(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if self.checkForStack(cmd, a, b):
            if cmd.registerOp:
                register = boolean(b<=a, False)
            else:
                self.currentStack.append(boolean(b<=a, False))

    def gte(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if self.checkForStack(cmd, a, b):
            if cmd.registerOp:
                register = boolean(b>=a, False)
            else:
                self.currentStack.append(boolean(b>=a, False))
    
    def eq(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if self.checkForStack(cmd, a, b):
            if cmd.registerOp:
                register = boolean(b==a, False)
            else:
                self.currentStack.append(boolean(b==a, False))        

    def logicalNot(self, cmd):
        a = self.getOne(cmd.registerOp)
        if isinstance(a, stack):
            codeStack.append(cmd)
            self.eval(a)
        else:
            if cmd.registerOp:
                register = boolean(not a, False)
            else:
                self.currentStack.append(boolean(not a, False))

    def andAnd(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if self.checkForStack(cmd, a, b):
            if cmd.registerOp:
                register = boolean(b and a, False)
            else:
                self.currentStack.append(boolean(b and a, False))    

    def orOr(self, cmd):
        a, b = self.getTwo(cmd.registerOp)
        if self.checkForStack(cmd, a, b):
            if cmd.registerOp:
                register = boolean(b or a, False)
            else:
                self.currentStack.append(boolean(b or a, False))

    #I/O
    def put(self, cmd):
        print(self.getOne(cmd.registerOp), end=" ")
    def putc(self, cmd):
        tok = self.getOne(cmd.registerOp)
        if isinstance(tok, number):
            print(chr(tok.token), end="")
        else:
            print(tok, end="")
    def get(self, cmd):
        r = input(">>>")
        gen = (tokstr for tokstr in r.split(';'))
        self.parseList(gen, self.currentStack)
    def getc(self, cmd):
        r = input(">>>")
        r = string(r, False)
        if cmd.registerOp:
            self.register = r
        else:
            self.currentStack.append(r)

def interpret(strang):
    codeGen = (x.lstrip() for x in strang.split(';') )
    a = staple()
    a.parseList(codeGen, a.codeStack)
    a.run()
