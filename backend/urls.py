from django.urls import path
from .views import LoginAPIView,FileUploadView,UserSignupView,EmailVerificationView,FileDownloadView,FileListView

from . import views

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('verify-email/', EmailVerificationView.as_view(), name='email-verification'),
    path('download/', FileDownloadView.as_view(), name='download'),
    path('files/', FileListView.as_view(), name='file-list'),
]