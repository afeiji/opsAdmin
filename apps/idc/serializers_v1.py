from rest_framework import serializers
from idc.models import Idc

class Idcserializer(serializers.Serializer):
    id      = serializers.IntegerField(read_only=True)
    name    = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()


    # id      = serializers.IntegerField(read_only=True)
    # name    = serializers.CharField(read_only=False)
    # address = serializers.CharField(read_only=False)
    # phone = serializers.CharField(read_only=False)
    # email = serializers.EmailField(read_only=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.address = validated_data.get("address",instance.address)
        instance.phone = validated_data.get("phone",instance.phone)
        instance.email = validated_data.get("email",instance.email)
        instance.save()
        return instance

    def create(self,validated_data):
        return Idc.objects.create(**validated_data)

