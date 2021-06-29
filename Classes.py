class LambdaTerm:
    #Abstract Base Class for lambda terms.

    def fromstring(self):
        """Construct a lambda term from a string.
        aanvoer r"\v b" waarbij v de variabele is en b de body 
        aan elkaar als het een gewonen expression is en in de vorm v. b als het een abstraction is."""
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
        #aanvoer "A1 A2 A3 A4 ... An" voor de n variabelen.
        exp = rules.split()
        self.substitute(exp)
        
    def reduce(self):
        #Beta-reduce.
        raise NotImplementedError
    
    def __eq__(self, G):
        #checks if string representations of two lambda functions are equal
        return str(self) == str(G)
        


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
        if terms[0] == self.symb:
            self.symb = terms[2]


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

    def __call__(self, argument):
        term = "{} = {}".format(str(self.var), str(argument))
        return self.reduce(term)

    def substitute(self, rules):
        #aanvoer "A1 = 7" voor het variabel.
        values = rules.split()
        return str(self.body).replace(values[0], values[2])

    
    def reduce(self, input = ""):
        #Beta-reduce.
        #aanvoer "A1 A2 A3 A4 ... An" voor de n variabelen.
        if type(self.body) == Variable:
            if input == "":
                return str(self.body)
            else:
                output = self.substitute(input)
                return eval(output)
        else:
            if input == "":
                return str(self.body.reduce(input))
            else:
                output = self.body.substitute(input)
                try:
                    return eval(output)
                except:
                    return output





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
        self.redu = Abstraction(self.arg, self.func.reduce("{} = {}".format(str(self.func.var), str(self.arg))))

    def __repr__(self):
        return "Application({}, {})".format(repr(self.func), repr(self.arg))
    def __str__(self): 
        return "(" + str(self.func) + ") " + str(self.arg)

    def substitute(self, rules): 
        #aanvoer "A1 = 7" voor de het variabel.
        values = rules.split()
        self.redu.body = Variable(str(self.redu.body).replace(values[0], values[2]))

    def reduce(self, input = ""):
        #Beta-reduce.
        #aanvoer "A0 = x0 A1 = x1 ... An = xn" voor de n variabelen.
        if input == "":
            return self.redu.substitute("{} = {}".format(str(self.func.var), str(self.arg)))
        else:
            terms = input.split()
            newApp = Application(self.redu, self.arg)
            for i in range(0, len(terms)-2,3):
                newApp.substitute("{} {} {}".format(terms[0], terms[1], terms[2]))
            try:
                return eval(str(newApp.redu.body))
            except:
                return str(newApp.redu.body)
        



    

    


x = Variable('x')
id = Abstraction(Variable('a'), Variable('a'))
id_x = Application(id, x)
tt = LambdaTerm.fromstring(r"\a a*a+a")
tt2 = LambdaTerm.fromstring(r"\a b. a")
tt3 = LambdaTerm.fromstring(r"\a b. x. a*b*x")



for t in [x,id,id_x]: print(str(t))
for t in [x,id,id_x]: print(repr(t))
print(id_x, "-->", id_x.reduce('x = 34'))
print(id(26))
for t in [tt,tt2,tt3]: print(str(t))
for t in [tt,tt2,tt3]: print(repr(t))
for t in [tt,tt2,tt3]: print(t(20))
for t in [tt,tt2,tt3]: print(t.reduce())



