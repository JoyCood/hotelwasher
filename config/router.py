#!/usr/bin/python 
# -*- coding: utf-8 -*-

#模块映射
model = {
    """ 
     - 格式: {协议前两位:模块名称}
    """
    "10":"member"
}


#处理器
handler = {
        """
         - 格式：{协议:处理函数}
        """
    100000:"login",        
    100001:"register"
}
