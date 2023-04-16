from django.urls import path 
from .import views
from .views import classBased,mailsender,empPost,empget,Signup,AuthenticateUser
from .views import EmployeelistCreateApiView,EmployeeRetriveUpdateDeleteApiView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="User API",
      default_version='v1',
      description="User related all API's",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    # basic router for crud 
    path(r'data', views.all_details, name='all_details'),
    path('data/<int:pk>', views.all_details, name='all_details'),
    path('create',views.create_data,name='create_data'),
    path('update/<int:pk>',views.update_data,name='update_data'),
    path('delete/<int:pk>',views.delete_data,name='delete_data'),

    #Generic api views and mixins 
    path('employee',EmployeelistCreateApiView.as_view(),name='EmployeelistCreateApiView'),
    path('employee/<int:pk>',EmployeeRetriveUpdateDeleteApiView.as_view(),name='EmployeeRetriveUpdateDeleteApiView'),

    #class-Based 
    path('c',classBased.as_view(),name='classbased'),
    path('c/<int:pk>/',classBased.as_view(),name='classbased'),

    #Mail sending
    path('mail',mailsender.as_view(),name='mailsender'),

    #generics 
    path('api/create',empPost.as_view(),name='empPost'),
    path('api/create/<int:pk>',empget.as_view(),name='empget'),

    #signup and token generation
    path('signup',Signup.as_view(),name='signup'),
    path('AuthenticateUser',AuthenticateUser.as_view(),name='AuthenticateUser'),

    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# Viewsets example router customization 
# from .views import employeeView
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('examples', employeeView, basename='example')
# urlpatterns = router.urls