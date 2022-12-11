import PySimpleGUI as sg
import threading
import time
import socket
import socketio
import uvicorn
import requests
from uvicorn import Config, Server
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)
PORT=8000
window = None
# create a Socket.IO Client
sio_client = socketio.Client(engineio_logger=False, logger=False, ssl_verify=False)

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
    datetime = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    window['-LOG-'].update(datetime + sid + ': ' + data + "\n" + window['-LOG-'].get())
    window.refresh()
    print('message: ', data)

def createWindow(ip):
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [
                [sg.Text('Welcome to PyMessenger!', size=(30, 1), font=("Helvetica", 25))],
                [sg.Text('Send IP address')],
                [sg.Input(key='-IP-')],
                [sg.Text('Send Port')],
                [sg.Input(key='-PORT-')],
                [sg.Text('Enter a message and press send')],
                [sg.Input(key='-IN-')],
                [sg.Button('Send')],
                [sg.Text('Log')],
                [sg.Multiline(key="-LOG-", size=(88, 20), default_text=ip)],
                [sg.Button('Exit')]
            ]

    # Create the Window
    return sg.Window('PyMessenger', layout)

if __name__ == '__main__':
    config = Config(app, host='0.0.0.0', port=PORT, log_level="error", ssl_keyfile="server.key", ssl_certfile="server.crt")
    instance = UvicornServer(config)
    instance.start()

    host = socket.gethostname()
    ip = "Waiting for connection..." + "\n"
    ip = 'Running On: ' + socket.gethostbyname(host) + ":" + str(PORT) +"\n" + ip

    window = createWindow(ip)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            window.close()
            try:
                sio_client.disconnect()
            except:
                pass
            
            instance.stop()
            break

        if event == 'Send':
            # connect to the server
            try:
                sio_client.connect('https://' + values['-IP-'] + ':' + values['-PORT-'])
            except:
                pass
            sio_client.emit('message', values['-IN-'])
            # print(values[0])
            #sio.emit('message', values[0])
            datetime = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
            window['-LOG-'].update(datetime + 'You: ' + values['-IN-'] + "\n" + window['-LOG-'].get())
            window['-IN-'].update('')
            window.refresh()
