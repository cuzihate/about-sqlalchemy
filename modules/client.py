# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import paramiko
import sys
import os
import socket
import termios
import tty
from paramiko.py3compat import u
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import commons


def posix_shell(chan):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        log = open('handle.log', 'a+', encoding='utf-8')
        flag = False
        temp_list = []
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    if flag:
                        if x.startswith('\r\n'):
                            pass
                        else:
                            temp_list.append(x)
                        flag = False
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                import json

                if len(x) == 0:
                    break

                if x == '\t':
                    flag = True
                else:
                    temp_list.append(x)
                if x == '\r':
                    log.write(''.join(temp_list))
                    log.flush()
                    temp_list.clear()
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

def run():
    current_user = []
    flag = True
    while flag:
        username = input('Username:').strip()
        password = input('Password:').strip()
        ret = commons.session.query(commons.Users.password).filter_by(user_name=username).all()  # like this
        if not ret:
            print('Your Username is wrong!')
            continue
        for item in ret:
            if password in item:
                current_user.append(username)
                print('Welcome to DBMS~')
                break
        if not current_user:
            print('your Password is wrong')
            continue

        ret = commons.session.query(commons.Users).filter_by(user_name=current_user[0]).first()
        curr_hosts_obj = ret.hosts
        if not curr_hosts_obj:
            print('Seemingly that you have no group..')
            continue
        all_group = dict()
        all_group_key = []
        count = 0
        for item in curr_hosts_obj:
            all_group_key.append(item.group[0].group_name)
            all_group[all_group_key[count]] = []
            count += 1

        all_group_key = list(set(all_group_key))

        for item in curr_hosts_obj:
            for content in all_group_key:
                if item.group[0].group_name == content:
                    all_group[content].append(item.ip+':'+str(item.port))

        flag_2 = True
        while flag_2:
            for i in range(len(all_group_key)):
                print('Your group:', all_group_key[i])
            one_group = input('选择查看您所属的主机组：').strip()
            if one_group not in all_group:
                print('Your input not correctly!!')
                continue
            all_hosts = all_group.get(one_group)
            for one_host in all_hosts:
                print('Your hosts:', one_host)

            user_choice = input('Your choice:')
            if user_choice not in all_hosts:
                print('Wrong Again!!')
                continue
            hostname, port = user_choice.strip().split(':')
            tran = paramiko.Transport((hostname, int(port),))
            tran.start_client()
            tran.auth_password(username, password)

            # 打开一个通道
            chan = tran.open_session()
            # 获取一个终端
            chan.get_pty()
            # 激活器
            chan.invoke_shell()

            posix_shell(chan)
            flag = False
            flag_2 = False

            chan.close()
            tran.close()


if __name__ == '__main__':
    run()