#dict 

someDict = {
    "brand" : "Ford",
    "model" : "Mustant",
    "Country" : "America",
    "Country" : "merica",
    "Available Colors" : ["red", "blue", "yellow", "green"]
}

print(someDict)

print(len(someDict))

#can also use contstructor for dict

thisDict = dict(car = "Ford", age = 24)

print(thisDict)

#can access specicif items in dicts

print(someDict["brand"]) #or you could assign the value in the print method to a var

#using get
x = someDict.get("Country")
y = someDict.keys()
z = someDict
print(x," ", y)

#aqdding a key to the dict

someDict ["range in mi"] = 500

print(y)
print(z)

#.values returns all values

ZValue = z.values()
Zitem = z.items()

print("ZZZZ:",ZValue)

print("se")
print(Zitem)

someDict["Ice"] = True
print(Zitem)

#checks if key exists in dict

if "Ice" in someDict:
    print("This key exists in the dict")
else:
    print("no key")

print(z.get("Ice"))

#change values of keys

someDict["Ice"] = "yes"
print (z.get("Ice"))

#use update() to update the dict

someDict.update({"model" : "Mustang"})

#adding new items to the dict

someDict["Suspensed"] = False  #also use update to add items to the dict


#removing items, use .pop()

#someDict.pop("Suspended") also can use del. note del can delete the dictionary... e.g del someDict

del someDict["Suspensed"]

print(z)

#use .clear() to empty/clear the dict. someDict.clear() but don't want the dict cleared right now... 


#looping thrrough dict..

for q in someDict:
    print(q)

for q in someDict.values(): #can also do tha same for keys..
    print(q)

#looping through key and val

for a,b in someDict.items():
    print(a,b)


#copying dictionary use .dict() both are now separate copies. assisgning a var to a dict makes it the exact same copy, any changes made on the original dict is reflected on the copied in var (assigned.. )

someDictCOPY = someDict.copy()

#nested dicts

NestDict = {
    "Person1" : {
        "name" : "Ella",
        "year" : 2000
    },
    "person2" : {
    "name" : "Tobias",
    "year" : 2007
       },
    "per3" : {
    "name" : "Linus",
    "year" : 2011
  }
}

#accessing nestDict use name of outer dict

print(NestDict["Person1"] )

#looping nestDict

for x, obj in NestDict.items():
    print(x)
    
    for y in obj:
        print(y + ":", obj[y])