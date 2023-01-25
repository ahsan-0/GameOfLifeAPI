from django.urls import path
from testingApp import test_views

urlpatterns = [
    path("patterns", test_views.get_patterns, name="test_get_patterns"),
    path("patterns/<str:id>", test_views.single_pattern, name="test_get_single_pattern"),
    path("users", test_views.get_users, name="test_get_users"),
    path("users/<str:id>", test_views.get_single_user, name="test_get_single_user"),
    path('users/<str:username>/patterns', test_views.get_patterns_by_username, name='test_get_patterns_by_username')
]
