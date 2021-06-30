import Functies
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
            funcs = []
            for x in appcheck:
                exp = x.split()
                expr1 = exp.pop(0)
                funcs.append(Abstraction(expr1,exp))
            return Application(funcs[:-1],funcs[-1])
        else:
            exp = appcheck[0].split()
            expr1 = exp[0][0]
            exp.pop(0)
            return Abstraction(expr1,exp)
    def __eq__(self, G):
        #checks if string representations of two lambda functions are equal
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
        #aanvoer "A1 = 7" voor het variabel.
        terms = rules.split()
        if terms[0] in self.symb:
            self.symb = self.symb.replace(terms[0], terms[2])


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
        else:
            self.body = Variable(body)
    
    def __repr__(self):
        return "Abstraction({}, {})".format(repr(self.var), repr(self.body))
    def __str__(self):
        return chr(955) + str(self.var) + "." + str(self.body)

    def __call__(self, argument):
        raise NotImplementedError

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
            return str(bodies[-1])
        terms = input.split()
        for i in range(len(bodies)-1):
            if str(bodies[i].var) in terms:
                j = terms.index(str(bodies[i].var))
                bodies[i].substitute("{} {} {}".format(terms[j], terms[j+1], terms[j+2]))
            else:
                continue
        print(bodies)
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

        #self.redu = Abstraction(self.arg, self.func.reduce("{} = {}".format(str(self.func.var), str(self.arg))))

    def __repr__(self):
        return "Application({}, {})".format(repr(self.func), repr(self.arg))
    def __str__(self): 
        if type(self.arg) == Variable:
            return "(" + str(self.func) + ") " + str(self.arg)
        elif type(self.arg) == Abstraction:
            return "(" + str(self.func) + ") " + "(" + str(self.arg) + ")"

    def substitute(self, rules): 
        #aanvoer "A1 = 7" voor het variabel.
        raise NotImplementedError

    def reduce(self, input = ""):
        #Beta-reduce.
        #aanvoer "A0 = x0 A1 = x1 ... An = xn" voor de n variabelen.
        raise NotImplementedError
        



    

    


x = Variable('x')
id = Abstraction(Variable('a'), Variable('a'))
id2 = Abstraction(Variable('b'), Variable('b'))
id_x = Application(id, x)
id_x2 = Application(id, id2)
tt = LambdaTerm.fromstring(r"\a a*a+a")
tt2 = LambdaTerm.fromstring(r"\a b. a")
tt3 = LambdaTerm.fromstring(r"\a b. x. a*b*x")
hope = LambdaTerm.fromstring(r"\a a*a \b b*b*b")
k = Abstraction(Variable('x'), Variable('x^6'))
kk = Abstraction(Variable('x'), Variable('x**6'))

for t in [x,id,id_x]: print(str(t))
for t in [x,id,id_x]: print(repr(t))
#print(id_x, "-->", id_x.reduce('x = 34'))
#print(id(26))

for t in [tt,tt2,tt3]: print(str(t))
for t in [tt,tt2,tt3]: print(repr(t))
#for t in [tt,tt2,tt3]: print(t(20))
for t in [tt,tt2,tt3]: print(t.reduce())
print(tt3.reduce("a = 3 b = 4 x = 6"))
#for t in [tt,tt2,tt3]: print(t)
print(str(id_x2))
print(str(hope))
#print(tt3([2,3,4]))
#print(k == kk)
