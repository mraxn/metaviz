#!pyton
# -*- coding: utf-8 -*-
import csv
import fnmatch
import os
import tkinter as tk
from tkinter import filedialog

import pandas as pd
import toml


class CFileMgr:

    root = []

    mainRecDir = ''

    # 0 - Head, 1 - Neck, 2 - Waist / Knee
    sensorMacs = []
    dlgDir = []
    selFile = ''
    carpetFilePath = ''
    selFileDateTime = []
    recFileList = []
    sensorsRawData = []
    carpetDateTime = ''
    

    def SetDefaultDirs(self):

        cfg = toml.load("cfg.toml")
        self.carpetDataDir = cfg['General']['carpetDataDir']
        self.mainRecDir = cfg['General']['mainRecDir']
        self.sensorMacs = cfg['General']['sensorMacs']

        self.dlgDir = self.mainRecDir + "\\" + self.sensorMacs[0]

        self.sensors_full_paths = list(
            map("\\".join, zip([self.mainRecDir] * 3, self.sensorMacs)))

    def GetCarpetFilePath(self):    
        return self.carpetFilePath

    def GetSensorsData(self):
        return self.sensorsRawData

    def Run(self):
        self.SetDefaultDirs()
        self.selFile = self.OpenFile(self.dlgDir)
        self.carpetFilePath = self.OpenFile(self.carpetDataDir)
        self.CreateFileList(self.sensors_full_paths)
        self.ImportData()

    def OpenFile(self, dlgDir):

        root = tk.Tk()
        root.withdraw()
        fileName = tk.filedialog.askopenfilename(
            initialdir=dlgDir, title="Select file", filetypes=(("csv or txt files", "*.csv; *.txt"), ("all files", "*.*")))
        return fileName

    def CreateFileList(self, sensors_full_paths):

        startStr = "2018"

        dateStartIdx = self.selFile.find(startStr)
        self.selFileDateTime = self.selFile[dateStartIdx:dateStartIdx+23]

        sensors_full_paths = list(
            map("\\".join, zip([self.mainRecDir] * 3, self.sensorMacs)))

        # Taking only one sensor folder - assuming they all have the same recording...

        self.recFileList = []

        for curDir in sensors_full_paths:

            curDirfileList = os.listdir(curDir)

            for filename in curDirfileList:
                if fnmatch.fnmatch(filename, "*" + self.selFileDateTime + "*.csv"):
                    self.recFileList.append(curDir + "\\" + filename)

        if len(self.recFileList) != len(self.sensorMacs):
            # TODO: Do something if not all sensors files exist:
            print('Not all sensors files exist. Please, pick another file...')
        # print(*self.recFileList, sep='\n')

    def ImportData(self):

        self.sensorsRawData = []

        for iFile in self.recFileList:
            self.sensorsRawData.append(pd.read_csv(iFile))