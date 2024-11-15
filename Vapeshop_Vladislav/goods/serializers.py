from rest_framework import serializers
from .models import Goods


class GoodsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'