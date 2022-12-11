import PySimpleGUI as sg
import threading
import time
import socketio
import uvicorn
import requests
import multiprocessing
from uvicorn import Config, Server
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

class UvicornServer(threading.Thread):
    def __init__(self, config: Config):
        super().__init__()
        self.server = Server(config=config)
        self.config = config

    def stop(self):
        self.server.should_exit = True

    def run(self, *args, **kwargs):
        self.server.run()


# create a Socket.IO server
sio = socketio.AsyncServer(engineio_logger=False, logger=False, async_mode='asgi')

# create an ASGI application
app = socketio.ASGIApp(sio)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# receive a message from a client
@sio.event
def message(sid, data):
    print('message: ', data)

def createWindow():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('Enter a message and press send')],
                [sg.Input(key='-IN-')],
                [sg.Button('Send'), sg.Button('Exit')] ]

    # Create the Window
    return sg.Window('PyMessenger', layout)

if __name__ == '__main__':
    config = Config(app, host='0.0.0.0', port=8000, log_level="info", ssl_keyfile="server.key", ssl_certfile="server.crt")
    instance = UvicornServer(config)
    instance.start()

    window = createWindow()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            window.close()
            instance.stop()
            break

        if event == 'Send':
            # print(values[0])
            sio.emit('message', values[0])
            window['-IN-'].update('')
            window.refresh()
