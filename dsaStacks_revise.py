#stacks.. stack is lifo btw

stack = []

#push
stack.append('A')    #here is [0]
stack.append('b')   #[1] 
stack.append(5)
stack.append('ty')  #starts from here [-1]

print(stack)

#peek

topElement = stack[0] #last in first out in stacks.. this'll be the last element in the stack

print("lifo :", topElement)

pop = stack.pop()

print(pop)

#check if empty.. 

# isEmpty =  bool(stack)
# print(isEmpty)

print(len(stack))

#classes with stack

class Stack:
    def __init__(self):

        #creates the list/stack assigns self to it
        self.stack = []
        

    #push uses the .append method on stack with parameter element. anytime this func is called, it will take in this element so we can use this to populate the stack. kind of like set? maybe
    def push(self, element):
        self.stack.append(element)

    def pop(self):
        if self.isEmpty():
            return "Stack is empty"
        return self.stack.pop()

    def peek(self):
        if self.isEmpty():
            return "Stack is empty"
        return self.stack[-1]

    def isEmpty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)


myStack = Stack()

myStack.push("car")
myStack.push("dog")
myStack.push("meat")
myStack.push("jett")

#prints just the stack..
print(myStack.stack)

#removes and returns the first element in stack.. 
print(myStack.pop())

#stack after pop
print(myStack.stack)

#peek.. 

print(myStack.peek())

#check if stack is empty
print(myStack.isEmpty())

#check size 

print(myStack.size())