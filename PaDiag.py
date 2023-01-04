import sys
import time

from PyQt5 import QtWidgets, Qt, QtCore, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from constants import *
from power_amplifier import Ui_MainWindow
from socketprog import PaSock

############################################################################################################
class CableHarnessTester(Ui_MainWindow,QtWidgets.QMainWindow,):
    def __init__(self):
        super().__init__()
        self.App = None
        self.PAEnableFlag = False
        #self.global_var_2 =2
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint)

    def Slots_and_Signals(self):
        self.RB_PA1.setChecked(True)
        self.PB_PAEnable.clicked.connect(self.EnablePA)
        self.PB_PADisable.clicked.connect(self.DisablePA)
        self.updateresponsetimer = QTimer()
        self.updateresponsetimer.timeout.connect(self.UpdateData)


        self.PB_PADisable.setDisabled(True)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.App = QtWidgets.QApplication(sys.argv)
        self.App.aboutToQuit.connect(self.Exit)
        self.DefaultFaultCheBoxes()
        self.pixmap = QPixmap('RN Microwave Transperant.png')

        # adding image to label
        self.label_rnlogo.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.label_rnlogo.resize(self.pixmap.width(),
                          self.pixmap.height())

    #########################################################################################################
    def EnablePA(self):
            if self.RB_PA1.isChecked() == True:
                cmd = {'cmd': ENABLE_PA1}
            else:
                cmd = {'cmd': ENABLE_PA2}
            PaCntrl = PaSock()
            if PaCntrl.Paconnect(IP='172.232.50.9', Port=20108) == SUCCESS:
                msg = PaCntrl.sendcmd(cmd=cmd)
                if  msg == SUCCESS:
                    time.sleep(0.1)
                    PaCntrl.close()
                    self.PB_PADisable.setEnabled(True)
                    self.PB_PAEnable.setDisabled(True)
                    self.RB_PA1.setDisabled(True)
                    self.RB_PA2.setDisabled(True)
                    self.PAEnableFlag = True
                    self.updateresponsetimer.start(5000)
                else:
                    QMessageBox.information(self, msg)
            else:
                QMessageBox.information(self, "Disable PA", "PA Connection Failed")
