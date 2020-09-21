from rest_framework import serializers

class OrgSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField(max_length=120)
    city = serializers.CharField(max_length=120)
    adress = serializers.CharField(max_length=120)
    lat = serializers.CharField(max_length=120)
    lng = serializers.CharField(max_length=120)


class RegionSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField(max_length=256)


class AreaSerializer(serializers.Serializer):
    id = serializers.CharField()
    region = serializers.CharField(max_length=256)
    title = serializers.CharField(max_length=256)


class CitySerializer(serializers.Serializer):
    id = serializers.CharField()
    area = serializers.CharField(max_length=256)
    title = serializers.CharField(max_length=256)


