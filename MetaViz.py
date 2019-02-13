#!pyton
import re
import tkinter as tk
from multiprocessing import Process
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font

import toml

from DataMgr import CDataMgr
from FilesMgr import CFileMgr
from Plot import CPlot
from utils import GetScreenSize


class CMetaViz:

    scrParams = {}
    sensorsData = []
    proc = Process()

    def Run(self):
        self.CreateGUI()

    def CreateRunButton(self):

        self.root1 = tk.Tk()

        self.scrParams = GetScreenSize()
        gW = 1/4 * self.scrParams['width']
        gH = 1/8 * self.scrParams['height']
        gX = 3/4 * self.scrParams['width']
        gY = 0

        self.root1.title("Visualize Sensors Data")
        self.root1.geometry('%dx%d+%d+%d' % (gW, gH, gX, gY))

        myFont = font.Font(family='Helvetica', size=20, weight=font.BOLD)

        self.playImg = tk.PhotoImage(file="resources\\play-button.png")
        self.replayImg = tk.PhotoImage(file="resources\\replay-button.png")

        self.btn1 = tk.Button(self.root1, image=self.playImg, command=self.RunBtnCallback,
                              height=85, width=175, compound=tk.CENTER, bg="green", font=myFont)
        self.btn2 = tk.Button(self.root1, image=self.replayImg, command=self.RerunBtnCallback,
                              height=85, width=175, compound=tk.CENTER, bg="#7f7f00", font=myFont)

        self.btn2['state'] = 'disabled'

        self.btn1.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        self.btn2.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

    def RunBtnCallback(self):

        # LoadCfg()
        fm = CFileMgr()
        dm = CDataMgr()
        pl = CPlot()

        fm.Run()
        sensorsRawData = fm.GetSensorsData()
        
        dm.SetCarpetFilePath(fm.GetCarpetFilePath())
        dm.SetSensorsRawData(sensorsRawData)
        dm.Run()
        self.sensorsData = dm.GetSensorsData()

        # pl.Run(self.sensorsData)

        if self.proc.name == 'Plot':
            self.proc.kill()
        self.proc = Process(name='Plot', target=pl.Run,
                            args=(self.sensorsData,))
        self.proc.start()

        self.btn2['state'] = 'normal'

    def RerunBtnCallback(self):

        pl = CPlot()

        if self.proc.name == 'Plot':
            self.proc.kill()
        self.proc = Process(name='Plot', target=pl.Run,
                            args=(self.sensorsData,))
        self.proc.start()

    def CreateCfgEditor(self):

        self.cfg = toml.load("app_cfg.toml")

        appCfgFile = open(self.cfg["cfgFilePath"], 'r')
        appCfgTxt = appCfgFile.read()
        appCfgFile.close()

        gW = 0.25 * self.scrParams['width']
        gH = 0.875 * self.scrParams['height'] - 105
        gX = 0.75 * self.scrParams['width']
        gY = 0.125 * self.scrParams['height'] + 32
        self.root2 = tk.Tk()
        self.txt = ScrolledText(self.root2, width=80, height=80, undo=True)
        # self.txt.insert(tk.END, appCfgTxt)
        
        self.root2.bind_all("<Control-s>", self.CfgEditorSave)
        self.txt.bind('<Key>', self.TxtModifiedCallback)
        self.txt.bind('<Control-z>', self.UndoCallback)

        self.txt.tag_configure("Comment", foreground="#B27300")
        self.txt.tag_configure("RegularText", foreground="#000000")
        self.txt.tag_configure("Tags", foreground="#0000FF")

        self.ApplySyntaxHl(appCfgTxt)

        # self.txt.tag_configure("Token.Comment", foreground="#b21111")

        self.root2.title("CFG Editor")
        self.root2.geometry('%dx%d+%d+%d' % (gW, gH, gX, gY))

        self.txt.pack()

    def ApplySyntaxHl(self, appCfgTxt):
        appCfgTxtLines = appCfgTxt.split('\n')

        for cfgLine in appCfgTxtLines:
            if re.search('^\\s*\\#', cfgLine, re.VERBOSE):
                self.txt.insert("end", cfgLine, 'Comment')
            elif re.search('^\\s*\\[', cfgLine, re.VERBOSE):
                self.txt.insert("end", cfgLine, 'Tags')
            else:
                self.txt.insert("end", cfgLine, 'RegularText')
            self.txt.insert("end", '\n', 'RegularText')

    def TxtModifiedCallback(self, event):
      # Save combination pressed:
      if event.keycode != 17:
        self.root2.title("CFG Editor*")

    def UndoCallback(self, *args):
      self.ApplySyntaxHl(self.txt.get("1.0", "end"))

    def CfgEditorSave(self, *args):
        txt = self.txt.get("1.0", "end")
        filename = self.cfg["cfgFilePath"]

        with open(filename, 'w') as f:
            f.write(txt)
        f.close()

        self.root2.title("CFG Editor")


        # messagebox.showinfo("Save", "CFG file saved...")

    def CreateGUI(self):
        self.CreateRunButton()
        self.CreateCfgEditor()
        self.root1.mainloop()


if __name__ == "__main__":
    sdv = CMetaViz()
    sdv.Run()
