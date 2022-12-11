# PyMessenger
A simple python script to send messages to your friends on LocalNetwork.

## Requirements
- Python 3.6 or above
- Python modules: `requests`, `socketio`, `PySimpleGUI`

## Usage

```bash
$ openssl genrsa 4096 > server.key
$ openssl req -new -x509 -nodes -sha256 -days 3650 -key server.key > server.crt
```
  
- Run `python3 PyMessenger.py` on your computer.

## Features
- Send messages to your friends on LocalNetwork.

## TODO
- Send files to your friends on LocalNetwork.

## Screenshots
![screenshot](./screenshot.png)

## License
MIT License (c) 2022 Takahashi Akari <akaritakahashioss@gmail.com>