###########################################################################################################
    def DisablePA(self):
        PaCntrl = PaSock()
        if PaCntrl.Paconnect(IP='172.232.50.9', Port=20108) == SUCCESS:
            msg = PaCntrl.sendcmd(cmd={'cmd': DISABLE_PA})
            if msg == SUCCESS:
                time.sleep(0.1)
                PaCntrl.close()
                self.PB_PADisable.setDisabled(True)
                self.PB_PAEnable.setEnabled(True)
                self.RB_PA1.setEnabled(True)
                self.RB_PA2.setEnabled(True)
                self.PAEnableFlag = False
                self.updateresponsetimer.stop()
                self.DefaultFaultCheBoxes()
                self.lineEdit_PA_forwardpower.setText(str('  '))
                self.lineEdit_PA_returnpower.setText(str('   '))
                self.lineEdit_PA_temperature.setText(str('   '))
                self.lineEdit_PA_current.setText(str('   '))
            else:
                QMessageBox.information(self, msg)
        else:
            QMessageBox.information(self, "Disable PA", "PA Connection Failed")

    ###########################################################################################################
    def UpdateData(self):
        if self.RB_PA1.isChecked() == True:
            cmd = {'cmd': GET_STATUS_PA1}
        else:
            cmd = {'cmd': GET_STATUS_PA2}
        PaCntrl = PaSock()
        if PaCntrl.Paconnect(IP='172.232.50.9', Port=20108) == SUCCESS:
            msg = PaCntrl.sendcmd(cmd=cmd)
            if  msg == SUCCESS:
                time.sleep(0.1)
                PaStatus = PaCntrl.receiveresp()
                time.sleep(0.1)
                print(PaStatus)
                self.UpdateFaultCheckBoxes(PaStatus)
                PaCntrl.close()
            else:
                QMessageBox.information(self, msg)
        else:
            QMessageBox.information(self, "Disable PA", "PA Connection Failed")

        if self.RB_PA1.isChecked() == True:
            cmd = {'cmd': GET_DATA_PA1}
        else:
            cmd = {'cmd': GET_DATA_PA2}
        PaCntrl = PaSock()
        if PaCntrl.Paconnect(IP='172.232.50.9', Port=20108) == SUCCESS:
            msg = PaCntrl.sendcmd(cmd=cmd)
            if  msg == SUCCESS:
                time.sleep(0.1)
                PaData = PaCntrl.receiveresp()
                time.sleep(0.1)
                print(PaData)
                self.UpdatePowerData(PaData)
                PaCntrl.close()
            else:
                QMessageBox.information(self, msg)
        else:
            QMessageBox.information(self, "Disable PA", "PA Connection Failed")
    ###########################################################################################################
    def UpdatePowerData(self,PaData = {'VF': 2.13, 'VR': 2.13, 'Temp': 0.0, 'Current': 0.0}):
        self.lineEdit_PA_forwardpower.setText(str(PaData['VF']))
        self.lineEdit_PA_returnpower.setText(str(PaData['VR']))
        self.lineEdit_PA_temperature.setText(str(PaData['Temp']))
        self.lineEdit_PA_current.setText(str(PaData['Current']))
    ###########################################################################################################
    def DefaultFaultCheBoxes(self):
        self.checkBox_2.setStyleSheet("QCheckBox"
                                "{"
                                "padding : 5px;"
                                "}"
                                "QCheckBox::indicator"
                                "{"
                                "border : 2px solid white;"
                                "background-color : rgb(255, 255, 255);"
                                "width : 12px;"
                                "height : 12px;"
                                "border-radius :7px;"
                                "}")
        self.checkBox_3.setStyleSheet("QCheckBox"
                                "{"
                                "padding : 5px;"
                                "}"
                                "QCheckBox::indicator"
                                "{"
                                "border : 2px solid white;"
                                "background-color : rgb(255, 255, 255);"
                                "width : 12px;"
                                "height : 12px;"
                                "border-radius :7px;"
                                "}")
        self.checkBox_4.setStyleSheet("QCheckBox"
                                "{"
                                "padding : 5px;"
                                "}"
                                "QCheckBox::indicator"
                                "{"
                                "border : 2px solid white;"
                                "background-color : rgb(255, 255, 255);"
                                "width : 12px;"
                                "height : 12px;"
                                "border-radius :7px;"
                                "}")
    ###########################################################################################################
    def UpdateFaultCheckBoxes(self,PaStatusFlags={'VSWR': 0, 'THERMAL': 0, 'THERMAL_VSWR': 0}):
        if PaStatusFlags['VSWR'] == 0:
            self.checkBox_2.setStyleSheet("QCheckBox"
                                          "{"
                                          "padding : 5px;"
                                          "}"
                                          "QCheckBox::indicator"
                                          "{"
                                          "border : 2px solid white;"
                                          "background-color : rgb(255, 255, 255);"
                                          "width : 12px;"
                                          "height : 12px;"
                                          "border-radius :7px;"
                                          "}")
        else:
            self.checkBox_2.setStyleSheet("QCheckBox"
                                    "{"

                                    "padding : 5px;"
                                    "}"
                                    "QCheckBox::indicator"
                                    "{"
                                    "border : 2px solid white;"
                                    "background-color : rgb(255, 17, 17);"
                                    "width : 20px;"
                                    "height : 20px;"
                                    "border-radius :12px;"
                                    "}")
        if PaStatusFlags['THERMAL'] == 0:
            self.checkBox_3.setStyleSheet("QCheckBox"
                                          "{"
                                          "padding : 5px;"
                                          "}"
                                          "QCheckBox::indicator"
                                          "{"
                                          "border : 2px solid white;"
                                          "background-color : rgb(255, 255, 255);"
                                          "width : 12px;"
                                          "height : 12px;"
                                          "border-radius :7px;"
                                          "}")
        else:
            self.checkBox_3.setStyleSheet("QCheckBox"
                                    "{"

                                    "padding : 5px;"
                                    "}"
                                    "QCheckBox::indicator"
                                    "{"
                                    "border : 2px solid white;"
                                    "background-color : rgb(255, 17, 17);"
                                    "width : 20px;"
                                    "height : 20px;"
                                    "border-radius :12px;"
                                    "}")
        if PaStatusFlags['THERMAL_VSWR'] == 0:
            self.checkBox_4.setStyleSheet("QCheckBox"
                                          "{"
                                          "padding : 5px;"
                                          "}"
                                          "QCheckBox::indicator"
                                          "{"
                                          "border : 2px solid white;"
                                          "background-color : rgb(255, 255, 255);"
                                          "width : 12px;"
                                          "height : 12px;"
                                          "border-radius :7px;"
                                          "}")
        else:
            self.checkBox_4.setStyleSheet("QCheckBox"
                                    "{"

                                    "padding : 5px;"
                                    "}"
                                    "QCheckBox::indicator"
                                    "{"
                                    "border : 2px solid white;"
                                    "background-color : rgb(255, 17, 17);"
                                    "width : 20px;"
                                    "height : 20px;"
                                    "border-radius :12px;"
                                    "}")
    ###########################################################################################################
    def Exit(self):
        if  self.PAEnableFlag == True:
            self.updateresponsetimer.stop()
            self.DisablePA()
        time.sleep(1)
        self.close()
###########################################################################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # create a main window
    main = QMainWindow()
    main_win = CableHarnessTester()
    main_win.setupUi(main)

    main_win.Slots_and_Signals()
    main.show()
    sys.exit(app.exec_())
#############################################################################################################