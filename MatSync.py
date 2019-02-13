#!pyton
import tkinter as tk
from tkinter import filedialog
import toml
import datetime

class CMatSync:
  dlgDir = ""
  matDataDir = []

  def Run(self):

    carpetDataFilePath = ('')

    iLine = 0 

    with open(carpetDataFilePath) as f:
      for line in f:
        iLine = iLine + 1

        if iLine == 7:
          line = line.strip('\n')
          carpetDateTimeStartStr = line.split(';')[1]

    carpetTimeEnd = float(line.split(';')[0])

    dateTimeFormat = '%d/%m/%Y %H:%M:%S'
    carpetDateTimeStart = datetime.datetime.strptime(carpetDateTimeStartStr, dateTimeFormat)

    epoch = datetime.datetime(1970,1,1)

    carpetEpochTimeStart = (carpetDateTimeStart - epoch).total_seconds()
    carpetEpochTimeEnd = carpetEpochTimeStart + carpetTimeEnd

    print(carpetEpochTimeStart)
    print(carpetEpochTimeEnd)
  
    
  def OpenFile(self):

    root = tk.Tk()
    root.withdraw()

    if len(self.matDataDir) == 0:
      self.filename = tk.filedialog.askopenfilename(
        initialdir=self.dlgDir, title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
      self.selFile = self.filename
    else:
      self.selFile = self.matDataFilePath

if __name__ == "__main__":
    metaWiz = CMatSync()
    metaWiz.Run()