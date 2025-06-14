from django.urls import path
from .views import current_user, LoginView, RegisterAdminView, AdminAccessRequestView, AdminAccessApprovalView

urlpatterns = [
    path('me/', current_user, name='current_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('register-admin/', RegisterAdminView.as_view(), name='register-admin'),
    path('request-admin/', AdminAccessRequestView.as_view(), name='request-admin'),
    path('review-admin-requests/', AdminAccessApprovalView.as_view(), name='review-admin-requests'),
]
