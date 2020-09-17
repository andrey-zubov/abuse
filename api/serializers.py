from rest_framework import serializers

class OrgSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField(max_length=120)
    city = serializers.CharField(max_length=120)
    adress = serializers.CharField(max_length=120)
    lat = serializers.CharField(max_length=120)
    lng = serializers.CharField(max_length=120)