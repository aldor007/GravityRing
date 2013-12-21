import yaml
import re
from collections import OrderedDict
from kivy.logger import Logger
import yaml.constructor
# import logging
from simulation.conf import Config
from utils import Singleton
from simulation.system.solarsystem import SpaceObject

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

LEFT_ASSOC = 0
RIGHT_ASSOC = 1

OPERATORS = {
'+' : (0, LEFT_ASSOC),
'-' : (0, LEFT_ASSOC),
'*' : (5, LEFT_ASSOC),
'/' : (5, LEFT_ASSOC),
'%' : (5, LEFT_ASSOC),
'^' : (10, RIGHT_ASSOC)
}

def isOperator(token):
    """check if token in operators dict"""
    return token in OPERATORS.keys()

def isAssociative(token, assoc):
    if not isOperator(token):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token][1] == assoc

def cmpPrecedence(token1, token2):
    if not isOperator(token1) or not isOperator(token2):
        raise ValueError('Invalid tokens: %s %s' % (token1, token2))
    return OPERATORS[token1][0] - OPERATORS[token2][0]

def infixToRPN(tokens):
    """Conver infinix writen statement to revers polish notation"""
    out = []
    stack = []

    for token in tokens:
        if isOperator(token):
            while len(stack) != 0 and isOperator(stack[-1]):
                if (isAssociative(token, LEFT_ASSOC) and cmpPrecedence(token, stack[-1]) <= 0)  or (isAssociative(token, RIGHT_ASSOC)  and cmpPrecedence(token, stack[-1]) < 0):
                    out.append(stack.pop())
                    continue
                break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while len(stack) != 0 and stack[-1] != '(':
                out.append(stack.pop())
            stack.pop()
        else:
            out.append(token)
    while len(stack) != 0:
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
    """Parsing yaml configuration file """
    __metaclass__ = Singleton
    DEFINITIONSKEY = {'mass': 'mass', 'position': 'distance', "velocity": 'velocity'}
    ATTRIBUTESKEY = ('mass', 'position', 'velocity')
    OPERATORS = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x * y,
            '*': lambda x, y: x * y
            }
    def __init__(self, config):
        self.config = config
        self.definitions = self.config.get_definitions()
        self.solarsystemconf = self.config.get_solarsystem()
        self.definitions['position'] = {}
        self.definitions['position']['center'] = (0, 0)
        self.system = list()

    def parse(self):
        """Parse configuration for simulation 
           convert all knowed attributes to number values
           :return SpaceObject list """
        for name, spaceobjectconf in self.solarsystemconf.iteritems():
            spaceobj = SpaceObject(pos=[0, 0])
            for attr in spaceobjectconf.keys():
                if attr in ConfigParser.ATTRIBUTESKEY:
                    value = spaceobjectconf[attr]
                    Logger.debug("value  %s" %value)
                    if isinstance(value, str):
                        if value in self.definitions[ConfigParser.DEFINITIONSKEY[attr]]:
                            tmpvalue = self.definitions[ConfigParser.DEFINITIONSKEY[attr]][value]
                        elif value in self.definitions[attr]:
                            tmpvalue = self.definitions[attr][value]
                        else:
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
            self.system.append(spaceobj)
            Logger.debug("System = %s"%self.system)
            return self.system

    def resovle(self, stringeq):
        """Resolve math statement"""
        stringeq = stringeq.split(" ")
        string = infixToRPN(stringeq)

        Logger.debug("After RPN string %s" %string)
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
