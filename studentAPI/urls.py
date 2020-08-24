from django.urls import path
from .views import StudentCRUDCBV


app_name = 'studentAPI'
urlpatterns = [
    #path('api/<int:id>/', StudentCRUDCBV.as_view(), name='student_api'),
    path('api/', StudentCRUDCBV.as_view(), name='student_api'),

    # path('', my_fbv, name='course-list'),

]

