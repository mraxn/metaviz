import os
import math
import tkinter as tk


def GetScreenSize():

    root = tk.Tk()
    root.withdraw()
    scrWidth = root.winfo_screenwidth()
    scrHeight = root.winfo_screenheight()
    scrInWidth = root.winfo_screenmmwidth() / 25.4
    scrInHeight = root.winfo_screenmmheight() / 25.4
    scrSize = math.sqrt(scrInWidth ** 2 + scrInHeight ** 2)

    scrDpi = (math.sqrt(scrWidth ** 2 + scrHeight ** 2)) / scrSize
    scrParams = {"width": scrWidth,
                 "height": scrHeight,
                 "dpi": scrDpi,
                 "scrSize": scrSize}
    return scrParams
