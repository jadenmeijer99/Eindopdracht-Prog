class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    def fromstring(self):
        """Construct a lambda term from a string."""
        exp = (self.rstrip(")")).lstrip("(")
        if ord(exp[0]) == 955:
            #abstraction
            terms = (exp.replace(chr(955), "")).split(".")
            return Abstraction(terms[0],terms[1])
        else:
            #application
            terms = exp.split()
            return Application(terms[0],terms[1])

    def substitute(self, rules):
        """Substitute values for keys where they occur."""
        raise NotImplementedError
            

    def reduce(self):
        """Beta-reduce."""
        raise NotImplementedError


class Variable(LambdaTerm):
    """Represents a variable."""

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
    """Represents a lambda term of the form (λx.M)."""

    def __init__(self, variable, body):
        self.var = Variable(variable)
        self.body = Variable(body)
    
    def __repr__(self):
        return "Abstraction({},{})".format(repr(self.var), repr(self.body))
    def __str__(self):
        return chr(955) + str(self.var) + "." + str(self.body)

    def __call__(self, argument): raise NotImplementedError

    def substitute(self, rules): raise NotImplementedError


class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    def __init__(self, function, argument):
        exp = (((str(function).rstrip(")")).lstrip("(")).replace(chr(955),"")).split(".")
        self.func = Abstraction(exp[0],exp[1])
        self.arg = Variable(argument)
    def __repr__(self):
        return "Application({},{})".format(repr(self.func), repr(self.arg))
    def __str__(self): 
        return "(" + str(self.func) + ") " + str(self.arg)

    def substitute(self, rules): raise NotImplementedError

    def reduce(self): raise NotImplementedError

x = Variable('x')
id = Abstraction(Variable('a'), Variable('a'))
id_x = Application(id, x)

for t in [x,id,id_x]: print(str(t))
for t in [x,id,id_x]: print(repr(t))
