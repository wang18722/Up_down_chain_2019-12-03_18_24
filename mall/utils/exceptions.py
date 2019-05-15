from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

# 获取在配置文件中定义的logger，用来记录日志
logger = logging.getLogger('Distribution')

def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response


"""
├── front   静态文件
└── mall    项目根
    ├── apps    应用
    │   ├── areas   地区
    │   ├── curriculum  课程
    │   ├── order   订单
    │   ├── pay 支付
    │   ├── school  学校
    │   ├── store   门店
    │   ├── user    用户
    │   ├── verification    验证
    │   └── oauth    授权
    ├── dump.rdb
    ├── libs    第三方库
    ├── logs    日志
    ├── mall    主应用
    ├── manage.py   应用启动文件
    ├── scripts     脚本
    └── utils   工具包
"""
