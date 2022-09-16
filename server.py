from PyQt5 import QtCore, QtWebSockets, QtNetwork, QtWidgets


class MyServer(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.clients = []
        self.server = QtWebSockets.QWebSocketServer(parent.serverName(), parent.secureMode(), parent)
        if self.server.listen(QtNetwork.QHostAddress.LocalHost, 1302):
            print('Connected: ' + self.server.serverName() + ' : ' + self.server.serverAddress().toString() + ':' + str(
                self.server.serverPort()))
        else:
            print('error')
        self.server.newConnection.connect(self.onNewConnection)

        print(self.server.isListening())

    def onNewConnection(self):
        clientConnection = self.server.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)
        print(self.sender())
        print("inside")
        clientConnection.textMessageReceived.connect(self.processTextMessage)
        clientConnection.binaryMessageReceived.connect(self.processBinaryMessage)
        self.server.disconnected.connect(self.socketDisconnected)

    def processTextMessage(self, message):
        if (self.clientConnection):
            self.clientConnection.sendTextMessage(message)

    def processBinaryMessage(self, message):
        if (self.clientConnection):
            self.clientConnection.sendBinaryMessage(message)

    def socketDisconnected(self):
        if (self.clientConnection):
            self.clients.remove(self.clientConnection)
            self.clientConnection.deleteLater()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    serverObject = QtWebSockets.QWebSocketServer('My Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = MyServer(serverObject)
    serverObject.closed.connect(app.quit)
    app.exec_()
