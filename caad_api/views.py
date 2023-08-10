from rest_framework.response import Response

from .models import *
from .serializers import *
from caad_api import services


from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions


# ------------------------------NASIR APIS------------------------------------

# Accomodation Proforma API
# @api_view(['GET', 'POST','PUT','DELETE'])
# def AccomodationProformaApi(request,id=0):
class AccomodationProformaApi(APIView):

    def get(self, request):
            accomodation_profs = AccomodationProforma.objects.all()
            accomodation_prof_serializer = AccomodationProformaSerializer(accomodation_profs, many=True)
            return Response(accomodation_prof_serializer.data)


    def post(self, request):
        accomodation_prof_data = request.data
        try:
            std_cnic = accomodation_prof_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)

        internship=services.get_internship(std_cnic)
        identity=services.get_identity(internship)
        accomodation_prof_data['internship'] = internship
        accomodation_prof_data['identity_card']=identity
        accomodation_prof_serializer = AccomodationProformaSerializer(data=accomodation_prof_data)
        if accomodation_prof_serializer.is_valid():
            accomodation = accomodation_prof_serializer.save()
            caad_accomodation_verification_data = {
                'accomodation_form': accomodation.ac_id,
            }
            caad_accomodation_verification_serializer = CaadAccomodationVerificationSerializer(
                data=caad_accomodation_verification_data
            )
            if caad_accomodation_verification_serializer.is_valid():
                caad_accomodation_verification_serializer.save()

            return Response({"message": "Insert successfully"})
        return Response(accomodation_prof_serializer.errors, status=400)
   
    def put(self, request, pk):
        accomodation_prof_data = request.data
        accomodation_prof = AccomodationProforma.objects.get(pk=pk)
        accomodation_prof_serializer = AccomodationProformaSerializer(accomodation_prof, data=accomodation_prof_data)
        if accomodation_prof_serializer.is_valid():
            accomodation_prof_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(accomodation_prof_serializer.errors, status=400)

    def delete(self, request, pk):
        accomodation_prof = AccomodationProforma.objects.get(pk=pk)
        accomodation_prof.delete()
        return JsonResponse("Deleted sucessfully", safe=False)

# End here Accomodation Proforma API
  

# Accomodation Type API
class AccomodationTypeApi(APIView):
    def get(self, request):
        accomodation_types = AccomodationType.objects.all()
        accomodation_type_serializer = AccomodationTypeSerializer(accomodation_types, many=True)
        return Response(accomodation_type_serializer.data)
       
    def post(self, request):
        accomodation_type_data = request.data
        accomodation_type_serializer = AccomodationTypeSerializer(data=accomodation_type_data)
        if accomodation_type_serializer.is_valid():
            accomodation_type_serializer.save()
            return Response({"message": "Insert successfully"})
        return Response(accomodation_type_serializer.errors, status=400)

    def put(self, request, pk):
        accomodation_type_data = request.data
        accomodation_type = AccomodationType.objects.get(pk=pk)
        accomodation_type_serializer = AccomodationTypeSerializer(accomodation_type, data=accomodation_type_data)
        if accomodation_type_serializer.is_valid():
            accomodation_type_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(accomodation_type_serializer.errors, status=400)

    def delete(self, request, pk):
        accomodation_type = AccomodationType.objects.get(pk=pk)
        accomodation_type.delete()
        return JsonResponse("Deleted sucessfully", safe=False)


# Caad Accomodation Verification
class CaadAccomodationApi(APIView):
    def get(self, request, id=0):
            caad_accomodations = CaadAccomodationVerification.objects.all()
            caad_accomodation_serializer = CaadAccomodationVerificationSerializer(caad_accomodations, many=True)
            return Response(caad_accomodation_serializer.data)
      
    def post(self, request):
        caad_accomodation_data = request.data
        caad_accomodation_serializer = CaadAccomodationVerificationSerializer(data=caad_accomodation_data)
        if caad_accomodation_serializer.is_valid():
            caad_accomodation_serializer.save()
            return Response({"message": "Insert successfully"})
        return Response(caad_accomodation_serializer.errors, status=400)

    def put(self, request, pk):
        caad_accomodation_data = request.data
        caad_accomodation = CaadAccomodationVerification.objects.get(pk=pk)
        caad_accomodation_serializer = CaadAccomodationVerificationSerializer(caad_accomodation, data=caad_accomodation_data)
        if caad_accomodation_serializer.is_valid():
            caad_accomodation_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(caad_accomodation_serializer.errors, status=400)

    def delete(self, request, pk):
        caad_accomodation = CaadAccomodationVerification.objects.get(pk=pk)
        caad_accomodation.delete()
        return JsonResponse("Deleted sucessfully", safe=False)
