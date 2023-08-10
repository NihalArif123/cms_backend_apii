from django.urls import path
from caad_api import views

urlpatterns = [ 
    path('accomodation', views.AccomodationProformaApi.as_view(), name="AccomodationProformaApi"),
    path('accomodation/<int:pk>', views.AccomodationProformaApi.as_view()),
    path('accomodationtype', views.AccomodationTypeApi.as_view(), name="AccomodationTypeApi"),
    path('accomodationtype/<int:pk>', views.AccomodationTypeApi.as_view()),
    path('caadaccomodation', views.CaadAccomodationApi.as_view(), name="CaadAccomodationApi"),
    path('caadaccomodation/<int:pk>', views.CaadAccomodationApi.as_view()),
    path('ncpaccomodationchk', views.NcpCheckAccApi.as_view(), name="NcpCheckAccApi"),
    path('ncpaccomodationchk/<int:pk>', views.NcpCheckAccApi.as_view()),
    path('ncpaccomodationapp', views.NcpApprovalAccApi.as_view(), name="NcpApprovalAccApi"),
    path('ncpaccomodationapp/<int:pk>', views.NcpApprovalAccApi.as_view()),
    path('extension', views.ExtensionProformaApi.as_view(), name="ExtensionProformaApi"),
    path('extension/<int:pk>', views.ExtensionProformaApi.as_view()),
    path('caadextension', views.CaadExtensionVerificationApi.as_view(), name="CaadExtensionVerificationApi"),
    path('caadextension/<int:pk>', views.CaadExtensionVerificationApi.as_view()),
    path('login', views.LoginProformaApi.as_view(), name="LoginProformaApi"),
    path('login/<int:id>', views.LoginProformaApi.as_view()),
    path('itlogin', views.ItDeptLoginApi, name="ItDeptLoginApi"),
    path('itlogin/<int:id>', views.ItDeptLoginApi), 
]