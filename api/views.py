from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Organizations, Region, Area, City
from .serializers import (
    OrgSerializer,
    RegionSerializer,
    AreaSerializer,
    CitySerializer
)


class OrgAPIView(APIView):
    def get(self, request):
        orgs = Organizations.objects.filter()
        serializer = OrgSerializer(orgs, many=True)
        return Response(
            {'orgs': serializer.data}
        )


class RegionAPI(APIView):
    def get(self, request):
        regions = Region.objects.filter()
        serializer = RegionSerializer(regions, many=True)
        return Response(
            {'regions': serializer.data}
        )


class AreaAPI(APIView):
    def get(self, request):
        areas = Area.objects.filter()
        serializer = RegionSerializer(areas, many=True)
        return Response(
            {'areas': serializer.data}
        )


class CityAPI(APIView):
    def get(self, request):
        cities = City.objects.filter()
        serializer = CitySerializer(cities, many=True)
        return Response(
            {'cities': serializer.data}
        )