#END

#NCP check accomodation
class NcpCheckAccApi(APIView):
    def get(self, request, id=0):
            ncp_accomodations = NcpAccomodationCheck.objects.all()
            ncp_accomodation_serializer = NcpAccomodationCheckSerializer(ncp_accomodations, many=True)
            return Response(ncp_accomodation_serializer.data)
      

    def post(self, request):
        ncp_accomodation_data = request.data
        ncp_accomodation_serializer = NcpAccomodationCheckSerializer(data=ncp_accomodation_data)
        if ncp_accomodation_serializer.is_valid():
            ncp_accomodation_serializer.save()
            return Response({"message": "Insert successfully"})
        return Response(ncp_accomodation_serializer.errors, status=400)

    def put(self, request, pk):
        ncp_accomodation_data = request.data
        ncp_accomodation = NcpAccomodationCheck.objects.get(pk=pk)
        ncp_accomodation_serializer = NcpAccomodationCheckSerializer(ncp_accomodation, data=ncp_accomodation_data)
        if ncp_accomodation_serializer.is_valid():
            ncp_accomodation_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(ncp_accomodation_serializer.errors, status=400)

    def delete(self, request, pk):
        ncp_accomodation = NcpAccomodationCheck.objects.get(pk=pk)
        ncp_accomodation.delete()
        return JsonResponse("Deleted sucessfully", safe=False)

#NCP approval accomodation
class NcpApprovalAccApi(APIView):

    def get(self, request, id=0):
        ncp_approval_accomodations = NcpAccomodationApproval.objects.all()
        ncp_approval_accomodation_serializer = NcpAccomodationApprovalSerializer(ncp_approval_accomodations, many=True)
        return Response(ncp_approval_accomodation_serializer.data)
     

    def post(self, request):
        ncp_approval_accomodation_data = request.data
        ncp_approval_accomodation_serializer = NcpAccomodationApprovalSerializer(data=ncp_approval_accomodation_data)
        if ncp_approval_accomodation_serializer.is_valid():
            ncp_approval_accomodation_serializer.save()
            return Response({"message": "Insert successfully"})
        return Response(ncp_approval_accomodation_serializer.errors, status=400)

    def put(self, request, pk):
        ncp_approval_accomodation_data = request.data
        ncp_approval_accomodation = NcpAccomodationApproval.objects.get(pk=pk)
        ncp_approval_accomodation_serializer = NcpAccomodationApprovalSerializer(ncp_approval_accomodation, data=ncp_approval_accomodation_data)
        if ncp_approval_accomodation_serializer.is_valid():
            ncp_approval_accomodation_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(ncp_approval_accomodation_serializer.errors, status=400)

    def delete(self, request, pk):
        ncp_approval_accomodation = NcpAccomodationApproval.objects.get(pk=pk)
        ncp_approval_accomodation.delete()
        return JsonResponse("Deleted sucessfully", safe=False)
#Extension Proforma


class ExtensionProformaApi(APIView):
    def get(self, request, id=0):
        extension_profs = ExtensionProforma.objects.all()
        extension_prof_serializer = ExtensionProformaSerializer(extension_profs, many=True)
        return Response(extension_prof_serializer.data)

    def post(self, request):
        extension_prof_data = request.data
        try:
            std_cnic = extension_prof_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing std_cnic"}, status=404)

        internship = services.get_internship(std_cnic)
        extension_prof_data['internship'] = internship
        extension_prof_serializer = ExtensionProformaSerializer(data=extension_prof_data)
        if extension_prof_serializer.is_valid():
            extension = extension_prof_serializer.save()
            caad_extension_verification_data = {
                'extension_form': extension.extension_form_id,
            }
            caad_extension_verification_serializer = CaadExtensionVerificationSerializer(
                data=caad_extension_verification_data
            )
            if caad_extension_verification_serializer.is_valid():
                caad_extension_verification_serializer.save()
            return Response({"message": "Insert successfully"})
        return Response(extension_prof_serializer.errors, status=400)

    def put(self, request, pk):
        extension_prof_data = request.data
        extension_prof = ExtensionProforma.objects.get(pk=pk)
        extension_prof_serializer = ExtensionProformaSerializer(extension_prof, data=extension_prof_data)
        if extension_prof_serializer.is_valid():
            extension_prof_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(extension_prof_serializer.errors, status=400)

    def delete(self, request, pk):
        extension_prof = ExtensionProforma.objects.get(pk=pk)
        extension_prof.delete()
        return JsonResponse("Deleted sucessfully", safe=False)

