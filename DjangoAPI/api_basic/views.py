from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser, FileUploadParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# for class based APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# generic view
from rest_framework import generics
from rest_framework import mixins

from .models import Article
from .serializers import ArticleSerializer


# Create your views here.

# Generic class view
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)

# class basic view
class ArticleAPIView(APIView):

    # lookup_field = 'id'

    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id=None):

        if id:
            article = self.get_object(id)
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # work with file
    class FileUploadView(APIView):
        parser_classes = (FileUploadParser,)

        def post(self, request, format='jpg'):
            up_file = request.FILES['file']
            destination = open('/Users/Username/' + up_file.name, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            destination.close()  # File should be closed only after all chuns are added

            # ...
            # do some stuff with uploaded file
            # ...
            return Response(up_file.name, status.HTTP_201_CREATED)


# basic view
@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
