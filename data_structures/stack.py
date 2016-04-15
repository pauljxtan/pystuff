"""Stack: A simple stack."""

class Stack(object):
    """
    A simple stack.
    """
    def __init__(self):
        """
        Initializes an empty stack.
        """
        self._stack = []

    def size(self):
        """
        Returns the number of items on the stack.
        """
        return len(self._stack)

    def push(self, item):
        """
        Pushes the given item onto the stack.
        """
        self._stack.append(item)

    def pop(self):
        """
        Pops an item off the stack.
        """
        return self._stack.pop()

    def peek(self):
        """
        Returns the top item without removing it.
        """
        return self._stack[-1]

    def is_empty(self):
        """
        Returns True if the stack if empty, otherwise returns False.
        """
        return self._stack == []

    def search(self, item):
        """
        Searches for the given item on the stack. If found, returns its
        distance from the top of the stack; otherwise, returns -1.
        """
        for idx in range(self.size()):
            if self._stack[idx] == item:
                return self.size() - idx - 1
        return -1