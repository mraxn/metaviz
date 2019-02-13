
#!python
import ctypes
import math

import matplotlib
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import toml

from utils import GetScreenSize


class CPlot:

    scrParams          = {}
    sensorsData        = []
    gains              = []
    offsets            = []
    carpetDataFile     = ''
    carpetDateTime     = ''
    carpetDataDir = ''
    


    def SetSensorData(self, sensorsData):
        self.sensorsData = sensorsData

    def Run(self, sensorsData):

        self.sensorsData = sensorsData
        self.gains       = []
        self.offsets     = []
        self.xlim        = []
        self.ylim        = []
        self.xticks      = []
        self.yticks      = []

        self.cfg                = toml.load("cfg.toml")
        self.sensorMacs         = self.cfg['General']['sensorMacs']
        self.figTitles          = self.cfg['General']['figTitles']
        self.vertLinePos        = self.cfg['Figures']['vertLinePos']
        self.vertLineColor      = self.cfg['Figures']['vertLineColor']
        self.lineWidth          = self.cfg['Figures']['lineWidth']
        self.lineColors         = self.cfg['Figures']['lineColors']
        self.groupBy            = self.cfg['Figures']['groupBy']
        self.carpetDataDir = self.cfg['General']['carpetDataDir']

        for ii in range(3):

            cfgFigStr = "Figure%d" % (ii + 1)
            self.gains.append(self.cfg['Figures'][cfgFigStr]['gains'])
            self.offsets.append(self.cfg['Figures'][cfgFigStr]['offsets'])

            self.xlim.append(self.cfg['Figures'][cfgFigStr]['xlim'])
            self.ylim.append(self.cfg['Figures'][cfgFigStr]['ylim'])
            self.xticks.append(self.cfg['Figures'][cfgFigStr]['xticks'])
            self.yticks.append(self.cfg['Figures'][cfgFigStr]['yticks'])

        self.scrParams = GetScreenSize()
        self.Plot()

    def Plot(self):

        pltScrWidthRatio = 3.0/4.0
        pltScrHeightRatio = 1.0/3.0
        xLabel = 'Time (sec)'
        yLabel = 'Angle (deg)'

        plt.close('all')
        plt.switch_backend('wxAgg')

        plt.rcParams['toolbar'] = 'None'
        plt.rcParams['figure.dpi'] = self.scrParams["dpi"]

        figWidth = pltScrWidthRatio * \
            self.scrParams["width"] / self.scrParams["dpi"]
        figHeight = pltScrHeightRatio * \
            self.scrParams["height"] / self.scrParams["dpi"] - 0.5

        f = []
        elTime = []

        if self.groupBy == "SNS":

            titles = self.figTitles
            lgnd1 = ['pitch', 'roll', 'yaw']

            for iSensor in range(3):
                f.append([self.sensorsData[iSensor].pitch.copy(),
                          self.sensorsData[iSensor].roll.copy(),
                          self.sensorsData[iSensor].yaw.copy()])
                elTime.append([self.sensorsData[iSensor].elTime.copy(),
                               self.sensorsData[iSensor].elTime.copy(),
                               self.sensorsData[iSensor].elTime.copy()])
        else:

            lgnd1 = self.sensorMacs
            titles = ['pitch', 'roll', 'yaw']

            f.append([self.sensorsData[0].pitch.copy(),
                      self.sensorsData[1].pitch.copy(),
                      self.sensorsData[2].pitch.copy()])

            f.append([self.sensorsData[0].roll.copy(),
                      self.sensorsData[1].roll.copy(),
                      self.sensorsData[2].roll.copy()])

            f.append([self.sensorsData[0].yaw.copy(),
                      self.sensorsData[1].yaw.copy(),
                      self.sensorsData[2].yaw.copy()])

            elTime.append([self.sensorsData[0].elTime.copy(),
                           self.sensorsData[1].elTime.copy(),
                           self.sensorsData[2].elTime.copy()])
            elTime.append([self.sensorsData[0].elTime.copy(),
                           self.sensorsData[1].elTime.copy(),
                           self.sensorsData[2].elTime.copy()])
            elTime.append([self.sensorsData[0].elTime.copy(),
                           self.sensorsData[1].elTime.copy(),
                           self.sensorsData[2].elTime.copy()])

        for iFigure in range(3):

            plt.figure(iFigure, figsize=(figWidth, figHeight))

            figMgr = plt.get_current_fig_manager()
            figMgr.window.SetPosition(
                (0, self.scrParams["height"] * pltScrHeightRatio * iFigure - iFigure * 15))

            lgnd = []

            for ii in range(3):

                lgnd.append(lgnd1[ii] + ', ' + str(self.gains[iFigure]
                                                   [ii]) + '*x+(' + str(self.offsets[iFigure][ii]) + ')')

            yMax = 180
            yMin = -180

            for iStudy in range(3):
                plt.plot(elTime[iFigure][iStudy],
                         self.gains[iFigure][iStudy] * f[iFigure][iStudy] +
                         self.offsets[iFigure][iStudy],
                         self.lineColors[iStudy], linewidth=self.lineWidth)

            if not isinstance(self.vertLinePos, str):
                plt.plot([self.vertLinePos, self.vertLinePos],
                         [yMin, yMax], self.vertLineColor)

            plt.title(titles[iFigure])
            plt.legend(lgnd)
            plt.xlabel(xLabel)
            plt.ylabel(yLabel)

            if len(self.ylim[iFigure]) == 0:
                plt.ylim(-180, 180)
            else:
                plt.ylim(self.ylim[iFigure])

            # Disabled, was needed to cut into carpet frame lim:
            if 0:

                carpetEndPnt = elTime[0][0][len(elTime[0][0])-1]    

                plt.xlim(0.0, carpetEndPnt)

                if not len(self.xticks[iFigure]) == 0:
                    xS, xSt, xE = self.xticks[iFigure]
                    plt.xticks(np.arange(0, carpetEndPnt, xSt))
            else:
                xS, xSt, xE = self.xticks[iFigure]
                if len(self.xlim[iFigure]) == 0:
                    if xS == xE:
                        endPnt = elTime[0][0][len(elTime[0][0])-1]    
                        plt.xticks(np.arange(elTime[iFigure][0][0], endPnt, xSt))   
                    else:
                        # plt.xlim(self.xlim[iFigure])
                        plt.autoscale(enable=True, axis='x', tight=True)
                else:
                    plt.xlim(self.xlim[iFigure])

                    if not len(self.xticks[iFigure]) == 0:
                        xS, xSt, xE = self.xticks[iFigure]
                        plt.xticks(np.arange(xS, xE, xSt))

            if not len(self.yticks[iFigure]) == 0:
                yS, ySt, yE = self.yticks[iFigure]
                plt.yticks(np.arange(yS, yE, ySt))

            plt.grid()

            plt.tight_layout(pad=0, w_pad=0, h_pad=0)

        mplcursors.cursor(highlight=True)
        # plt.ion()
        plt.show()
