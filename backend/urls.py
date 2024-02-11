from django.urls import path
from .views import Login,Upload,Signup,EmailVerification,Download,FileList

from . import views

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('upload/', Upload.as_view(), name='file-upload'),
    path('signup/', Signup.as_view(), name='user-signup'),
    path('verify-email/', EmailVerification.as_view(), name='email-verification'),
    path('download/', Download.as_view(), name='download'),
    path('files/', FileList.as_view(), name='file-list'),
]