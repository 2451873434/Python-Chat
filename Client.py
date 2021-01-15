import Server_Window
import Client_Window
from PyQt5.QtWidgets import *
import sys
import socket
import threading
import time

class Client_Window(QWidget, Client_Window.Ui_Form):
    def __init__(self):
        super(Client_Window, self).__init__()
        self.setupUi(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.online_peoples = []
        self.server_close = False
        self.connect_success = False
    def set_textbrowser_2(self,str):
        self.textBrowser_2.setText(str)
    def connect(self):
        try:
            self.s.connect((self.lineEdit.text(), int(self.lineEdit_2.text())))
            self.textBrowser.append('<font color =\"#00FF00\">'+'connect success'+ '--time:' + time.ctime() +'</font>')
            self.pushButton.setEnabled(True)
            self.connect_success = True
            self.textBrowser_2.append('<font color =\"#FF0000\">' + self.s.getsockname()[0]+'-'+str(self.s.getsockname()[1])+ '</font>')
            self.online_peoples.append('<font color =\"#FF0000\">' + self.s.getsockname()[0]+'-'+str(self.s.getsockname()[1])+ '</font>')
            threading.Thread(target=self.recv, args=()).start()
        except:
            self.textBrowser.append('no find server')
    def recv(self):
        while True:
            try:
                data0 = self.s.recv(1024)
                try:
                    data = data0.decode('utf-8')
                    if data[0] == 'p':
                        self.textBrowser_2.append(data[1:])
                        self.online_peoples.append(data[1:])
                    elif data[0] == 'l':
                        self.textBrowser.append(data[1:] + 'is disconnected')
                        self.online_peoples.remove(data[1:])
                    else:
                        self.textBrowser.append(data)
                except:
                    data2 = data0.decode('utf-16')
                    self.textBrowser.append('服务器已经关闭')
                    self.online_peoples.clear()
                    self.server_close = True
            except:
                pass
    def lj(self):
        self.textBrowser.append('<font color =\"#00FF00\">' + 'client now connecting...' + '</font>')
        threading.Thread(target=self.connect, args=()).start()
    def send(self):
        try:
            self.s.sendall(self.textEdit.toPlainText().encode('utf-8'))
            sockname = '<font color =\"#FF0000\">' + self.s.getsockname()[0]+'-'+str(self.s.getsockname()[1])+ ':</font>'
            self.textBrowser.append(sockname+self.textEdit.toPlainText())
            self.textEdit.clear()
        except:
            QMessageBox.information('提示', '发送错误', QMessageBox.Yes|QMessageBox.No)
    def shuaxin(self):
        try:
            self.textBrowser_2.clear()
            for online_people in self.online_peoples:
                self.textBrowser_2.append(online_people)
        except:
            pass
    def closeEvent(self, event):
        if not self.server_close:
            if self.connect_success:
                reply = QMessageBox.question(self, '退出程序', "真的要退出程序吗QAQ?", QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.s.sendall(('likai').encode('utf-16'))
                    self.s.close()
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()
        else:
            event.accept()

app = QApplication(sys.argv)
client_window_1 = Client_Window()
client_window_1.setWindowTitle('Client_1')
client_window_2 = Client_Window()
client_window_2.setWindowTitle('Client_2')
client_window_3 = Client_Window()
client_window_3.setWindowTitle('Client_2')
client_window_1.show()
client_window_2.show()
client_window_3.show()
sys.exit(app.exec_())