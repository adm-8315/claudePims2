from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'notification-templates', views.NotificationTemplateViewSet)
router.register(r'notification-preferences', views.NotificationPreferenceViewSet, basename='notificationpreference')

urlpatterns = [
    path('', include(router.urls)),
]