from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Organizations
from .serializers import OrgSerializer


class OrgAPIView(APIView):
    def get(self, request):
        orgs = Organizations.objects.filter()
        serializer = OrgSerializer(orgs, many=True)
        return Response(
            {'orgs': serializer.data}
        )
