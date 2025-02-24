from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'faculty', views.FacultyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/login/', views.admin_login),
    path('admin/logout/', views.admin_logout),
    path('verify-face/', views.verify_face),
]