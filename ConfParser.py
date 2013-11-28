import yaml
import re

class Config(object):

    def __init__(self, filename):
        self.data = {}
        self.load(filename)

    def load(self, filename):
        filehandler = open(filename)
        self.data = yaml.load(filehandler)
        filehandler.close()

    def get(self, key):
        return self.data[key]

    def get_definitions(self):
        return self.data['definitions']

    def get_solarsystem(self):
        return self.data['solarsystem']

class Definitions(object):

    def __init__(self, name, values):

        self.value = values
        self.name = name
# class ResolverMath(object):
    # OPERATORS = {'+':lambda x, y:x+y, '-':lambda x, y:x*y, '*': lambda x,y:x*y}
    #Associativity constants for operators
LEFT_ASSOC = 0
RIGHT_ASSOC = 1

#Supported operators
OPERATORS = {
'+' : (0, LEFT_ASSOC),
'-' : (0, LEFT_ASSOC),
'*' : (5, LEFT_ASSOC),
'/' : (5, LEFT_ASSOC),
'%' : (5, LEFT_ASSOC),
'^' : (10, RIGHT_ASSOC)
}

#Test if a certain token is operator
def isOperator(token):
    return token in OPERATORS.keys()

#Test the associativity type of a certain token
def isAssociative(token, assoc):
    if not isOperator(token):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token][1] == assoc

#Compare the precedence of two tokens
def cmpPrecedence(token1, token2):
    if not isOperator(token1) or not isOperator(token2):
        raise ValueError('Invalid tokens: %s %s' % (token1, token2))
    return OPERATORS[token1][0] - OPERATORS[token2][0]

#Transforms an infix expression to RPN
def infixToRPN(tokens):
    out = []
    stack = []
    #For all the input tokens [S1] read the next token [S2]
    print("tokens %s"%tokens)

    for token in tokens:
        if isOperator(token):
        # If token is an operator (x) [S3]
            while len(stack) != 0 and isOperator(stack[-1]):
                # [S4]
                if (isAssociative(token, LEFT_ASSOC) and cmpPrecedence(token, stack[-1]) <= 0)  or (isAssociative(token, RIGHT_ASSOC)  and cmpPrecedence(token, stack[-1]) < 0):
                # [S5] [S6]
                    out.append(stack.pop())
                    continue
                break
            # [S7]
            stack.append(token)
        elif token == '(':
            stack.append(token) # [S8]
        elif token == ')':
            # [S9]
            while len(stack) != 0 and stack[-1] != '(':
                out.append(stack.pop()) # [S10]
            stack.pop() # [S11]
        else:
            print("token %s"%token)
            out.append(token) # [S12]
    while len(stack) != 0:
            # [S13]
        out.append(stack.pop())
    return out


class SpaceObjectBase(object):

    def __init__(self):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.mass = None
        self.radius = None

    def get(self, key):
        if key is "position":
            return (self.x, self.y)
        elif key is "velocity":
            return (self.velocity_x, self.velocity_y)
        elif key is "x":
            return self.x
        elif kesy is "y":
            return self.y
    def __repr__(self):
        return "postion=%s velocity=%s mass=%s radius=%s" %(self.position, self.velocity, self.mass, self.radius)
    def __str__(self):
        return "postion=%s velocity=%s mass=%s radius=%s" %(self.position, self.velocity, self.mass, self.radius)
class ConfigParser(object):
    """Docstring for ConfigParser """
    DEFINITIONSKEY = {'mass':'mass', 'position':'distance', "velocity":'velocity'}
    ATTRIBUTESKEY = ('mass', 'position', 'velocity')
    OPERATORS = {'+':lambda x, y:x+y, '-':lambda x, y:x*y, '*': lambda x,y:x*y}
    def __init__(self, filename):
        """@todo: to be defined1 """
        self.filename = filename
        self.config = Config(filename)
        self.definitions = self.config.get_definitions()
        self.solarsystemconf = self.config.get_solarsystem()
        self.definitions['position'] = {}
        self.definitions['position']['center'] = (0,0)
        print self.definitions
        self.system = dict()
    def parse_definitions(self):
       pass
    def parse_solarsystem(self):
        print"solar syste %s" %self.solarsystemconf
        for name, spaceobjectconf in self.solarsystemconf.iteritems():
            spaceobj = SpaceObjectBase()
            for attr in spaceobjectconf.keys():
                if attr in ConfigParser.ATTRIBUTESKEY:
                    value = spaceobjectconf[attr]
                    print "test %s"%value
                    if isinstance(value, str):
                        print "value "+value
                        if value in self.definitions[ConfigParser.DEFINITIONSKEY[attr]]:
                            tmpvalue = self.definitions[ConfigParser.DEFINITIONSKEY[attr]][value]
                        elif value in self.definitions[attr]:
                            tmpvalue = self.definitions[attr][value]
                        else:
                            #TODO: resolev
                            if re.match("\(.+?\,\s.+\)", value):
                                regex = re.search("\((?P<x>.+?)\,\s?(?P<y>.+?)\)", value)
                                tmpvalue = []
                                for value_attr in regex.groups():
                                    tmpvalue.append(self.resovle(value_attr))
                            else:
                                tmpvalue = self.resovle(value)
                    else:
                        try:
                            tmpvalue = float(value)
                        except ValueError:
                            print("Error")
                            return
                    setattr(spaceobj, attr, tmpvalue)
            self.system[name] = spaceobj
            print "System = %s"%self.system
    def resovle(self, stringeq):
        stringeq = stringeq.split(" ")
        print "eq %s" %stringeq
        string = infixToRPN(stringeq)

        print "string %s" %string
        stack =  []
        for item in string:
            if re.match("\w+\.\w+", item):
                item = item.split('.')
                try:
                    # item = self.solarsystem[item[0]].get(item[1])
                    item = getattr(self.system[item[0]], item[1])
                except KeyError:
                    if item[0] in ConfigParser.DEFINITIONSKEY.values():
                        item = self.definitions[item[0]][item[1]]
                stack.append(item)
                print("stack %s" %stack)
            elif item in ConfigParser.OPERATORS:
                try:
                    value1 = stack.pop()
                    value2 = stack.pop()
                    stack.append(ConfigParser.OPERATORS[item](value1, value2))
                except TypeError:
                    if type(value1) is list:
                        listvalue = value1
                        othervalue = value2
                    else:
                        othervalue = value1
                        listvalue = value2
                    newvalue = []
                    for propert in listvalue:
                        newvalue.append(ConfigParser.OPERATORS[item](int(propert), int(othervalue)))
                    stack.append(newvalue)
            else:
                item = float(item)
                stack.append(item)
        return stack.pop()
if __name__ == '__main__':
    conf = ConfigParser('config.yml')
    conf.parse_definitions()
    conf.parse_solarsystem()
