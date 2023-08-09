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
    
]