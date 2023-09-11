from django.urls import path
from .views import *

urlpatterns = [ 
 path('student', studentApi.as_view()),
    path('student/<str:cnic>', studentApi.as_view()),
    path('studentreg', studentRegistrationApi.as_view()),
    path('studentreg/<str:cnic>', studentRegistrationApi.as_view()),
    path('internships', InternshipsApi.as_view()),
    path('internships/<str:id>',InternshipsApi.as_view()),
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
    path('send-verification-email', send_verification_email.as_view()),
   path('verify-code',verify_code.as_view()),
    path('login',login.as_view()),
    path('identity', IdentitycardApi.as_view(), name='IdentitycardApi'),  
    path('identity/<int:id>', IdentitycardApi.as_view(), name='IdentitycardApi'),
    path('caadidentity',CaadIdentityApi.as_view(), name='CaadIdentityApi'),  
    path('caadidentity/<int:id>', CaadIdentityApi.as_view(), name='CaadIdentityApi'),  
    path('latesitting', LateSittingApi.as_view(), name='LateSittingApi'),  
    path('latesitting/<str:id>', LateSittingApi.as_view(), name='LateSittingApi'), 
    path('caadlatesitting',CaadLatesittingVerificationApi.as_view(), name='CaadLatesittingVerificationApi'),  
    path('caadlatesitting/<int:id>', CaadLatesittingVerificationApi.as_view(), name='CaadLatesittingVerificationApi'), 
    path('transport', TransportMemFormApi.as_view(), name='TransportMemFormApi'),  
    path('transport/<int:id>',TransportMemFormApi.as_view(), name='TransportMemFormApi'),
    path('transportsect', CaadTransportVerificationApi.as_view(), name='CaadTransportVerificationApi'),  
    path('transportsect/<int:id>', CaadTransportVerificationApi.as_view(), name='CaadTransportVerificationApi'), 

    path('accomodation', AccomodationProformaApi.as_view(), name="AccomodationProformaApi"),
    path('accomodation/<int:id>', AccomodationProformaApi.as_view()),
    path('accomodationtype', AccomodationTypeApi.as_view(), name="AccomodationTypeApi"),
    path('accomodationtype/<int:pk>', AccomodationTypeApi.as_view()),
    path('caadaccomodation', CaadAccomodationApi.as_view(), name="CaadAccomodationApi"),
    path('caadaccomodation/<int:pk>', CaadAccomodationApi.as_view()),
    path('ncpaccomodationchk', NcpCheckAccApi.as_view(), name="NcpCheckAccApi"),
    path('ncpaccomodationchk/<int:pk>', NcpCheckAccApi.as_view()),
    path('ncpaccomodationapp', NcpApprovalAccApi.as_view(), name="NcpApprovalAccApi"),
    path('ncpaccomodationapp/<int:pk>', NcpApprovalAccApi.as_view()),
    path('extension', ExtensionProformaApi.as_view(), name="ExtensionProformaApi"),
    path('extension/<int:pk>', ExtensionProformaApi.as_view()),
    path('caadextension', CaadExtensionVerificationApi.as_view(), name="CaadExtensionVerificationApi"),
    path('caadextension/<int:pk>', CaadExtensionVerificationApi.as_view()),
    path('login', LoginProformaApi.as_view(), name="LoginProformaApi"),
    path('login/<int:pk>', LoginProformaApi.as_view()),
    path('itlogin', ItDeptLoginApi.as_view(), name="ItDeptLoginApi"),
    path('itlogin/<int:pk>', ItDeptLoginApi.as_view()), 

  
]