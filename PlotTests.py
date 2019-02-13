import unittest
from FilesMgr import CFileMgr
from DataMgr import CDataMgr
from Plot import CPlot


class Test_Plot(unittest.TestCase):

    def test_MethodInTest(self):
        print("Method in test...")


if __name__ == '__main__':
    unittest.main()

# mainRecDir = [
#     "C:\\Users\\Daniel\\Downloads\\MbientLab.43351ABAF8FB0_afn0cdqbtq7je!App\\Devices\\"]

# # 0 - Head, 1 - Neck, 2 - Waist / Knee
# sensorMacs = ["DBDE2962734F", "E662E5A8EC50", "FA985F1353DE"]

# fm.Run()
# sensorsRawData = fm.GetSensorsData()

# dm.SetSensorsRawData(sensorsRawData)
# dm.Run()
# sensorsData = dm.GetSensorsData()

# pl.SetSensorData(sensorsData)
# pl.Run()
