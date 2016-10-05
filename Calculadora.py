#!/usr/bin/env python

#Library for regular expressions
import  string
import sys
import operator
import re


OP = '('
CP = ')'
OBR = '['
CBR = ']'
FAC = '!'
OPERATOR= '+-/*'

##Stack to be used in the process
class Stack:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

#Queue to be used in the process
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self,item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

#Factorial Calculation
def factorial(x):
    factorial = 1
    while x > 0:
        factorial *=x
        x -= 1
    return factorial

#Checks if the current expression has letter( Returns TRUE if it has)
def letter_check(string):
    if re.search('[a-zA-Z]', string) :
        print ("The expression must not contain letters")
        return True

#Checks if the function is balanced, all the parentheses and brackets are correctly closed.(Returns FALSE if the expression is unbalanced)
def func_unbalance(string):
    stack = Stack()
    for i in range(len(string)):
        if string[i] == OP or string[i] == OBR:
            stack.push(string[i])
        elif string[i] == CP or string[i] == CBR:
        #Checks first if the stacks isn't empty
        #Then checks if the top of the stack is compatible with the element
            if stack.size() == 0 or stack.peek()== OP and string[i] == CBR or stack.peek() == OBR and string[i] == CP:
                return True
        #If the the elements were compatible , then removes the opened one.
            else:
                stack.pop()

    #Checks if the function is balanced
    if stack.size() == 0:
        return False
    else:
        return True

#Substitutes brackets for parenthesis
def bracketstoparenthesis(list):
    for i in list:
        if i == '[':
            i = '('
        elif i == ']':
            i = ')'
    return list

#Separates numbers from operators and parenthesis
def split_numbers(expression):
    x = re.findall('[+-/*//()!^]|\d+',expression)
    return x

#Pass the expression to the RPN notation
def shunting_yard(expression):
    stack = Stack()
    output = Queue()
    expression = bracketstoparenthesis(expression)
    vec = split_numbers(expression)
    for i in vec :
        #If token is a number, put it in the output
        if i.isdigit():
            output.enqueue(i)
        #If token is a function token (FACTORIAL), push it onto the stack
        elif i == FAC:
            stack.push(i)
        elif i == '^':
            stack.push(i)
        #if token is an operator and the stack was empty
        elif i in OPERATOR and stack.size() ==0:
            stack.push(i)
        #if the token is an operator and the stack had something
        elif i in OPERATOR:
            if i == '+' or i == '-':
                if stack.peek()== '+' or stack.peek() == '-':
                    a = stack.pop()
                    output.enqueue(a)
                    stack.push(i)
                elif stack.peek() == '*' or stack.peek()  == '/':
                    b = stack.pop()
                    output.enqueue(b)
                    stack.push(i)
                else:
                    stack.push(i)
            elif i == '*' or i == '/':
                if stack.peek() == '+' or stack.peek() == '-':
                    stack.push(i)
                elif stack.peek() == '*' or stack.peek() == '/':
                    c=stack.pop()
                    output.enqueue(c)
                    stack.push(i)
                #Case the top of the the stack is a parenthesis or a bracket
                else:
                    stack.push(i)

        # If token is a parenthesis '(',push it onto the stack
        elif i == OP:
            stack.push(i)

        # If token is a right parenthesis ')', until the token on the top of the stack is a left bracket, pop operators off the stack to the output queue
        elif i == CP:

            while stack.peek() != OP:
                x = stack.pop()
                output.enqueue(x)

            # Pop the left parenthesis from the stack, but not put in the output queue
            if stack.peek() == OP:
                stack.pop()

            # If the token at the top of the stack is a function token, pop into the output queue
            if stack.size()>0 and stack.peek() == FAC:
                y = stack.pop()
                output.enqueue(y)

    #While there are operators in the stack, pop them to the output queue
    while(stack.size() > 0):
        z = stack.pop()
        output.enqueue(z)
    #Returns the RPN expression
    RPN = []
    for i in range(output.size()):
        RPN.append(output.dequeue())

    return RPN

#Finds the value of the RPN notation
def calculate_rpn(list):
    stack = Stack()
    operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,'^':pow}
    #Loops through the list
    for i in list:
        #If it is an operator, pop the numbers from the stack, calculate the result and push it again
        if i not in '+-*/!^':
            stack.push(i)
        elif i in '!':
            c=float(stack.pop())
            stack.push(factorial(c))
        else:
            b = float(stack.pop())
            a = float(stack.pop())
            fn = operators[i]
            result = fn(a,b)
            stack.push(result)
    return stack.pop()

#Main Loop
while True:
    string = input("Type your expression:")
    #Checks if the expression contains letters
    if letter_check(string):
        continue
    #Checks for balanced brackets and parenthesis
    elif func_unbalance(string):
        print("Function isn't balanced, check your parenthesis and brackets")
        continue
    #Prints RPN nonation and the result
    else:
        x=shunting_yard(string)
        print ("This is the RPN notation:",x)
        y = calculate_rpn(x)
        print("This is your result",y)



#PROBLEMS
# input needs comma
