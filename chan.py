#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paramiko
import sys
import os
import socket
import select
import getpass
from paramiko.py3compat import u
from threading import Thread


def outThread(chan):
    while True:
        # 监视用户输入和服务器返回数据
        # sys.stdin 处理用户输入
        # chan 是之前创建的通道，用于接收服务器返回信息
        readable, writeable, error = select.select([chan, ], [], [], 1)
        if chan in readable:
            try:
                x = u(chan.recv(4096))
                if len(x) == 0:
                    print('\r\n*** EOF\r\n')
                    break
                sys.stdout.write(x)
                sys.stdout.flush()
            except socket.timeout:
                pass

def ssh(username, hostname, password):
    tran = paramiko.Transport((hostname, 22,))
    tran.start_client()
    tran.auth_password(username, password)

    chan = tran.open_session()
    chan.get_pty()
    chan.invoke_shell()
    out = Thread(target=outThread, args=(chan, )).start()

    while True:
        inp = sys.stdin.readline()
        if inp.strip() == "q":
            break
        chan.sendall(inp)

    chan.close()
    tran.close()

if __name__ == "__main__":
    ssh(username="16191051", hostname="10.254.20.154", password="")
