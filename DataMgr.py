
#!pyton
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import toml
import datetime
import pytz

from FilesMgr import CFileMgr


class CSensorData:
    epTime = []
    elTime = []
    pitch = []
    roll = []
    yaw = []


class CDataMgr:

    nSensors = 3
    pitchNorm = [0, 180, 180]
    rollNorm = [0, 90, 90]
    yawNorm = [0, -180, -80]
    sensorsData = []
    sensorsRawData = []
    carpetEpochTimeStart = 0
    carpetEpochTimeEnd = 0
    carpetDataFilePath = ''

    def LoadCfg(self):
        self.cfg = toml.load("cfg.toml")

        self.pitchNorm = self.cfg['General']['pitchNorm']
        self.rollNorm  = self.cfg['General']['rollNorm']
        self.yawNorm   = self.cfg['General']['yawNorm']


    def SetCarpetFilePath(self, carpetFilePath):    
        self.carpetDataFilePath = carpetFilePath
    
    def SetSensorsRawData(self, sensorsRawData):
        self.sensorsRawData = sensorsRawData

    def GetSensorsData(self):
        return self.sensorsData

    def Run(self):
        self.LoadCfg()
        if self.carpetDataFilePath:
            self.GetCarpetTime()
        self.ProcessData()

    def GetCarpetTime(self):

        iLine = 0 

        with open(self.carpetDataFilePath) as f:
          for line in f:
            iLine = iLine + 1

            if iLine == 7:
              line = line.strip('\n')
              carpetDateTimeStartStr = line.split(';')[1]

        carpetTimeEnd = float(line.split(';')[0]) * 1000.0

        dateTimeFormat = '%d/%m/%Y %H:%M:%S'
        carpetDateTimeStart = (datetime.datetime.strptime(carpetDateTimeStartStr, dateTimeFormat)).astimezone(tz=pytz.utc)

        epoch = datetime.datetime(1970,1,1,tzinfo=pytz.utc)

        self.carpetEpochTimeStart = (carpetDateTimeStart - epoch).total_seconds() * 1000.0
        self.carpetEpochTimeEnd = self.carpetEpochTimeStart + carpetTimeEnd

    def ProcessData(self):

        self.sensorsData = []


        for iSensor in range(self.nSensors):
            sensorData = CSensorData()

            if self.carpetDataFilePath:

                carpetSyncIdxStart = (self.sensorsRawData[iSensor]['epoch (ms)'].values > self.carpetEpochTimeStart).argmax()

                syncElValue = self.sensorsRawData[iSensor]['elapsed (s)'].values[carpetSyncIdxStart]

                sensorData.elTime = \
                    self.sensorsRawData[iSensor]['elapsed (s)'].values - syncElValue

            else:
                sensorData.epTime = \
                    self.sensorsRawData[iSensor]['epoch (ms)'].values
                sensorData.elTime = \
                    self.sensorsRawData[iSensor]['elapsed (s)'].values


            sensorData.pitch = \
                self.sensorsRawData[iSensor]['pitch (deg)'].values
            sensorData.roll = \
                self.sensorsRawData[iSensor]['roll (deg)'].values
            sensorData.yaw = \
                self.sensorsRawData[iSensor]['yaw (deg)'].values

            if iSensor == 1:
                sensorData.pitch + self.pitchNorm[1]
                sensorData.roll + self.rollNorm[1]
                sensorData.yaw + self.yawNorm[1]

                sensorData.pitch, sensorData.roll = sensorData.roll, sensorData.pitch

            elif iSensor == 2:
                sensorData.pitch + self.pitchNorm[2]
                sensorData.roll + self.rollNorm[2]
                sensorData.yaw + self.yawNorm[2]

                sensorData.pitch, sensorData.roll = sensorData.roll, sensorData.pitch

            self.sensorsData.append(sensorData)
