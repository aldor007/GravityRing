import unittest
from simulation.conf.configparser import isOperator, cmpPrecedence, infixToRPN, isAssociative, LEFT_ASSOC
class RPNTest(unittest.TestCase):
    """Test case docstring"""
    def test_isoperator(self):
        for item in ['+','-','/','*']:
            self.assertTrue(isOperator('+'))
    def test_isAssociative(self):
        self.assertTrue(isAssociative('*', LEFT_ASSOC))
        self.assertRaises(ValueError, isAssociative, 'e', LEFT_ASSOC)
    def test_priorirty(self):
        self.assertEqual(cmpPrecedence('+', '-'), 0)
        self.assertEqual(cmpPrecedence('*', '/'), 0)
        self.assertTrue(cmpPrecedence('*', '-') !=0)
        self.assertRaises(ValueError, cmpPrecedence, 'a','2')
    def test_infixtorpn(self):
        after = ['2','2','+']
        before = ['2', '+', '2']
        ret_val = infixToRPN(before)
        self.assertEqual(after, ret_val)
