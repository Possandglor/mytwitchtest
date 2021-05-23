# coding: utf-8
import socket
import Ui_Form1
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

HOST = "irc.twitch.tv"
PORT = 6667
NICK = 'barbar_bot'
PASS = 'oauth:sg8p20t7nodc9j161lh8szlzkb95q6'
CHANNEL = 'skorpak'

s = socket.socket()
def send_message(message):
    s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n","UTF-8"))

    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n","UTF-8"))
    s.send(bytes("NICK " + NICK + "\r\n","UTF-8"))
    s.send(bytes("JOIN #" + CHANNEL+" \r\n","UTF-8"))

    while True:
        st = input()
        send_message(st)

class ExampleApp(QtWidgets.QMainWindow, Ui_Form1.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна


# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Show the calculator's GUI
    view = ExampleApp()
    view.show()
    # Create instances of the model and the controller
    app.exec()
    # Execute calculator's main loop
    #sys.exit(pycalc.exec_())

main()