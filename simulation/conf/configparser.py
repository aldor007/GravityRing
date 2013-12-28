""" Module containing functionf for parsing yaml file with 
    position and mass of object in system """


import re
from kivy.logger import Logger
# import logging
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
}

def isOperator(token):
    """check if token in operators dict

    :param token: char.
    :returns: True or False.

    """
    return token in OPERATORS.keys()

def isAssociative(token, assoc):
    """check associative of operator

    :raise: ValueError if token is not operator.
    :return: True or False. """
    if not isOperator(token):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token][1] == assoc

def cmpPrecedence(token1, token2):
    """Comper priorities of operators.

    :param token1: char.
    :param token2: char.
    :raise: ValueError if token isn't operator.
    :returns: number
    """
    if not isOperator(token1) or not isOperator(token2):
        raise ValueError('Invalid tokens: %s %s' % (token1, token2))
    return OPERATORS[token1][0] - OPERATORS[token2][0]

def infixToRPN(tokens):
    """Conver infinix writen statement to revers polish notation

    :param tokens: list of strings.
    :return: list of string in rever polish notation order.
    """
    out = []
    stack = []

    for token in tokens:
        if isOperator(token):
            while len(stack) != 0 and isOperator(stack[-1]):
                if (isAssociative(token, LEFT_ASSOC) and 
                        cmpPrecedence(token, stack[-1]) <= 0)  or (isAssociative(token, RIGHT_ASSOC)
                                and cmpPrecedence(token, stack[-1]) < 0):
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



class ConfigParser(object):
    """Class for parsing yaml configuration file """
    __metaclass__ = Singleton
    DEFINITIONSKEY = {'mass': 'mass', 'x': 'distance', 'y': 'distance', 'position': 'distance', "velocity": 'velocity'}
    ATTRIBUTESKEY = ('mass', 'x', 'y', 'velocity', 'position')
    OPERATORS = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x * y,
            '*': lambda x, y: x * y
            }
    def __init__(self, config):
        """Init method for class

        :param config: config class where is dict to parse."""
        self.config = config
        self.definitions = self.config.get_definitions()
        self.solarsystemconf = self.config.get_solarsystem()
        self.definitions['position'] = {}
        self.definitions['position']['center'] = (400, 400)
        self.system = {}

    def parse(self):
        """Parse configuration for simulation
           convert all knowed attributes to number values.

           :returns: SpaceObject list """
        self.system = {}
        # Logger.debug("read %s" % len(self.solarsystemconf.keys()))
        for name, spaceobjectconf in self.solarsystemconf.iteritems():
            spaceobj = SpaceObject(pos=[0, 0])
            # Logger.debug(" name %s" % name) 
            for attr in spaceobjectconf.keys():
                if attr in ConfigParser.ATTRIBUTESKEY:
                    value = spaceobjectconf[attr]
                    # Logger.debug("value  %s" %value)
                    if isinstance(value, str):
                        try:
                            if value in self.definitions[ConfigParser.DEFINITIONSKEY[attr]]:
                                tmpvalue = self.definitions[ConfigParser.DEFINITIONSKEY[attr]][value]
                            elif value in self.definitions[attr]:
                                tmpvalue = self.definitions[attr][value]
                            else:
                                if re.match(r"\(.+?\,\s.+\)", value):
                                    regex = re.search(r"\((?P<x>.+?)\,\s?(?P<y>.+?)\)", value)
                                    tmpvalue = []
                                    for value_attr in regex.groups():
                                        tmpvalue.append(self.resovle(value_attr))
                                else:
                                    tmpvalue = self.resolve(value)
                        except KeyError:
                            pass
                    else:
                        try:
                            tmpvalue = float(value)
                        except ValueError:
                            print("Error")
                            return
                    try:
                        setattr(spaceobj, attr, tmpvalue)
                    except AttributeError as err:
                        Logger.warning(" error %s %s" % (err, attr))
            spaceobj.name = name
            self.system[name] = spaceobj
            Logger.debug("System = %s"%self.system)
        return self.system.values()

    def resolve(self, stringeq):
        """Resolve math statement
        :param stringeq: string containing equation to calculate
        :return: number, value of equation
        """
        stringeq = stringeq.split(" ")
        string = infixToRPN(stringeq)

        Logger.debug("After RPN string %s" %string)
        stack =  []
        for item in string:
            if re.match(r"\w+\.\w+", item):
                item = item.split('.')
                try:
                    # item = self.solarsystem[item[0]].get(item[1])
                    item = getattr(self.system[item[0]], item[1])
                except KeyError:
                    if item[0] in ConfigParser.DEFINITIONSKEY.values():
                        item = self.definitions[item[0]][item[1]]
                    else:
                        raise Exception
                stack.append(item)
            elif item in ConfigParser.OPERATORS:
                try:
                    value1 = stack.pop()
                    value2 = stack.pop()
                    stack.append(ConfigParser.OPERATORS[item](value1, value2))
                except TypeError:
                    # Logger.debug("IN %s %s   " %(value1, value2))
                    if type(value1) is list or type(value1) is tuple:
                        listvalue = value1
                        othervalue = value2
                        # Logger.debug("IN value  %s %s   " %(listvalue, othervalue))
                    elif type(value2) is list or type(value2) is tuple:
                        othervalue = value1
                        listvalue = value2
                        # Logger.debug("IN  value  %s %s   " %(listvalue, othervalue))
                    newvalue = []
                    try:
                        for propert in listvalue:
                            newvalue.append(ConfigParser.OPERATORS[item](int(propert), int(othervalue)))
                    except UnboundLocalError:
                        for number in range(0, 1):
                            newvalue.append(ConfigParser.OPERATORS[item](int(value1[number]), int(value2[number])))

                    stack.append(newvalue)
            else:
                try:
                    item = float(item)
                except ValueError:
                    pass
                stack.append(item)
        return stack.pop()
