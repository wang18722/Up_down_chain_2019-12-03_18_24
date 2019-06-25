from haystack import indexes

from .models import Bids


class BidsIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Bids索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    id = indexes.IntegerField(model_attr='id',)
    Title = indexes.CharField(model_attr='Title',null=True)
    BidsPirce = indexes.CharField(model_attr='BidsPirce',null=True)
    Company = indexes.CharField(model_attr='Company',null=True)
    BidsAreaID = indexes.CharField(model_attr='BidsAreaID',null=True)
    Url = indexes.CharField(model_attr='Url',null=True)
    Source = indexes.CharField(model_attr='Source',null=True)
    IsValid = indexes.IntegerField(model_attr='IsValid',null=True)
    IsDeleted = indexes.IntegerField(model_attr='IsDeleted',null=True)
    ReleaseDate = indexes.CharField(model_attr='ReleaseDate',null=True)
    EndDate = indexes.DateField(model_attr='EndDate',null=True)
    StartDate = indexes.CharField(model_attr='StartDate',null=True)
    CreateTime = indexes.DateField(model_attr='CreateTime',null=True)
    BidsContent = indexes.MultiValueField(model_attr='BidsContent',null=True)
    Phone = indexes.CharField(model_attr="Phone",null=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return Bids

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.all()


# class BidsContentIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#
#     # ID = indexes.CharField(model_attr='ID',unique=True,primary_key=True)
#     BidsContent = indexes.CharField(model_attr='BidsContent',null=True)
#
#     def get_model(self):
#         """返回建立索引的模型类"""
#         return BidsContent
#
#     def index_queryset(self, using=None):
#         """返回要建立索引的数据查询集"""
#         return self.get_model().objects.all()