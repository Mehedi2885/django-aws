from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookAPI import views

router = DefaultRouter()

router.register('book', views.BookApiModelViewSet, basename='book')
router.register('bookset', views.BookApiViewSet, basename='bookset')
router.register('bookbulkupdate', views.BookBulkUpdateTry, basename='bookbulkupdate')



urlpatterns = [
    path('', include(router.urls)),
    path('bookList/', views.BookApiViewList.as_view()),
    path('bookbulk/', views.BookBulkUpdateView.as_view()),
    path('bookbulk1/', views.FooView.as_view()),
    # path('bookdemo/id=<int:id>/', views.BookDemo.as_view()),
    path('bookdemo/id=<str:id>/', views.BookDemo.as_view()),
    path('booktry/', views.BookTry.as_view())
]