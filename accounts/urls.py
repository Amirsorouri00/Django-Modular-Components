from django.urls import include, path

from .views import admins

urlpatterns = [
    
    path('admins/', include(([
        path('', admins.QuizListView.as_view(), name='quiz_list'),
        
    ], 'accounts'), namespace='admins')),
]