class LambdaTerm:
    #Abstract Base Class for lambda terms.

    def fromstring(self):
        #Construct a lambda term from a string.
        exp = self.split()
        condition = exp[0][:len(exp[0])-1]
        if condition == "\\":
            #Abstraction
            expr1 = exp[0][len(exp[0])-1:len(exp[0])]
            exp.pop(0)
            return Abstraction(expr1,exp)
        else:
            #Application
            func = exp[:len(exp)-1]
            return Application(func,exp[-1])

    def substitute(self, rules):
        #Substitute values for keys where they occur.
        raise NotImplementedError
        
    def reduce(self):
        #Beta-reduce.
        raise NotImplementedError


class Variable(LambdaTerm):
    #Represents a variable.

    def __init__(self, symbol):
        self.symb = symbol

    def __repr__(self):
        return "Variable({})".format("'" + str(self.symb) + "'")
    def __str__(self):
        return str(self.symb)
    def substitute(self, rules): 
        for x in rules:
            terms = ((x.rstrip("]")).lstrip("[")).split(":=")
            if terms[0] == self.symb:
                self.symb = terms[1]


class Abstraction(LambdaTerm):
    #Represents a lambda term of the form (λx.M).

    def __init__(self, variable, body):
        if type(variable) == str:
            finvar = variable.replace(".","")
            self.var = Variable(finvar)
        elif type(variable) == Variable:
            self.var = variable
        else:
            self.var = Variable(variable)
        if type(body) == list and len(body)>1:
            self.body = Abstraction(body.pop(0), body)
        elif type(body) == list:
            self.body = Variable(body[0])
        else:
            self.body = Variable(body)
    
    def __repr__(self):
        return "Abstraction({}, {})".format(repr(self.var), repr(self.body))
    def __str__(self):
        return chr(955) + str(self.var) + "." + str(self.body)

    def __call__(self, argument): raise NotImplementedError

    def substitute(self, rules): raise NotImplementedError


class Application(LambdaTerm):
    #Represents a lambda term of the form (M N).

    def __init__(self, function, argument):
        if type(function) == list:
            new = ""
            for x in function:
                new += x + " "
            self.func = LambdaTerm.fromstring(new)
        elif type(function) == Abstraction:
            self.func = function
        else:
            self.func = LambdaTerm.fromstring(function)
        self.arg = Variable(argument)
    def __repr__(self):
        return "Application({}, {})".format(repr(self.func), repr(self.arg))
    def __str__(self): 
        return "(" + str(self.func) + ") " + str(self.arg)

    def substitute(self, rules): raise NotImplementedError

    def reduce(self): raise NotImplementedError

x = Variable('x')
id = Abstraction(Variable('a'), Variable('a'))
id_x = Application(id, x)
tt = LambdaTerm.fromstring(r"\a b. a")

for t in [x,id,id_x]: print(str(t))
for t in [x,id,id_x]: print(repr(t))
print(repr(tt))
#yeet: the second coming
