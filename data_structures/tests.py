import random
import unittest

from data_structures import bst, stack

class TestDataStructures(unittest.TestCase):
    def test_BST(self):
        tree = bst.BST()
        values = (5, 3, 7, 2, 8, 4, 6)

        # Insertion
        for value in values:
            tree.insert(value)

        visit_func = lambda node: node._value

        generator_preorder = tree.traverse_preorder(visit_func)
        self.assertEqual(generator_preorder.next(), 5)
        self.assertEqual(generator_preorder.next(), 3)
        self.assertEqual(generator_preorder.next(), 2)
        self.assertEqual(generator_preorder.next(), 4)
        self.assertEqual(generator_preorder.next(), 7)
        self.assertEqual(generator_preorder.next(), 6)
        self.assertEqual(generator_preorder.next(), 8)

        generator_inorder = tree.traverse_inorder(visit_func)
        self.assertEqual(generator_inorder.next(), 2)
        self.assertEqual(generator_inorder.next(), 3)
        self.assertEqual(generator_inorder.next(), 4)
        self.assertEqual(generator_inorder.next(), 5)
        self.assertEqual(generator_inorder.next(), 6)
        self.assertEqual(generator_inorder.next(), 7)
        self.assertEqual(generator_inorder.next(), 8)

        generator_postorder = tree.traverse_postorder(visit_func)
        self.assertEqual(generator_postorder.next(), 2)
        self.assertEqual(generator_postorder.next(), 4)
        self.assertEqual(generator_postorder.next(), 3)
        self.assertEqual(generator_postorder.next(), 6)
        self.assertEqual(generator_postorder.next(), 8)
        self.assertEqual(generator_postorder.next(), 7)
        self.assertEqual(generator_postorder.next(), 5)

        self.assertFalse(tree.search(1))
        self.assertTrue(tree.search(3))
        self.assertTrue(tree.search(7))
        self.assertFalse(tree.search(9))

    def test_Stack(self):
        stk = stack.Stack()

        self.assertTrue(stk.is_empty())

        items = (9, 1, 8, 2, 7, 3)

        for item in items:
            stk.push(item)

        self.assertFalse(stk.is_empty())

        self.assertEqual(stk.size(), 6)

        self.assertEqual(stk.pop(), 3)

        self.assertEqual(stk.size(), 5)

        self.assertEqual(stk.peek(), 7)

        self.assertEqual(stk.size(), 5)

        self.assertEqual(stk.search(7), 0)    
        self.assertEqual(stk.search(8), 2)    
        self.assertEqual(stk.search(9), 4)
        self.assertEqual(stk.search(5), -1)

if __name__ == '__main__':
    unittest.main()
