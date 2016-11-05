# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import commons
from modules import add_data_to_mysql


#  初始化数据库
commons.init_db()

#  添加数据
add_data_to_mysql.commons.session.commit()