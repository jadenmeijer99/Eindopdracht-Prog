from Functions import changepower
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
                exp = x.split()
                if "^" in exp[-1] or "**" in exp[-1]:
                    exp[-1] = changepower(exp[-1])
                expr1 = exp.pop(0)
                funcs.append(Abstraction(expr1,exp))
            return Application(funcs[:-1],funcs[-1])
        else:
            #Create Abstraction object
            if "^" in appcheck[0] or "**" in appcheck[0]:
                exp = changepower(appcheck[0]).split()
            else:
                exp = appcheck[0].split()
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
    #Represents a Variable.

    def __init__(self, symbol):
        if "**" in symbol or "^" in symbol:
            self.symb = changepower(symbol)
        else:
            self.symb = symbol

    def __repr__(self):
        return "Variable({})".format("'" + str(self.symb) + "'")

    def __str__(self):
        return str(self.symb)

    def substitute(self, rules):
        #substitutes the symbol for this Variable object
        rules = rules.replace(" ","")
        terms = rules.split("=")
        if terms[0] in self.symb:
            self.symb = self.symb.replace(terms[0], terms[1])


class Abstraction(LambdaTerm):
    #Represents a lambda term of the form (??x.M).

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
        elif type(body) == str:
            self.body = Variable(body)
        else:
            self.body = body
    
    def __repr__(self):
        return "Abstraction({}, {})".format(repr(self.var), repr(self.body))

    def __str__(self):
        #output gives the LambdaTerm in the form "??x.M" where x is self.var and M is self.body
        #or output gives the LambdaTerm in the form (??x.M)N where x is self.var , M is self.body , and N is self.arg
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
        #substitutes the variable and body for this Abstraction object
        self.var.substitute(rules)
        self.body.substitute(rules)

    def reduce(self, input = "", internal = False):
        #Beta-reduce.
        newAbstr = copy.deepcopy(self)
        bodies = [newAbstr, newAbstr.body]
        bod = newAbstr.body
        while type(bod) == Abstraction:
            bod = bod.body
            bodies.append(bod)
        if input == "":
            if internal:
                return bodies[0]
            try:
                return eval(str(bodies[-1]))
            except:
                return str(bodies[-1])
        tempterms = input.split()
        for k in range(len(tempterms)):
            tempterms[k] = tempterms[k].replace("=", "")
        tempterms = [a for a in tempterms if a != '']
        terms = []
        for x in range(0,len(tempterms),2):
            terms.append("{} = {}".format(tempterms[x], tempterms[x+1]))
        for i in range(len(bodies)-1):
            for h in range(len(terms)):
                if str(bodies[i].var) in terms[h]:
                    bodies[i].substitute(terms[h])
            else:
                continue
        if internal:
            return bodies[0]
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
        #output gives the LambdaTerm in the form (??x.M)N where x is self.var , M is self.body , and N is self.arg
        if type(self.arg) == Variable:
            return "(" + str(self.func) + ") " + str(self.arg)
        elif type(self.arg) == Abstraction:
            return "(" + str(self.func) + ") " + "(" + str(self.arg) + ")"

    def substitute(self, rules): 
        #substitutes the variable into the function of this Application object.
        self.func.substitute(rules)

    def reduce(self, input = "", internal = False):
        #Beta-reduce.
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
                        return "Variable {} is used as a representation for two distinct variables. \nPlease use the substitute function to change one of them.".format(str(newAbstr.arg.var))
                    if len(str(bodies[-1])) > 1:
                        #this does not carry the vars of the reduced statement
                        temp = newAbstr.arg.reduce("", True)
                        bod2 = temp.body
                        temp2 = temp.var
                        bodies2 = [temp2]
                        while type(bod2) == Abstraction:
                            temp2 = bod2.var
                            bod2 = bod2.body
                            bodies2.append(temp2)
                        bodies[-1].substitute("{} = {}".format(str(newAbstr.func.var), str(temp.reduce())))
                        j = len(bodies)-1
                        for i in range(len(bodies2)-1,-1,-1):
                            if type(bodies[j]) == Variable:
                                bodies[j-1].body = Abstraction(bodies2[i], bodies[j])
                                j -= 1
                            elif type(bodies[j]) == Abstraction:
                                bodies[j].body = Abstraction(bodies2[i], bodies[j].body)
                    else:
                        bodies[-1].substitute("{} = {}".format(str(newAbstr.func.var), str(newAbstr.arg.reduce())))
                else:
                    bodies[-2].substitute("{} = {}".format(str(newAbstr.func.var), str(newAbstr.arg)))
                if internal:
                    return bodies[0].body
                return bodies[0].reduce(input)
            else:
                if internal:
                    return bodies[0].body
                return bodies[0].reduce(input)
        elif type(self.func) == Application:
            newAppl = copy.deepcopy(self)
            funcs = [newAppl.func, newAppl.func.func]
            f = newAppl.func.func
            while type(f) == Application:
                f = f.func
                funcs.append(f)
            funcs.pop()
            newAbs = funcs[-1].reduce("", True)
            if type(newAbs) == str:
                return newAbs
            funcs[0].func = newAbs
            redfunc = funcs[0].reduce(input, True)
            if type(redfunc) == str:
                return newAbs
            Appl2 = Application(redfunc, newAppl.arg)
            if internal:
                return Appl2.reduce(input, True)
            return Appl2.reduce(input)
