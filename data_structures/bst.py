"BST: Binary search tree"

class BST(object):
    """
    A binary search tree.
    (Essentially a simple wrapper class to encapsulate the root node.)
    """
    def __init__(self, value=None):
        self._root = _BSTNode(value)

    def insert(self, value):
        """
        Inserts a value into the tree.
        """
        self._root._insert(value)

    def traverse_preorder(self, visit_func):
        """
        Traverses the tree in pre-order fashion, applying the given function to
        each node encountered and returning a generator containing the results.
        """
        if self._root._value:
            return self._root._traverse_preorder(visit_func)

    def traverse_inorder(self, visit_func):
        """
        Traverses the tree in in-order fashion, applying the given function to
        each node encountered and returning a generator containing the results.
        """
        if self._root._value:
            return self._root._traverse_inorder(visit_func)

    def traverse_postorder(self, visit_func):
        """
        Traverses the tree in post-order fashion, applying the given function
        to each node encountered and returning a generator containing the
        results.
        """
        if self._root._value:
            return self._root._traverse_postorder(visit_func)

    def search(self, value):
        """
        Searches the tree for the given value, and returns True if the value is
        found; otherwise, returns False.
        """
        if self._root._value:
            return self._root._search(value)

class _BSTNode(object):
    """
    A node in a binary search tree.
    """
    def __init__(self, value):
        self._value = value
        # Left child
        self._left = None
        # Right child
        self._right = None

    def _insert(self, value):
        """
        Inserts a value into the tree rooted by this node.
        """
        # If current node has no value, simply set it on this node
        if not self._value:
            self._value = value
            return
        
        if self._value == value:
            raise ValueError("Value (%d) already in tree" % value)

        # Go down the left subtree
        if value < self._value:
            # If node exists, recursively insert value on left subtree
            if self._left:
                self._left._insert(value)
            # Otherwise, create new node and add as left child
            else:
                self._left = _BSTNode(value)
                return

        # Go down the right subtree
        if value > self._value:
            # If node exists, recursively insert value on right subtree
            if self._right:
                self._right._insert(value)
            # Otherwise, create new node and add as right child
            else:
                self._right = _BSTNode(value)
                return

    def _search(self, value):
        """
        Searches the tree rooted by this node for the given value, and returns
        True if the value is found; otherwise, returns False.
        """
        if not self._value:
            # Not found
            return False

        if value < self._value:
            if not self._left:
                # Not found
                return False
            # Search the left subtree
            return self._left._search(value)

        if value > self._value:
            if not self._right:
                # Not found
                return False
            # Search the left subtree
            return self._right._search(value)
           
        # Found
        return True

    def _traverse_preorder(self, visit_func):
        """
        Traverses the tree rooted by this node in pre-order fashion, applying
        the given function to each node encountered and yielding the result.
        """
        if self._value:
            yield visit_func(self)
        if self._left:
            for result in self._left._traverse_preorder(visit_func):
                yield result
        if self._right:
            for result in self._right._traverse_preorder(visit_func):
                yield result

    def _traverse_inorder(self, visit_func):
        """
        Traverses the tree rooted by this node in in-order fashion, applying
        the given function to each node encountered and yielding the result.
        """
        if self._left:
            for result in self._left._traverse_inorder(visit_func):
                yield result
        if self._value:
            yield visit_func(self)
        if self._right:
            for result in self._right._traverse_inorder(visit_func):
                yield result

    def _traverse_postorder(self, visit_func):
        """
        Traverses the tree rooted by this node in post-order fashion, applying
        the given function to each node encountered and yielding the result.
        """
        if self._left:
            for result in self._left._traverse_postorder(visit_func):
                yield result
        if self._right:
            for result in self._right._traverse_postorder(visit_func):
                yield result
        if self._value:
            yield visit_func(self)