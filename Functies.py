def change(func):
      toevoeging = ""
      newfunc = ""
      func = func.split("+")
      for i in range(len(func)):
          func[i] = func[i].split("^")
          try:
              a = int(func[i][1])
              
          except:
              continue
          
          for j in range(a-1):
              toevoeging += "*{}".format(func[i][0][-1])
              
             
          func[i][0] = "{}".format(func[i][0]) + toevoeging
          toevoeging = ""
          newfunc += func[i][0] + "+"
      newfunc = newfunc[:-1]
      if newfunc == "":
          for i in range(len(func)):
              newfunc += func[i][0] + "+"
          newfunc = newfunc[:-1]
          return newfunc
      else:
          return newfunc
