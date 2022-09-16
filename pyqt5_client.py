import sys

from PyQt5 import QtWebSockets
from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtWidgets import QApplication


class Client(QObject):
    def __init__(self, parent):
        super().__init__(parent)

        self.client = QtWebSockets.QWebSocket("", QtWebSockets.QWebSocketProtocol.Version13, None)
        # self.client.error.connect(self.error)

        self.client.textMessageReceived.connect(self.on_text_msg_received)

        self.client.open(QUrl("ws://127.0.0.1:8000/ws/pyqt5_client"))

        print('client should be connected now.')

    def on_text_msg_received(self, message):

        print(f'client received the message: {message}')

    def close(self):
        print('closing client')
        self.client.close()

    def change_page_within_gui(self, page_number):
        # Change the page pseudocode for now
        print(f'Page number has been changed from 0 to {str(page_number)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client(app)
    app.exec_()
