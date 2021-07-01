from Classes import LambdaTerm
from Classes import Variable
from Classes import Abstraction
from Classes import Application

"""Begin Class tests"""

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
k3 = LambdaTerm.fromstring(r"\a b. a*b \y d. y*d")
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

"""End Class tests"""

"""Begin Function tests"""

#test here

"""End Function tests"""