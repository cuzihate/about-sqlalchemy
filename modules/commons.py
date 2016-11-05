# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

Base = declarative_base()


class HostsToGroup(Base):
    __tablename__ = 'hosts_to_group'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    hosts_id = Column(Integer, ForeignKey('hosts.nid'))
    group_id = Column(Integer, ForeignKey('group.nid'))


class UsersToHosts(Base):
    __tablename__ = 'users_to_hosts'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    users_id = Column(Integer, ForeignKey('users.nid'))
    hosts_id = Column(Integer, ForeignKey('hosts.nid'))


class Hosts(Base):
    __tablename__ = 'hosts'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    host_name = Column(String(32), unique=True, nullable=False)
    ip = Column(String(32), unique=True, nullable=False)
    port = Column(Integer, default=22)
    group = relationship('Group', secondary=HostsToGroup.__table__, backref='hosts')
    users = relationship('Users', secondary=UsersToHosts.__table__, backref='hosts')


class Group(Base):
    __tablename__ = 'group'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(32), default='default_group')


class Users(Base):
    __tablename__ = 'users'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(32), unique=True, nullable=False)
    password = Column(String(32), nullable=False)


engine = create_engine(settings.CONN, max_overflow=5)


#  数据库初始化
def init_db():
    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()




# ret = session.query(Users).all()
# print(ret)