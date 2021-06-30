import Functions
import copy
class LambdaTerm:
    #Abstract Base Class for lambda terms.

    def fromstring(self):
        """Construct a lambda term from a string.
        aanvoer r"\v b" waarbij v de variabele is en b de body 
        aan elkaar als het een gewonen expression is en in de vorm v. b als het een abstraction is."""
        appcheck = self.split("\\")
        appcheck.pop(0)
        if len(appcheck) != 1:
            #Create Application object
            funcs = []
            for x in appcheck:
                exp = Functions.changepower(x).split()
                expr1 = exp.pop(0)
                funcs.append(Abstraction(expr1,exp))
            return Application(funcs[:-1],funcs[-1])
        else:
            #Create Abstraction object
            exp = Functions.changepower(appcheck[0]).split()
            expr1 = exp[0][0]
            exp.pop(0)
            return Abstraction(expr1,exp)
    def __eq__(self, G):
        """checks if string representations of two reduced lambda functions
        or a lambda function and an integer or string are equal"""
        if type(G) == int or type(G) == str:
            return self.reduce() == str(G)
        return self.reduce() == G.reduce()
    def __req__(self, G):
        """checks if string representations of two reduced lambda functions
        or a lambda function and an integer or string are equal if the order of the two is reversed"""
        if type(G) == int or type(G) == str:
            return self.reduce() == str(G)
        return self.reduce() == G.reduce()

        


class Variable(LambdaTerm):
    #Represents a variable.

    def __init__(self, symbol):
        if "**" in symbol or "^" in symbol:
            self.symb = Functions.changepower(symbol)
        else:
            self.symb = symbol
    def __repr__(self):
        return "Variable({})".format("'" + str(self.symb) + "'")
    def __str__(self):
        return str(self.symb)
    def substitute(self, rules):
        #aanvoer "A1 = 7" voor het variabel.
        rules = rules.replace(" ","")
        terms = rules.split("=")
        if terms[0] in self.symb:
            self.symb = self.symb.replace(terms[0], terms[1])


class Abstraction(LambdaTerm):
    #Represents a lambda term of the form (λx.M).

    def __init__(self, variable, body):
        if type(variable) == str:
            finvar = variable.replace(".","")
            self.var = Variable(finvar)
        else:
            self.var = variable
        if type(body) == list and len(body)>1:
            self.body = Abstraction(body.pop(0), body)
        elif type(body) == list:
            self.body = Variable(body[0])
        elif type(body) == Variable:
            self.body = body
        else:
            self.body = Variable(body)
    
    def __repr__(self):
        return "Abstraction({}, {})".format(repr(self.var), repr(self.body))
    def __str__(self):
        #output gives the LambdaTerm in the form "λx.M" where x is self.var and M is self.body
        #output gives the LambdaTerm in the form (λx.M)N where x is self.var , M is self.body , and N is self.arg
        return chr(955) + str(self.var) + "." + str(self.body)

    def __call__(self, argument):
        selfcpy = copy.deepcopy(self)
        if type(argument) == int:
            selfcpy.substitute("{} = {}".format(str(selfcpy.var),str(argument)))
            return selfcpy.reduce()
        elif type(argument) == list:
            if len(argument) != 1:
                selfcpy.substitute("{} = {}".format(str(selfcpy.var),str(argument[0])))
                argument.pop(0)
                return selfcpy.body(argument)
            else:
                return selfcpy(argument[0])

    def substitute(self, rules):
        #aanvoer "A1 = 7" voor het variabel.
        self.var.substitute(rules)
        self.body.substitute(rules)

    
    def reduce(self, input = ""):
        #Beta-reduce.
        #aanvoer "A0 = x0 A1 = x1 ... An = xn" voor de n variabelen.
        # (/\A1.(/\A2.(...(/\An.b)xn)...)x2)x1
        newAbstr = copy.deepcopy(self)
        bodies = [newAbstr, newAbstr.body]
        bod = newAbstr.body
        while type(bod) == Abstraction:
            bod = bod.body
            bodies.append(bod)
        if input == "":
            try:
                return eval(str(bodies[-1]))
            except:
                return str(bodies[-1])
        terms = input.split()
        for i in range(len(bodies)-1):
            if str(bodies[i].var) in terms:
                j = terms.index(str(bodies[i].var))
                bodies[i].substitute("{} {} {}".format(terms[j], terms[j+1], terms[j+2]))
            else:
                continue
        try:
            return eval(str(bodies[-1]))
        except:
            return str(bodies[-1])
        





