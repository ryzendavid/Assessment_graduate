x = "me"
try:
    print(x)
except:
    print("Error x is not defined")
else:
    print("no other issue")  #else works if error is not activated


try:
    print(x)
except:
    print("Error x is not defined")
finally:
    print("Code successfully run")  # finally to always run even if there is an error

try:
    f = open("demofile.txt")
    try:
        f.write("Some words written here")
    except:
        print("Could not write to file")
    finally:
        f.close()
except:
    print("Error opening file, may not exisit")

    #raising exeception.. 

x = 3

if x < 1:
    raise Exception("no num below 2, try again")

y = 30

if not type(y) is int:
    raise Exception(" needs to be a number try again")

print("Test")