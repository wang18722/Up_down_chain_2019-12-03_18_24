class MasterSlaveRouter(object):
    """数据库主从读写分离路由"""

    def db_for_read(self, model, **hints):
        """读数据库"""
        if model._meta.app_label == "Industry":
            return "industry"
        return "default"

    def db_for_write(self, model, **hints):
        """写数据库"""
        if model._meta.app_label == "Industry":
            return  "industry"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return False