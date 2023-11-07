# Overview

This server attempts to capture requests that are intended for a fortiauthenticator. It will capture and store sensitive information from the requests and provides a web interface to view the information. By default the server will authorize every login request. Run the server will --block_logins to block all logins instead.

## Requirements

Python 3.9 or higher
A way to route fortiauthenticator requets to the server

## Usage

Run server to capture and allow all auth requests
`python main.py`

Run server to capture and deny all auth requests
`python main.py --block_logins`

Visit https://127.0.0.1/ui to view the captured requests. Refresh the page to see new requests.

By default the server uses a self signed cert stored in the certs folder. You can replace this with a trusted cert if you have access to one.

## Installation Windows

Optionally setup a python virtual environment and activate it
`python -m venv venv`
`venv\Scripts\activate`

install dependencies
`pip install -r requirements.txt`

## Installation Linux

On linux you need to be running as root to listen on port 443. The simples way to do this is to launch a new shell as root with `sudo su` and then run the commands below.

Optionally setup a python virtual environment and activate it
`python3 -m venv venv`
`source venv/bin/activate`

install dependencies
`pip3 install -r requirements.txt`