#CAAD Extension Proforma Verification
class CaadExtensionVerificationApi(APIView):
    def get(self, request, id=0):
        caad_extension_profs = CaadExtensionVerification.objects.all()
        caad_extension_prof_serializer = CaadExtensionVerificationSerializer(caad_extension_profs, many=True)
        return Response(caad_extension_prof_serializer.data)
     
    def post(self, request):
        caad_extension_prof_data = request.data
        caad_extension_prof_serializer = CaadExtensionVerificationSerializer(data=caad_extension_prof_data)
        if caad_extension_prof_serializer.is_valid():
            caad_extension_prof_serializer.save()
            return Response({"message": "Insert successfully"})
        return Response(caad_extension_prof_serializer.errors, status=400)

    def put(self, request, pk):
        caad_extension_prof_data = request.data
        caad_extension_prof = CaadExtensionVerification.objects.get(pk=pk)
        caad_extension_prof_serializer = CaadExtensionVerificationSerializer(caad_extension_prof, data=caad_extension_prof_data)
        if caad_extension_prof_serializer.is_valid():
            caad_extension_prof_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(caad_extension_prof_serializer.errors, status=400)

    def delete(self, request, pk):
        caad_extension_prof = CaadExtensionVerification.objects.get(pk=pk)
        caad_extension_prof.delete()
        return JsonResponse("Deleted sucessfully", safe=False)
#END

#Login Proforma

class LoginProformaApi(APIView):
    def get(self, request, id=0):
        login_profs = LoginProforma.objects.all()
        login_prof_serializer = LoginProformaSerializer(login_profs, many=True)
        return Response(login_prof_serializer.data)


    def post(self, request):
        login_prof_data = request.data
        try:
            std_cnic = login_prof_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing std_cnic"}, status=404)

        internship = services.get_internship(std_cnic)
        login_prof_data['internship'] = internship
        login_prof_serializer = LoginProformaSerializer(data=login_prof_data)
        if login_prof_serializer.is_valid():
            login = login_prof_serializer.save()
            it_dept_data = {
                'login_form': login.login_form_id,
            }
            it_dept_serializer = ItDeptLoginSerializer(data=it_dept_data)
            if it_dept_serializer.is_valid():
                it_dept_serializer.save()
            return Response({"message": "Insert successfully"})
        return Response(login_prof_serializer.errors, status=400)

    def put(self, request, pk):
        login_prof_data = request.data
        login_prof = LoginProforma.objects.get(pk=pk)
        login_prof_serializer = LoginProformaSerializer(login_prof, data=login_prof_data)
        if login_prof_serializer.is_valid():
            login_prof_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(login_prof_serializer.errors, status=400)

    def delete(self, request, pk):
        login_prof = LoginProforma.objects.get(pk=pk)
        login_prof.delete()
        return JsonResponse("Deleted sucessfully", safe=False)


#Login Proforma
class ItDeptLoginApi(APIView):
    def get(self, request, id=0):
        it_logins = ItDeptLogin.objects.all()
        it_login_serializer = ItDeptLoginSerializer(it_logins, many=True)
        return Response(it_login_serializer.data)
      
    def post(self, request):
        it_login_data = request.data
        it_login_serializer = ItDeptLoginSerializer(data=it_login_data)
        if it_login_serializer.is_valid():
            it_login_serializer.save()
            return Response({"message": "Insert successfully"})
        return Response(it_login_serializer.errors, status=400)

    def put(self, request, pk):
        it_login_data = request.data
        it_login = ItDeptLogin.objects.get(pk=pk)
        it_login_serializer = ItDeptLoginSerializer(it_login, data=it_login_data)
        if it_login_serializer.is_valid():
            it_login_serializer.save()
            return Response({"message": "Updated successfully"})
        return Response(it_login_serializer.errors, status=400)

    def delete(self, request, pk):
        it_login = ItDeptLogin.objects.get(pk=pk)
        it_login.delete()
        return JsonResponse("Deleted sucessfully", safe=False)
#END