class Application(LambdaTerm):
    #Represents a lambda term of the form (M N).

    def __init__(self, function, argument):
        if type(function) == list:
            if len(function) != 1:
                self.func = Application(function[:-1],function[-1])
            else:
                self.func = function[0]
        elif type(function) == Abstraction or type(function) == Application:
            self.func = function
        else:
            self.func = LambdaTerm.fromstring(function)
        if type(argument) == str:
            self.arg = Variable(argument)
        else:
            self.arg = argument

    def __repr__(self):
        return "Application({}, {})".format(repr(self.func), repr(self.arg))
    def __str__(self): 
        #output gives the LambdaTerm in the form (λx.M)N where x is self.var , M is self.body , and N is self.arg
        if type(self.arg) == Variable:
            return "(" + str(self.func) + ") " + str(self.arg)
        elif type(self.arg) == Abstraction:
            return "(" + str(self.func) + ") " + "(" + str(self.arg) + ")"

    def substitute(self, rules): 
        #aanvoer "A1 = 7" voor het variabel die in de functie veranderd moet worden.
        self.func.substitute(rules)

    def reduce(self, input = ""):
        #Beta-reduce.
        #aanvoer "A0 = x0 A1 = x1 ... An = xn, A0 = x0 A1 = x1 ... An = xn"
        #voor de n variabelen in de functie en het argument.
        if type(self.func) == Abstraction:
            newAbstr = copy.deepcopy(self)
            bodies = [newAbstr.func, newAbstr.func.body]
            bod = newAbstr.func.body
            while type(bod) == Abstraction:
                bod = bod.body
                bodies.append(bod)
            if str(bodies[0].var) in str(bodies[-1]):
                if type(newAbstr.arg) == Abstraction:
                    if str(newAbstr.arg.var) in str(bodies[-1]):
                        raise ValueError("Varable {} is used as a representation for two distinct variables. \nPlease use the substitute function to change one of them.".format(str(newAbstr.arg.var)))
                    if len(str(bodies[-1])) > 1:
                        bodies[-1].substitute("{} = {}".format(str(newAbstr.func.var), str(newAbstr.arg.body)))
                        bodies[-2].body = Abstraction(newAbstr.arg.var, bodies[-1])
                    else:
                        bodies[-1].substitute("{} = {}".format(str(newAbstr.func.var), str(newAbstr.arg.body)))
                else:
                    bodies[-2].substitute("{} = {}".format(str(newAbstr.func.var), str(newAbstr.arg)))
                return bodies[0].reduce(input)
            else:
                return bodies[0].reduce(input)
        



    
"""Test Area"""
    


x = Variable('x')
id = Abstraction(Variable('a'), Variable('a'))
id2 = Abstraction(Variable('b'), Variable('b'))
id_x = Application(id, x)
id_x2 = Application(id, id2)
tt = LambdaTerm.fromstring(r"\a a*a+a")
tt2 = LambdaTerm.fromstring(r"\a b. a")
tt3 = LambdaTerm.fromstring(r"\a b. x. a*b*x")
hope = LambdaTerm.fromstring(r"\a b. a*b \b b**3")
k = Abstraction(Variable('x'), Variable('x^6'))
kk = Abstraction(Variable('x'), Variable('x**6'))

for t in [x,id,id_x]: print(str(t))
for t in [x,id,id_x]: print(repr(t))
print(id_x, "-->", id_x.reduce('x = 34'))
print(id(26))
for t in [tt,tt2,tt3]: print(str(t))
for t in [tt,tt2,tt3]: print(repr(t))
for t in [tt,tt2,tt3]: print(t(20))
for t in [tt,tt2,tt3]: print(t.reduce())
print(tt3([3,4,5]))
for t in [tt,tt2,tt3]: print(t)
print(str(id_x2))
print(hope)
hope.substitute("b = c")
print(str(hope))
print(hope.reduce())
print(hope.reduce("b = 3 c = 4"))
print(tt3([2,3,4]))
print(k(6) == kk(6))
print(k(6) == 46656)
print(46656 == k(6))

