from PyQt5 import QtCore, QtGui, QtWidgets
import os, re
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
from main import *
import shutil





class Ui_MainWindow(QMainWindow):

    def __init__(self):
        global txt_f
        global lst_key
        global text
        self.value = 0
        
        text = 0
        super().__init__()
        self.setupUi()
        

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(597, 148)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 30, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(280, 30, 231, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 30, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 90, 391, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setAcceptRichText(False)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(430, 90, 111, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(190, 10, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(190, 50, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.ComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.ComboBox.setGeometry(QtCore.QRect(100, 30, 81, 31))
        self.ComboBox.addItems(["ECB", "CBC", "CFB", "OFB"])
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(self.openFile)
        self.pushButton_2.clicked.connect(self.saveFile)
        self.pushButton_3.clicked.connect(self.key_lst_add)
        self.pushButton_4.clicked.connect(self.encrypt)
        self.pushButton_5.clicked.connect(self.decrypt)

        self.retranslateUi()
       

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Safer64bit"))
        self.pushButton.setText(_translate("MainWindow", "Open File"))
        self.pushButton_2.setText(_translate("MainWindow", "Save File"))
        self.pushButton_3.setText(_translate("MainWindow", "Enter Key"))
        self.pushButton_4.setText(_translate("MainWindow", "Encript"))
        self.pushButton_5.setText(_translate("MainWindow", "Decript"))
    
    def key_lst_add(self):
        global key_txt
        key_txt = self.textEdit.toPlainText()   
        ds = len(key_txt)
        self.textEdit.setPlainText("*"*ds) 
        
        self.statusbar.showMessage("key enter")
        
    
    def update_pb(self, value):
        self.progressBar.setValue(value) 
    
    def stat_up(self, value):
        self.statusbar.showMessage(value)
    
    
            
    def encrypt(self):
        try:
            global text
            global key_txt
            tip =  self.ComboBox.currentText()
            self.logic = Logic(self, abasid, key_txt, tip, True)
            self.logic.uppb.connect(self.update_pb)       
            self.logic.start()
            # text = self.logic.shifr_tr(txt_f, lst_key, tip)
            self.statusbar.showMessage("start encrypt file")
            self.logic.sigl.connect(self.stat_up)
        except:
            self.statusbar.showMessage("error")
        
        
    def decrypt(self):
        try:
            global text
            global key_txt
            tip =  self.ComboBox.currentText()
            self.logic = Logic(self, abasid, key_txt, tip, False)
            self.logic.uppb.connect(self.update_pb)       
            self.logic.start()
            # text = self.logic.shifr_tr(txt_f, lst_key, tip)
            self.statusbar.showMessage("start decrypt file")
            self.logic.sigl.connect(self.stat_up)
        except:
            self.statusbar.showMessage("error")
       

    def openFile(self):
        global abasid
        response = QFileDialog.getOpenFileNames()
        if(response != ([], '')):
            abasid = str(response[0])
            abasid = abasid.replace("]", "")
            abasid = abasid.replace("[", "")
            abasid = abasid.replace("'", "")
            self.statusbar.showMessage('open file - ' + abasid)
            
            
       

    def saveFile(self):
        response = QFileDialog.getSaveFileName()
        try:
            if(response != ([], '')):
                abasid = str(response[0])
                abasid = abasid.replace("]", "")
                abasid = abasid.replace("[", "")
                abasid = abasid.replace("'", "")
                print(abasid)
                self.statusbar.showMessage('save to file - ' + abasid)
                to_c = open(abasid, 'wb')
                from_c = open("temp/temp.temp", 'rb')
                shutil.copyfileobj(from_c, to_c)
                
        except:
            print("error")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())
