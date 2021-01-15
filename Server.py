import Server_Window
import Client_Window
from PyQt5.QtWidgets import *
import sys
import socket
import threading
import time


class Server_Window(QWidget, Server_Window.Ui_Form):
    def __init__(self):
        super(Server_Window, self).__init__()
        self.setupUi(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conns = []
        self.addrs = []
        self.online_peoples = []
    def listen(self):
        while True:
            try:
                self.s.listen(10)
                self.textBrowser.append('<font color =\"#00FF00\">' + 'server now listening...' + '</font>')
                self.pushButton_2.setEnabled(False)
                conn, addr = self.s.accept()
                self.conns.append(conn)
                self.addrs.append(addr)
                self.textBrowser.append('<font color =\"#00FF00\">' +conn.getpeername()[0]+'-'+str(conn.getpeername()[1])+ 'connect success' + '--connect time:' + time.ctime() + '</font>')
                self.online_peoples.append(conn.getpeername()[0]+'-'+str(conn.getpeername()[1]))
                self.pushButton.setEnabled(True)
                self.send_people(conn)
                threading.Thread(target=self.recv, args=()).start()
            except:
                self.textBrowser.append('can\'t listen this ip and port')
    def recv_threading(self,conn):
        while True:
            try:
                data0 = conn.recv(1024)
                try:
                    data = data0.decode('utf-8')
                    peername = '<font color =\"#0000FF\">' + conn.getpeername()[0] + '-' + str(
                        conn.getpeername()[1]) + ':</font>'
                    str_conbine = peername  + data
                    self.textBrowser.append(str_conbine)
                    self.send_other(conn, str_conbine)
                except:
                    data2 = data0.decode('utf-16')
                    peername = conn.getpeername()[0] + '-' + str(
                        conn.getpeername()[1])
                    self.textBrowser.append(peername + 'is disconnected')
                    self.online_peoples.remove(peername)
                    del self.addrs[self.conns.index(conn)]
                    self.conns.remove(conn)
                    self.send_other(conn, 'l' + peername)
            except:
                pass
    def recv(self):
        for conn in self.conns:
            threading.Thread(target=self.recv_threading, args=(conn,)).start()
    def ksjt(self):
        self.s.bind((self.lineEdit.text(), int(self.lineEdit_2.text())))
        self.textBrowser.append('<font color =\"#00FF00\">'+'bind ok'+'</font>')
        threading.Thread(target=self.listen, args=()).start()
    def send_other(self, conn_, str_conbine):
        for conn in self.conns:
            if conn != conn_:
                conn.sendall(str_conbine.encode('utf-8'))
    def send_people(self, conn_):
        for conn in self.conns:
            if conn != conn_:
                conn.sendall(('p' + conn_.getpeername()[0]+'-'+str(conn_.getpeername()[1])).encode('utf-8'))
            else:
                if self.textBrowser_2.toPlainText() != '':
                    conn.sendall(('p' + self.textBrowser_2.toPlainText()).encode('utf-8'))
        self.textBrowser_2.append(conn_.getpeername()[0] + '-' + str(conn_.getpeername()[1]))
    def send(self):
        for conn in self.conns:
            sockname = '<font color =\"#0000FF\">' + conn.getsockname()[0] + '-' + str(
                conn.getsockname()[1]) + ':</font>'
            conn.sendall((sockname + self.textEdit.toPlainText()).encode('utf-8'))
        sockname = '<font color =\"#FF0000\">' + conn.getsockname()[0] + '-' + str(
                conn.getsockname()[1]) + ':</font>'
        self.textBrowser.append(sockname + self.textEdit.toPlainText())
        self.textEdit.clear()
    def shuaxin(self):
        try:
            self.textBrowser_2.clear()
            for online_people in self.online_peoples:
                self.textBrowser_2.append(online_people)
        except:
            pass
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出程序', "真的要退出程序吗QAQ?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            for conn in self.conns:
                conn.sendall('c'.encode('utf-16'))
            self.s.close()
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server_window = Server_Window()
    server_window.show()
    sys.exit(app.exec_())