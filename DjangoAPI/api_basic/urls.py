from django.urls import path
from .views import article_list, ArticleAPIView, GenericAPIView

urlpatterns = [
    # path('article/', article_list),
    path('article/', ArticleAPIView.as_view()),
    path('article/<int:id>/', ArticleAPIView.as_view()),
    path('generic/article/<int:id>/', GenericAPIView.as_view()),
    path('generic/article/', GenericAPIView.as_view()),
]
