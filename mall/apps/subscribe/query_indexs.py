from haystack import indexes
from .models import Bids

class BidsIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Bids索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)

    id = indexes.IntegerField(model_attr='id')
    pirce = indexes.DecimalField(model_attr='pirce')
    company = indexes.CharField(model_attr='company')
    title = indexes.CharField(model_attr='title')
    url = indexes.CharField(model_attr='url')
    source = indexes.CharField(model_attr='source')
    areas_id = indexes.IntegerField(model_attr='areas_id')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        """返回建立索引的模型类"""
        return Bids

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.all()