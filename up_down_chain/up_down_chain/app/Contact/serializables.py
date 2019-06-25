
from rest_framework import serializers

from Contact.models import AutomateMessagePost, EnterpriseArticlesModel, CommentsOnArticlesModel, ThumbsUpModel


class AiMarketingSerializers(serializers.ModelSerializer):
    """Ai自动营销"""

    class Meta:
        model = AutomateMessagePost

    def create(self, validated_data):
        obj = AutomateMessagePost.objects.create(**validated_data)
        return obj


class TouchArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnterpriseArticlesModel
        fields = "__all__"

class ObtainTouchArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnterpriseArticlesModel
        fields = "__all__"

class CommentsOnArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentsOnArticlesModel
        fields = "__all__"


class ThumbsUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThumbsUpModel
        fields = "__all__"