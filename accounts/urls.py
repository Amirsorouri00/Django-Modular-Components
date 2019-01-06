from django.urls import include, path
# from django.conf.urls import url
# from django.views.decorators.csrf import csrf_exempt
from .views import admins
from .views.rest.views import test2, Logout #, CustomAuthToken

app_name = 'accounts'

urlpatterns = [
    path('form/', include(([
        path('admins/', include(([
            path('', admins.AdminListView.as_view(), name='admin_list'),
            path('email_form/', admins.AdminFormView.as_view(), name='admin_list'),
            
        ], 'accounts'), namespace='admins')),

    ], 'accounts'), namespace='form')),
    

    path('rest/', include(([
        # url(r'^api-token-auth/', csrf_exempt(CustomAuthToken.as_view()), name='api_token_auth'),
        path('logout/', Logout, name='service_logout'),
        
        path('admins/', include(([
            path('test/', test2, name='rest_admin_test2'),
            
        ], 'accounts'), namespace='rest_admins')),
        
    ], 'accounts'), namespace='rest')),
]