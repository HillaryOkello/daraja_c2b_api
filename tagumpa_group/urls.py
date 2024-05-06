from django.contrib import admin
from django.urls import path
from c2b_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/c2b/register/', views.RegisterC2BUrl.as_view(), name='register_c2b_url'),
    path('api/v1/c2b/simulate/', views.SimulateC2BTransaction.as_view(), name='simulate_c2b_transaction')
]
