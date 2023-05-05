from .models import Message, Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response as apires
from django.shortcuts import render

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView


class MessageViewSet(viewsets.ViewSet):
    pass

class ResponseViewSet(viewsets.ViewSet):
    pass

class PageViewSet(viewsets.ViewSet):
    pass


class Home(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
