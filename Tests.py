from Classes import LambdaTerm
from Classes import Variable
from Classes import Abstraction
from Classes import Application
import copy
import time
"""Begin Class tests"""

#Debug section

print("\n---Debug tests--- \nPlease ingore the messiness \n ")
x = Variable('x')
id = Abstraction(Variable('a'), Variable('a'))
id2 = Abstraction(Variable('b'), Variable('b'))
id_x = Application(id, x)
id_x2 = Application(id, id2)
tt = LambdaTerm.fromstring(r"\a a*a+a")
tt2 = LambdaTerm.fromstring(r"\a b. a")
tt3 = LambdaTerm.fromstring(r"\a b. x. a*b*x")
hope = LambdaTerm.fromstring(r"\a b. a*b \b b**3 \x x*x \y d. y*d")
hope2 = LambdaTerm.fromstring(r"\a b. a*b \y d. y*d")
k = Abstraction(Variable('x'), Variable('x^6'))
kk = Abstraction(Variable('x'), Variable('x**6'))
k4 = LambdaTerm.fromstring(r"\b x. b*b*b*x*x \y d. y*d")

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
print(repr(hope))
hope.substitute("b = c")
print(str(hope))
print(hope.reduce("", True))
print(hope.reduce("d = 3 x = 4 y = 15"))
print(hope2.reduce())
print(hope2.reduce("", True))
print(hope2.reduce("y =32 b =3"))
print(tt3([2,3,4]))
print(k(6) == kk(6))
print(k(6) == 46656)
print(46656 == k(6))
print(k4.reduce())
print(k4.reduce("", True))
print(hope == k4)


#Unit test section

print("\n---Unit tests--- \nThese should all print True and/or the time taken\n")
fullstart = time.perf_counter_ns()
print("--init--")
start = time.perf_counter_ns()
x = Variable('x')
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
id = Abstraction(Variable('a'), Variable('a'))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
id2 = Abstraction(Variable('b'), Variable('b'))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
id_x = Application(id, x)
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
id_x2 = Application(id, id2)
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
tt = LambdaTerm.fromstring(r"\a a*a+a")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
tt2 = LambdaTerm.fromstring(r"\a b. a")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
tt3 = LambdaTerm.fromstring(r"\a b. x. a*b*x")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
hope = LambdaTerm.fromstring(r"\a b. a*b \b b**3 \x x*x \y d. y*d")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
hope2 = LambdaTerm.fromstring(r"\a b. a*b \y d. y*d")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
hope3 = copy.deepcopy(hope)
start = time.perf_counter_ns()
hope3.substitute("b = c")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
k = Abstraction(Variable('x'), Variable('x^6'))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
kk = Abstraction(Variable('x'), Variable('x**6'))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
k4 = LambdaTerm.fromstring(r"\b x. b**3*x*2 \y d. y*d")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))

print("--fromstring--")
start = time.perf_counter_ns()
print(str(tt) == "{}a.a*a+a".format(chr(955)))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(str(tt2) == "{}a.{}b.a".format(chr(955),chr(955)))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(str(tt3) == "{}a.{}b.{}x.a*b*x".format(chr(955),chr(955),chr(955)))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(str(hope) == "((({}a.{}b.a*b) ({}b.b*b*b)) ({}x.x*x)) ({}y.{}d.y*d)".format(chr(955),chr(955),chr(955),chr(955),chr(955),chr(955)))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(str(hope2) == "({}a.{}b.a*b) ({}y.{}d.y*d)".format(chr(955),chr(955),chr(955),chr(955)))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(str(k4) == "({}b.{}x.b*b*b*x*x) ({}y.{}d.y*d)".format(chr(955),chr(955),chr(955),chr(955)))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
print("--str--")
start = time.perf_counter_ns()
print((str(x) == "x"))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print((str(id) == "{}a.a".format(chr(955))))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print((str(id_x) == "({}a.a) x".format(chr(955))))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(str(hope3.reduce("", True)) == "{}x.{}y.{}d.y*d*y*d*y*d*x*x".format(chr(955),chr(955),chr(955)))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
print("--repr--")
start = time.perf_counter_ns()
print((repr(x) == "Variable('x')"))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print((repr(id) == "Abstraction(Variable('a'), Variable('a'))"))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print((repr(id_x) == "Application(Abstraction(Variable('a'), Variable('a')), Variable('x'))"))
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
print("--reduce--")
start = time.perf_counter_ns()
print(id.reduce() == "a")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(id_x.reduce() == "x")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(hope.reduce() == "Variable b is used as a representation for two distinct variables. \nPlease use the substitute function to change one of them.")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
start = time.perf_counter_ns()
print(hope3.reduce() == "y*d*y*d*y*d*x*x")
print("Process Time: {} ms".format(str(abs(time.perf_counter_ns() - start)/1000000)))
print("Total Unix test time: {} ms".format(str(abs(time.perf_counter_ns() - fullstart)/1000000)))

"""End Class tests"""

"""Begin Function tests"""

#test here

"""End Function tests"""