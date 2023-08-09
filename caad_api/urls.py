from django.urls import path
from caad_api import views

urlpatterns = [
  
    path('identity', views.IdentitycardApi.as_view(), name='IdentitycardApi'),  
    path('identity/<int:pk>', views.IdentitycardApi.as_view(), name='IdentitycardApi'),
    path('caadidentity', views.CaadIdentityApi.as_view(), name='CaadIdentityApi'),  
    path('caadidentity/<int:pk>', views.CaadIdentityApi.as_view(), name='CaadIdentityApi'),  
    path('latesitting', views.LateSittingApi.as_view(), name='LateSittingApi'),  
    path('latesitting/<int:pk>', views.LateSittingApi.as_view(), name='LateSittingApi'), 
    path('caadlatesitting', views.CaadLatesittingVerificationApi.as_view(), name='CaadLatesittingVerificationApi'),  
    path('caadlatesitting/<int:pk>', views.CaadLatesittingVerificationApi.as_view(), name='CaadLatesittingVerificationApi'), 
    path('transport', views.TransportMemFormApi.as_view(), name='TransportMemFormApi'),  
    path('transport/<int:pk>', views.TransportMemFormApi.as_view(), name='TransportMemFormApi'),
    path('transportsect', views.CaadTransportVerificationApi.as_view(), name='CaadTransportVerificationApi'),  
    path('transportsect/<int:pk>', views.CaadTransportVerificationApi.as_view(), name='CaadTransportVerificationApi'), 
   
]