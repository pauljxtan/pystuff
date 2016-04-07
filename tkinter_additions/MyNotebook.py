"""MyNotebook: ttk.Notebook with bells and whistles"""

#import Tkinter as tk
import ttk

class MyNotebook(ttk.Frame): # pylint: disable=too-many-ancestors
    """
    A wrapper around ttk.Notebook that adds more bells and whistles.
    """
    def __init__(self):
        ttk.Frame.__init__(self)
        self._notebook = ttk.Notebook()
        self._notebook.pack()

    def add_tab(self, tab_label, tab_content):
        """
        Adds a new tab to the notebook.

        :param tab_label: Tab label
        :type tab_label: String
        :param tab_content: Stuff to put in the tab (typically a Frame)
        :type tab_content: Tkinter.Widget
        """
        pass
