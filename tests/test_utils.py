import unittest
from utils import ListBase

class ListBaseTest(unittest.TestCase):
    """Test case docstring"""

    def test_list(self):
        test = ListBase()
        self.assertRaises(NotImplementedError, getattr,test, 'data')
        self.assertRaises(NotImplementedError, setattr,test, 'data','2')
