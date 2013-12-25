# import pycallgraph TODO
import yaml
import re
from collections import OrderedDict
import yaml.constructor
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

class Config(object):
    __metaclass__ = Singleton
    def __init__(self, filename):
        self.data = OrderedDict()
        self.load(filename)

    def load(self, filename):
        filehandler = open(filename)
        self.data = yaml.load(filehandler, Loader = OrderedDictYAMLLoader)
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
        self.system = dict()
    
    def parse(self):
        for name, spaceobjectconf in self.solarsystemconf.iteritems():
            spaceobj = SpaceObjectBase()
            for attr in spaceobjectconf.keys():
                if attr in ConfigParser.ATTRIBUTESKEY:
                    value = spaceobjectconf[attr]
                    logger.debug("value  %s" %value)
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
                    try:
                        setattr(spaceobj, attr, tmpvalue)
                    except AttributeError as err:
                        Logger.debug(" error %s" % err)
            self.system[name] = spaceobj
            logger.debug("System = %s"%self.system)
    def resovle(self, stringeq):
        stringeq = stringeq.split(" ")
        logger.debug("after split  %s" %stringeq)
        string = infixToRPN(stringeq)

        logger.debug("After RPN string %s" %string)
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
                logger.debug("stack %s" %stack)
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
    conf.parse()
    print("System: %s" % conf.system)
    # conf.parse_solarsystem()
