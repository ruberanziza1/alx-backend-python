from django.urls import path, include
from rest_framework import routers  # For DefaultRouter
from rest_framework_nested import routers as nested_routers  # Alias to avoid conflict

from .views import ConversationViewSet, MessageViewSet

# Create the parent router
default_router = routers.DefaultRouter()
default_router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create the nested router with parent router and prefix
nested_router = nested_routers.NestedDefaultRouter(default_router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(default_router.urls)),
    path('', include(nested_router.urls)),
]
