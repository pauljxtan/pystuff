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
        self._tabs = {}

        self._context_menu = self._make_context_menu()
        self._notebook.bind('<Button-3>', self._show_context_menu)

    def add_tab(self, tab_content, tab_label, **kw):
        """
        Adds a new tab to the notebook.

        :param tab_label: Tab label
        :type tab_label: String
        :param tab_content: Stuff to put in the tab (typically a Frame)
        :type tab_content: Tkinter.Widget
        """
        self._notebook.add(tab_content, text=tab_label, **kw)
        self._tabs[self._notebook.index(tab_content)] = tab_content

    def _make_context_menu(self):
        menu = tk.Menu(self)
        menu.add_command(label="Close tab", command=lambda tab_id=self._notebook.select(): self._close_tab(tab_id))
        return menu

    def _show_context_menu(self, event):
        self._context_menu.post(event.x_root, event.y_root)

    def _close_tab(self, tab_id):
        self._notebook.forget(tab_id)

if __name__ == '__main__':
    root = tk.Tk()

    my_notebook = MyNotebook(root)
    my_notebook.pack()

    my_first_tab = ttk.Frame()
    ttk.Label(my_first_tab, text="Hello, world!").pack()
    my_notebook.add_tab(my_first_tab, "An example tab")

    my_second_tab = ttk.Frame()
    my_text = tk.Text(my_second_tab)
    my_text.insert(tk.END, "Some text here")
    my_text.pack()
    my_notebook.add_tab(my_second_tab, "Another example tab")
    
    root.mainloop()
