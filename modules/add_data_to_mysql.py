# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import commons


#  添加主机
commons.session.add_all([
    commons.Hosts(host_name='server_1', ip='172.16.111.131'),
    commons.Hosts(host_name='server_2', ip='172.16.111.132'),
    commons.Hosts(host_name='server_3', ip='172.16.111.133', port='2012'),
    commons.Hosts(host_name='server_4', ip='172.16.111.134'),
    commons.Hosts(host_name='server_5', ip='172.16.111.135', port='2012'),
])


#  添加用户
commons.session.add_all([
    commons.Users(user_name='root', password='123456'),
    commons.Users(user_name='mysql', password='123456'),
    commons.Users(user_name='nginx', password='123456'),
    commons.Users(user_name='zabbix', password='123456'),
])


#  添加主机组
commons.session.add_all([
    commons.Group(group_name='web'),
    commons.Group(group_name='db'),
    commons.Group(group_name='others'),
])


#  主机与主机组对应关系
commons.session.add_all([
    commons.HostsToGroup(hosts_id=1, group_id=1),
    commons.HostsToGroup(hosts_id=2, group_id=1),
    commons.HostsToGroup(hosts_id=3, group_id=1),
    commons.HostsToGroup(hosts_id=4, group_id=2),
    commons.HostsToGroup(hosts_id=5, group_id=3),
])


#  主机与用户对应关系
commons.session.add_all([
    commons.UsersToHosts(hosts_id=1, users_id=1),
    commons.UsersToHosts(hosts_id=2, users_id=1),
    commons.UsersToHosts(hosts_id=3, users_id=1),
    commons.UsersToHosts(hosts_id=4, users_id=3),
    commons.UsersToHosts(hosts_id=5, users_id=4),
])

