import json


#converting from Json to py
jsonSample = '{"name" : "john", "age" : "30", "city" : "Los Angeles"}'

#parse json
y = json.loads(jsonSample)



print(y)

#from py to json

objDict = {
    "name" : "david",
    "car" : "Polestar",
    "course" : "Computer science"
}

#converting into json

yConv = json.dumps(objDict)

print(yConv)

print(type(y))


x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

#conv to json

xConv = json.dumps(x, indent=2, sort_keys=True,)

print(xConv)