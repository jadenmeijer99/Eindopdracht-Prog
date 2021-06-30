def changepower(func):
      # changes string representation of powers, eg "2**3+4^2" becomes "2*2*2+4*4"
      toevoeging = ""
      newfunc = ""

      #replace all ** to ^
      func = func.replace("**", "^")

      #split function to seperate terms
      func = func.split("+")
      for i in range(len(func)):
         
         #Split terms with powers to their base and power
          func[i] = func[i].split("^")
          try:
              a = int(func[i][1])
          except:
              continue
          
          # add the base element to toevoeging the power-1 amount of times
          for j in range(a-1):
              toevoeging += "*{}".format(func[i][0][-1])
            #replace the base with the base plus power-1 times the base
          func[i][0] = "{}".format(func[i][0]) + toevoeging
          #clear toevoeging for next term
          toevoeging = ""
      
      for i in range(len(func)):
          # add all bases of the terms and add them to a string
        newfunc += func[i][0] + "+"
      newfunc = newfunc[:-1]
      
      # if the new string is empty then none of the terms had powers so add the terms to a string
      if newfunc == "":
          for i in range(len(func)):
              newfunc += func[i][0] + "+"
          newfunc = newfunc[:-1]
          return newfunc
      else:
          return newfunc
