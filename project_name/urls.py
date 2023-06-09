"""{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from {{ project_name }} import views as api_views
from {{ project_name }}.views import ProductViewSet

product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('register/', api_views.RegistrationView.as_view(), name='register'),
    path('login/', api_views.LoginView.as_view(), name='login'),
    path('activate/<str:uidb64>/<str:token>/', api_views.ActivateAccountView.as_view(), name='activate'),
    path('reset-password/<str:uidb64>/<str:token>/', api_views.ResetPasswordView.as_view(), name='reset-password'),
    path('forgot-password/', api_views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
]
