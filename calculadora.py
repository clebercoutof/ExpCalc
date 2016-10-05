import  string
import sys
import operator
import re

#Defines
OP = '('
CP = ')'
OBR = '['
CBR = ']'

class Stack:

    def __init__(self,):
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

#Checks if there are any letters in the expression
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
                print("Function isn't balanced, check your parenthesis and brackets")
                return True
        #If the the elements were compatible , then removes the opened one.
            else:
                stack.pop()

    #Checks if the function is balanced
    if stack.size() == 0:
        return False
    else:
        print("Function isn't balanced, check your parenthesis and brackets")
        return True

#Substitutes brackets for parenthesis
def bracketstoparenthesis(list):
    for i in list:
        if i == '[':
            i = '('
        elif i == ']':
            i = ')'
    return list

#Function that separates operators from parenthesis and numbers, (SUPORTS 2 DIGIT NUMBERS)
def split_numbers(expression):
    x = re.findall('[+-/*//()!^]|\d+',expression)
    return x

#Binary Tree Class
class BinaryTree:
    def __init__(self,rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self,newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self,newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t


    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self,obj):
        self.key = obj

    def getRootVal(self):
        return self.key

def buildParseTree(exp):
    #Since our expression was previously balanced we can substituite the brackets by parenthesis
    exp = bracketstoparenthesis(exp)
    #We turn our string into a list
    list = split_numbers(exp)
    #The stack used to save the parents RootVal
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree
    for i in list:
        if i == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.getLeftChild()
        elif i not in ['+', '-', '*', '/', ')']:
            currentTree.setRootVal(int(i))
            parent = pStack.pop()
            currentTree = parent
        elif i in ['+', '-', '*', '/']:
            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            raise ValueError
    return eTree

def evaluate(parseTree):
    operators = {'+':operator.add, '-':operator.sub,'*':operator.mul, '/':operator.truediv}
    leftC = parseTree.getLeftChild()
    rightC = parseTree.getRightChild()

    if leftC and rightC:
        #Uses the dictionary to implement the operator library
        fn = operators[parseTree.getRootVal()]
        return fn(evaluate(leftC),evaluate(rightC))
    else:
        return parseTree.getRootVal()


while(True):
    x = input("Expression:")
    #If the expression contain letters, request the expression again
    if letter_check(x):
        continue
    #If the expression is unbalanced , request it again
    elif func_unbalance(x):
        continue
    else:
        parseTree = buildParseTree(x)
        print (evaluate(parseTree))
