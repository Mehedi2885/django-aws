from django.urls import path
from .views import UserCreateRegister, UserLoginCBV, UserLogout

app_name = 'accounts'
urlpatterns = [
    path('', UserCreateRegister.as_view(), name='user-register'),
    path('login/', UserLoginCBV.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    # path('api/', StudentCRUDCBV.as_view(), name='student_api'),

    # path('', my_fbv, name='course-list'),

]
