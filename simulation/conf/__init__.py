""" Module for reading yaml file containing configuration"""
import yaml
import yaml.constructor
from collections import OrderedDict
from utils import Singleton


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
    """Class cointains configuration of system"""
    __metaclass__ = Singleton
    def __init__(self ):
        self.data = OrderedDict()


    def loadfromstring(self, yamlstring):
        """Method load yaml-string and save data in order to data varible

        :param yamlstring: string containing yaml.
        """
        self.data = yaml.load(yamlstring, Loader=OrderedDictYAMLLoader)
        Config.loaded = True

    def get(self, key):
        """ Return specify key value

        :param key: string.
        :returns: value of key.
        """
        return self.data[key]

    def get_definitions(self):
        """ Return: dict containing definitions variables

        :returns: dict.
        """
        return self.data['definitions']

    def get_solarsystem(self):
        """Return dict containing defintions for spaceobject

        :returns: dict
        """
        return self.data['solarsystem']


    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value


