from haystack import indexes
from .models import *

class ANlmyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    ANlmy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved',null=True)
    province = indexes.CharField(model_attr='province',null=True)
    phone = indexes.CharField(model_attr='phone',null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)




    def get_model(self):
        """返回建立索引的模型类"""
        return ANlmy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""

        return self.get_model().objects.filter()


class BCkyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    BCky索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.CharField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    company_nameid = indexes.CharField(model_attr='company_name',null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return BCky

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()

class CZzyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    CZzy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    company_name = indexes.CharField(model_attr='company_name', null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return CZzy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()


class DDrrsgyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    DDrrsgy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return DDrrsgy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()

class EJzyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    EJzy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return EJzy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()

class FPflsyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    FPflsy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return FPflsy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class GJcyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    GJcy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return GJcy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class HZscyyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    HZscyy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)


    def get_model(self):
        """返回建立索引的模型类"""
        return HZscyy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class IXxrjyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    ANlmy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return IXxrjy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class JJryIndex(indexes.SearchIndex, indexes.Indexable):
    """
    JJry索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return JJry

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class KFdcyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    KFdcy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return KFdcy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()

class LZlswIndex(indexes.SearchIndex, indexes.Indexable):
    """
    ANlmy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return LZlsw

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class MKyjsIndex(indexes.SearchIndex, indexes.Indexable):
    """
    MKyjs索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    company_name = indexes.CharField(model_attr='company_name',null=True)
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return MKyjs

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class NSlhjggIndex(indexes.SearchIndex, indexes.Indexable):
    """
    NSlhjgg索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return NSlhjgg

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class OJmxlIndex(indexes.SearchIndex, indexes.Indexable):
    """
    OJmxl索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return OJmxl

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class PJyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    PJy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return PJy

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()
class QWsshIndex(indexes.SearchIndex, indexes.Indexable):
    """
    ANlmy索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return QWssh

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()

class RWtyIndex(indexes.SearchIndex, indexes.Indexable):
    """
    RWty索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return RWty

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()

class SGgshIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SGgsh索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)


    company_name = indexes.CharField(model_attr='company_name',null=True)
    industry_involved = indexes.CharField(model_attr='industry_involved', null=True)
    province = indexes.CharField(model_attr='province', null=True)
    phone = indexes.CharField(model_attr='phone', null=True)
    company_id = indexes.CharField(model_attr='company_id')
    id = indexes.IntegerField(model_attr='id')
    industriesid = indexes.CharField(model_attr='industriesid', null=True)



    def get_model(self):
        """返回建立索引的模型类"""
        return SGgsh

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter()