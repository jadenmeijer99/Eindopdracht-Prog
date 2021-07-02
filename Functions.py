def changepower(func):
    # changes string representation of powers, eg "2**3+4^2" becomes "2*2*2+4*4"
    toevoeging = ""
    newfunc = ""

    #replace all ** to ^
    func = func.replace("**", "^")

    #split function to seperate terms
    func = func.split("+")
    for x in range(len(func)):
        func[x] = func[x].split("*")
    for x in range(len(func)):
        for y in range(len(func[x])):
          func[x][y] = func[x][y].split("-")
    funcflat = [l for z in func for k in z for l in k if "^" in l]
    for i in range(len(funcflat)):
       
       #Split terms with powers to their base and power
        funcflat[i] = funcflat[i].split("^")
        try:
            a = int(funcflat[i][1])
        except:
            continue
        
        # add the base element to toevoeging the power-1 amount of times
        for j in range(a-1):
            toevoeging += "*{}".format(funcflat[i][0][-1])
          #replace the base with the base plus power-1 times the base
        funcflat[i][0] = "{}".format(funcflat[i][0]) + toevoeging
        #clear toevoeging for next term
        toevoeging = ""
    
    for i in range(len(funcflat)):
        # add all bases of the terms and add them to a string
        newfunc += funcflat[i][0] + "+"
    newfunc = newfunc[:-1]
    
    # if the new string is empty then none of the terms had powers so add the terms to a string
    if newfunc == "":
        for i in range(len(func)):
            for j in range(len(func[i])):
                for k in range(len(func[i][j])):
                    newfunc += func[i][j][k][0] + "-"
                newfunc = newfunc[:-1]
                newfunc += func[i][0] + "*"
        newfunc = newfunc[:-1]
        return newfunc
    else:
        return newfunc

print(changepower("b**3*x**3"))