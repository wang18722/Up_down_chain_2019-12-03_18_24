
from rest_framework import serializers

from Users.models import EnterpriseCertificationInfo


class SelfPortraitSerializers(serializers.ModelSerializer):

    class Meta:
        model = EnterpriseCertificationInfo
        fields = ("kind", "lndividual_labels",)

    def update(self, instance, validated_data):
        instance.kind=validated_data['kind']
        instance.lndividual_labels=validated_data['lndividual_labels']
        instance.save()
        return instance