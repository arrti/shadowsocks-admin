#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from __future__ import absolute_import, division, print_function, \
    with_statement

import socket, os


class config(object):
    manager_address = "/tmp/shadowsocks-multiuser.sock"
    client_address = "/tmp/shadowsocks-admin.sock"


class Shadowsocks():
    def __init__(self):
        pass

    def connect(self):
        try:
            self.cli = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            if os.path.exists(config.client_address):
                os.remove(config.client_address)
            self.cli.bind(config.client_address)  # address of the client
            self.cli.connect(config.manager_address)  # address of Shadowsocks manager
        except Exception as e:
            return False

        return True

    def valid(self):
        self.cli.send(b'ping')
        if self.cli.recv(1506) == b'pong':
            return True
        else:
            return False

    def add_port(self, port, password):
        self.cli.send(b'add: {"server_port":%s, "password":"%s"}' %(port, password))
        if self.cli.recv(1506) == b'ok':
            return True
        else:
            return False

    def remove_port(self, port):
        self.cli.send(b'remove: {"server_port":%s}' % port)
        if self.cli.recv(1506) == b'ok':
            return True
        else:
            return False

    def update_port(self, port, password):
        self.remove_port(port) # maybe the service on this port not start yet
        if self.add_port(port, password):
            return True
        else:
            return False


if __name__ == '__main__':
    pass
