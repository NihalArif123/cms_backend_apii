from django.urls import path
from .views import *

urlpatterns = [
    path('student', studentApi.as_view()),
    path('student/<str:cnic>', studentApi.as_view()),
    path('studentreg', studentRegistrationApi.as_view()),
    path('studentreg/<str:cnic>', studentRegistrationApi.as_view()),
    path('internships', InternshipsApi.as_view()),
    path('internships/<int:id>',InternshipsApi.as_view()),
    path('evaluation', EvaluationProformaApi.as_view()),
    path('evaluation/<int:id>', EvaluationProformaApi.as_view()),
    path('caadevaluation', CaadEvaluationVerificationApi.as_view()),
    path('caadevaluation/<int:id>', CaadEvaluationVerificationApi.as_view()),
    path('caadclearance', CaadClearanceVerificationApi.as_view()),
    path('caadclearance/<int:id>', CaadClearanceVerificationApi.as_view()),
    path('publications', NcpPublicationsApi.as_view()),
    path('publications/<int:id>', NcpPublicationsApi.as_view()),
    path('clearance', ClearancePerformaApi.as_view()),
    path('clearance/<int:id>', ClearancePerformaApi.as_view()),
    path('dues', NcpDuesApi.as_view()),
    path('dues/<int:id>', NcpDuesApi.as_view()),
    path('caadreg', CaadRegistrationVerificationApi.as_view()),
    path('caadreg/<int:id>', CaadRegistrationVerificationApi.as_view()),
    
  
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