"""MyNotebook: ttk.Notebook with bells and whistles"""

import Tkinter as tk
import ttk

class MyNotebook(ttk.Frame): # pylint: disable=too-many-ancestors
    """
    A wrapper around ttk.Notebook that adds more bells and whistles.
    """
    def __init__(self, parent, **kw):
        ttk.Frame.__init__(self, parent)
        self._notebook = ttk.Notebook(self, **kw)
        self._notebook.pack()

        self._index_right_clicked = None

        self._context_menu = self._make_context_menu()
        self._notebook.bind('<Button-3>', self._on_right_click)

    def add_tab(self, tab_content, tab_label, **kw):
        """
        Adds a new tab to the notebook.

        :param tab_content: Stuff to put in the tab (typically a Frame)
        :type tab_content: Tkinter.Widget
        :param tab_label: Tab label
        :type tab_label: String
        """
        self._notebook.add(tab_content, text=tab_label, **kw)

    def _make_context_menu(self):
        menu = tk.Menu(self)
        menu.add_command(label="Close tab", command=self._close_tab)
        return menu

    def _on_right_click(self, event):
        if event.widget.identify(event.x, event.y) == 'label':
            index = event.widget.index('@%d,%d' % (event.x, event.y))
            self._index_right_clicked = index
            self._context_menu.post(event.x_root, event.y_root)

    def _close_tab(self):
        self._notebook.forget(self._index_right_clicked)
        self._index_right_clicked = None

if __name__ == '__main__':
    root = tk.Tk()

    my_notebook = MyNotebook(root)
    my_notebook.pack()

    my_notebook.add_tab(ttk.Label(text="Content"), "label")
    
    root.mainloop()
