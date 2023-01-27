import tkinter as tk
from src.gui.app import App

if __name__ == '__main__':
    app = App()
    app.geometry('{}x{}'.format(700, 500))
    app.mainloop()
