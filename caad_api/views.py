from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from .models import *
from .serializers import *
from caad_api import services


class studentApi(APIView):
    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        if not students:
            return Response(
                {"res": "Students not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        students_serializer = StudentSerializer(students,many=True)
        return Response(students_serializer.data,status=status.HTTP_200_OK)
    # def get(self, request, cnic,*args, **kwargs):
    #     students= Student.objects.get(std_cnic=cnic)
    #     if not students:
    #         return Response(
    #             {"res": "Students not found"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     students_serializer = StudentSerializer(students)
    #     return Response(students_serializer.data,status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cnic, *args, **kwargs):
        student_data = Student.objects.get(std_cnic=cnic)
        if not student_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StudentSerializer(instance = student_data, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cnic, *args, **kwargs):
        student_data = Student.objects.get(std_cnic=cnic)
        if not student_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        student_data.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
class studentRegistrationApi(APIView):
    def get(self, request, *args, **kwargs):
        studentsReg = StudentRegistration.objects.all()
        studentsReg_serializer = StudentRegistrationSerializer(studentsReg, many=True)
        return Response(studentsReg_serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request,cnic, *args, **kwargs):
        studentReg_data = StudentRegistration.objects.get(std_cnic=cnic)
        if not studentReg_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StudentRegistrationSerializer(instance = studentReg_data, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, cnic,*args, **kwargs):
        studentReg_data = StudentRegistration.objects.get(std_cnic=cnic)
        if not studentReg_data:
            return Response(
                {"res": "Object does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        studentReg_data.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class CaadRegistrationVerificationApi(APIView):
    def get(self, request, *args, **kwargs):
        CaadRegistrationVerifications_data = CaadRegistrationVerification.objects.all()
        CaadRegistrationVerification_serializer =CaadRegistrationVerificationSerializer(CaadRegistrationVerifications_data, many=True)
        return Response(CaadRegistrationVerification_serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = CaadRegistrationVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request,id, *args, **kwargs):
        CaadRegistrationVerifications_data = CaadRegistrationVerification.objects.get(caad_registration_verification=id)
        if not studentReg_data:
            return Response(
                {"res": "Object does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StudentRegistrationSerializer(instance = studentReg_data, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id,*args, **kwargs):
        CaadRegistrationVerifications_data = CaadRegistrationVerification.objects.get(caad_registration_verification=id)
        if not CaadRegistrationVerifications_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        CaadRegistrationVerifications_data.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
class InternshipsApi(APIView):

    def get(self, request, *args, **kwargs):
        Internships_data = Internships.objects.all()
        Internships_serializer = InternshipsSerializer(Internships_data, many=True)
        return Response(Internships_serializer.data)
    def post(self, request, *args, **kwargs):
        Internships_data=request.data
        try:
            std_cnic = Internships_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        try:
            student_registration = StudentRegistration.objects.get(std_cnic=std_cnic)
        except StudentRegistration.DoesNotExist:
           return JsonResponse({"message": "Student registration not found"}, status=404)
        Internships_serializer = InternshipsSerializer(data=Internships_data) 
        if Internships_serializer.is_valid():
            internship=Internships_serializer.save()
            caad_registration_verification_data = {
                'internship': internship.internship_id,
            }
            caad_registration_verification_serializer = CaadRegistrationVerificationSerializer(
                data=caad_registration_verification_data
            )
            if caad_registration_verification_serializer.is_valid():
                caad_registration_verification_serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request,id, *args, **kwargs): 
        Internshipdata=Internships.objects.get(internship_id=id)
        if not Internshipdata:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StudentRegistrationSerializer(instance = Internshipdata, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, cnic,*args, **kwargs):
        Internshipdata=Internships.objects.get(internship_id=internship_id)
        if not Internshipdata:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        Internshipdata.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class EvaluationProformaApi(APIView):
    def get(self, request, *args, **kwargs):
        Evaluations_data = EvaluationProforma.objects.all()
        Evaluation_serializer = EvaluationProformaSerializer(Evaluations_data, many=True)
        return Response(Evaluation_serializer.data)
    def post(self, request, *args, **kwargs):
        Evaluations_data=request.data
        try:
            std_cnic = Evaluations_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        internship_id=services.get_internship(std_cnic)
        Evaluations_data['internship'] = internship_id
        Evaluations_serializer = EvaluationProformaSerializer(data=Evaluations_data) 
        if Evaluations_serializer.is_valid():
            evalaution=Evaluations_serializer.save()
            publications_data = {
                'evaluation': evalaution.evaluation_id,
            }
            caad_evaluation_verification_data = {
                'evaluation': evalaution.evaluation_id,
            }
            caad_evaluation_verification_serializer = CaadEvaluationVerificationSerializer(
                data=caad_evaluation_verification_data
            )
            publications_serializer = NcpPublicationsSerializer(
                data=publications_data
            )
            if caad_evaluation_verification_serializer.is_valid():
                caad_evaluation_verification_serializer.save() 
            if publications_serializer.is_valid():
                publications_serializer.save() 
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request,id, *args, **kwargs): 
        Evaluationsdata=EvaluationProforma.objects.get(evaluation_id=id)
        if not Evaluationsdata:
            return Response(
                {"res": "Object does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StudentRegistrationSerializer(instance = Evaluationsdata, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id,*args, **kwargs):
        Evaluationsdata=EvaluationProforma.objects.get(evaluation_id=id)
        if not Evaluationsdata:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        Evaluationsdata.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
class NcpPublicationsApi(APIView):
    def get(self, request, *args, **kwargs):
        Publications_data = NcpPublications.objects.all()
        if not Publications_data:
            return Response(
                {"res": "Not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        NcpPublications_serializer = NcpPublicationsSerializer(Publications_data, many=True)
        return Response(NcpPublications_serializer.data,status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer = NcpPublicationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        Publicationsdata=NcpPublications.objects.get(ncppublications_id=id)
        if not Publicationsdata:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StudentSerializer(instance = Publicationsdata, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        Publicationsdata=NcpPublications.objects.get(ncppublications_id=id)
        if not Publicationsdata:
            return Response(
                {"res": "Object does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        Publicationsdata.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class CaadEvaluationVerificationApi(APIView):
    def get(self, request, *args, **kwargs):
        CaadEvaluationVerifications_data = CaadEvaluationVerification.objects.all()
        if not CaadEvaluationVerifications_data:
            return Response(
                {"res": "Not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        CaadEvaluationVerification_serializer =CaadEvaluationVerificationSerializer(CaadEvaluationVerifications_data, many=True)
        return Response(CaadEvaluationVerification_serializer.data,status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer = CaadEvaluationVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        CaadEvaluationVerifications_data=CaadEvaluationVerification.objects.get(caad_evaluation_id=id)
        if not CaadEvaluationVerifications_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CaadEvaluationVerificationSerializer(instance = CaadEvaluationVerifications_data, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        CaadEvaluationVerifications_data=CaadEvaluationVerification.objects.get(caad_evaluation_id=id)
        if not CaadEvaluationVerifications_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        CaadEvaluationVerifications_data.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class ClearancePerformaApi(APIView):
    def get(self, request, *args, **kwargs):
        ClearancePerforma_data = ClearancePerforma.objects.all()
        if not ClearancePerforma_data:
            return Response(
                {"res": "Not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        ClearancePerforma_serializer =ClearancePerformaSerializer(ClearancePerforma_data, many=True)
        return Response(ClearancePerforma_serializer.data,status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer = ClearancePerformaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        ClearancePerforma_data=ClearancePerforma.objects.get(clearance_id=id)
        if not ClearancePerforma_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClearancePerforma_serializer(instance = ClearancePerforma_data, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        ClearancePerforma_data=ClearancePerforma.objects.get(clearance_id=id)
        if not ClearancePerforma_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        ClearancePerforma_data.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class NcpDuesApi(APIView):
    def get(self, request, *args, **kwargs):
        NcpDues_data = NcpDues.objects.all()
        if not NcpDues_data:
            return Response(
                {"res": "Not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        NcpDues_serializer =NcpDuesSerializer(NcpDues_data, many=True)
        return Response(NcpDues_serializer.data,status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer = NcpDuesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        NcpDues_data=NcpDues.get(dues_id=id)
        if not NcpDues_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = NcpDuesSerializer(instance = NcpDues_data, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        NcpDues_data=NcpDues.objects.get(dues_id=id)
        if not NcpDues_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        NcpDues_data.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class CaadClearanceVerificationApi(APIView):
    def get(self, request, *args, **kwargs):
        CaadClearanceVerifications_data = CaadClearanceVerification.objects.all()
        if not CaadClearanceVerifications_data:
            return Response(
                {"res": "Not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        CaadClearanceVerifications_serializer =CaadClearanceVerificationSerializer(CaadClearanceVerifications_data, many=True)
        return Response(CaadClearanceVerifications_serializer.data,status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer = CaadClearanceVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        CaadClearanceVerifications_data=CaadClearanceVerification.get(caad_clearance_id=id)
        if not CaadClearanceVerifications_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CaadClearanceVerificationSerializer(instance = CaadClearanceVerifications_data, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        CaadClearanceVerifications_data=CaadClearanceVerification.objects.get(caad_clearance_id=id)
        if not NcpDues_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        CaadClearanceVerifications_data.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
class IdentitycardApi(APIView):
    def get(self, request, *args, **kwargs):
        identity = IdentitycardProforma.objects.all()
        if not identity:
            return Response(
                {"res": "Identity Card not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        identity_serializer = IdentitycardProformaSerializer(identity, many=True)
        return Response(identity_serializer.data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        identity_data = request.data
        try:
            std_cnic = identity_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)

        internship=services.get_internship(std_cnic)
        identity_data['internship'] = internship
        identity_serializer = IdentitycardProformaSerializer(data=identity_data)
        if identity_serializer.is_valid():
            identity_serializer.save()
            return Response(identity_serializer.data, status=status.HTTP_201_CREATED)
        return Response(identity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk, *args, **kwargs):
        try:
            identity = IdentitycardProforma.objects.get(pk=pk)
        except identity.DoesNotExist:
            return Response(
                {"res": "Identity card not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        identity_serializer = IdentitycardProformaSerializer(identity, data=request.data)
        if identity_serializer.is_valid():
            identity_serializer.save()
            return Response(identity_serializer.data, status=status.HTTP_200_OK)
        return Response(identity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, *args, **kwargs):
        try:
            identity = IdentitycardProforma.objects.get(pk=pk)
        except identity.DoesNotExist:
            return Response(
                {"res": "Identity Card not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        identity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CaadIdentityApi(APIView):
    def get(self, request, *args, **kwargs):
        caadidentity = CaadIdentityVerification.objects.all()
        if not caadidentity:
            return Response(
                {"res": "Caad Identity Verification not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        caadidentity_serializer = CaadIdentityVerificationSerializer(caadidentity, many=True)
        return Response(caadidentity_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        caadidentity_data = request.data
        try:
            std_cnic = caadidentity_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)

        internship=services.get_internship(std_cnic)
        identity=services.get_identity(internship)
        caadidentity_data['identity_id']=identity
        caadidentity_serializer = CaadIdentityVerificationSerializer(data=caadidentity_data)
        if caadidentity_serializer.is_valid():
            caadidentity_serializer.save()
            return Response(caadidentity_serializer.data, status=status.HTTP_201_CREATED)
        return Response(caadidentity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            caadidentity = CaadIdentityVerification.objects.get(pk=pk)
        except CaadIdentityVerification.DoesNotExist:
            return Response(
                {"res": "CAAD identity verification not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        caadidentity_serializer = CaadIdentityVerificationSerializer(caadidentity, data=request.data)
        if caadidentity_serializer.is_valid():
            caadidentity_serializer.save()
            return Response(caadidentity_serializer.data, status=status.HTTP_200_OK)
        return Response(caadidentity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            caadidentity = CaadIdentityVerification.objects.get(pk=pk)
        except CaadIdentityVerification.DoesNotExist:
            return Response(
                {"res": "CAAD Identity Verification not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        caadidentity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LateSittingApi(APIView):
    def get(self, request, *args, **kwargs):
        latesitting=LateSittingProforma.objects.all()
        if not latesitting:
            return Response(
                {"res": "Late Sitting Proforma not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        latesitting_serializer=LateSittingProformaSerializer(latesitting,many=True)
        return Response(latesitting_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        latesitting_data = request.data
        try:
            std_cnic = latesitting_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)
        internship=services.get_internship(std_cnic)
        latesitting_data['internship']=internship
        latesitting_serializer = LateSittingProformaSerializer(data=latesitting_data)
        if latesitting_serializer.is_valid():
            latesitting=latesitting_serializer.save()
            caad_latesitting_verification_data = {
                'latesit': latesitting.latesit_id,
            }
            caad_latesitting_verification_serializer = CaadLatesittingVerificationSerializer(
                data=caad_latesitting_verification_data
            )
            if caad_latesitting_verification_serializer.is_valid():
                caad_latesitting_verification_serializer.save()
            return Response(latesitting_serializer.data, status=status.HTTP_201_CREATED)
        return Response(latesitting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            latesitting = LateSittingProforma.objects.get(pk=pk)
        except LateSittingProforma.DoesNotExist:
            return Response(
                {"res": "Late Sitting Proforma not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        latesitting_serializer = LateSittingProformaSerializer(latesitting, data=request.data)
        if latesitting_serializer.is_valid():
            latesitting_serializer.save()
            return Response(latesitting_serializer.data, status=status.HTTP_200_OK)
        return Response(latesitting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            latesitting = LateSittingProforma.objects.get(pk=pk)
        except LateSittingProforma.DoesNotExist:
            return Response(
                {"res": "Late Sitting Proforma not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        latesitting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CaadLatesittingVerificationApi(APIView):
    def get(self, request, *args, **kwargs):
        caadlatesit=CaadLatesittingVerification.objects.all()
        if not caadlatesit:
            return Response(
                {"res": "Caad Late Sitting Verification not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        caadlatesit_serializer=CaadLatesittingVerificationSerializer(caadlatesit,many=True)
        return Response(caadlatesit_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        caadlatesit_data = request.data
        caadlatesit_serializer = CaadLatesittingVerificationSerializer(data=caadlatesit_data)
        if caadlatesit_serializer.is_valid():
            caadlatesit_serializer.save()
            return Response(caadlatesit_serializer.data, status=status.HTTP_201_CREATED)
        return Response(caadlatesit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            caadlatesit = CaadLatesittingVerification.objects.get(pk=pk)
        except CaadLatesittingVerification.DoesNotExist:
            return Response(
                {"res": "CAAD Late Sitting Verification not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        caadlatesit_serializer = CaadLatesittingVerificationSerializer(caadlatesit, data=request.data)
        if caadlatesit_serializer.is_valid():
            caadlatesit_serializer.save()
            return Response(caadlatesit_serializer.data, status=status.HTTP_200_OK)
        return Response(caadlatesit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            caadlatesit = CaadLatesittingVerification.objects.get(pk=pk)
        except CaadLatesittingVerification.DoesNotExist:
            return Response(
                {"res": "CAAD Late Sitting Verification not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        caadlatesit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransportMemFormApi(APIView):
    def get(self, request, *args, **kwargs):
        transportform=TransportMemberProforma.objects.all()
        if not transportform:
            return Response(
                {"res": "Transport Member Proforma not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        transportform_serializer=TransportMemberProformaSerializer(transportform,many=True)
        return Response(transportform_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        transportform_data = request.data
        try:
            std_cnic = transportform_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)
        internship=services.get_internship(std_cnic)
        identity=services.get_identity(internship)
        transportform_data['internship']=internship
        transportform_data['identity_card']=identity
        transportform_serializer = TransportMemberProformaSerializer(data=transportform_data)
        if transportform_serializer.is_valid():
            transport=transportform_serializer.save()
            print(transport)
            caadtransportsect_verification_data = {
                'transport_form': transport.transport_form_id,
            }
            caadtransportsectverification_serializer = CaadTransportVerificationSerializer(
                data=caadtransportsect_verification_data
            )
            if caadtransportsectverification_serializer.is_valid():
                caadtransportsectverification_serializer.save()
            return Response(transportform_serializer.data, status=status.HTTP_201_CREATED)
        return Response(transportform_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            transportform = TransportMemberProforma.objects.get(pk=pk)
        except TransportMemberProforma.DoesNotExist:
            return Response(
                {"res": "Transport Member Proforma not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        transportform_serializer = TransportMemberProformaSerializer(transportform, data=request.data)
        if transportform_serializer.is_valid():
            transportform_serializer.save()
            return Response(transportform_serializer.data, status=status.HTTP_200_OK)
        return Response(transportform_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            transportform = TransportMemberProforma.objects.get(pk=pk)
        except TransportMemberProforma.DoesNotExist:
            return Response(
                {"res": "Transport Member Proforma not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        transportform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CaadTransportVerificationApi(APIView):
    def get(self, request, *args, **kwargs):
        caadtransportsect=CaadTransportVerification.objects.all()
        if not caadtransportsect:
            return Response(
                {"res": "Caad Transport Verification not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        caadtransportsect_serializer=CaadTransportVerificationSerializer(caadtransportsect,many=True)
        return Response(caadtransportsect_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        caadtransportsect_data = request.data
        caadtransportsect_serializer = CaadTransportVerificationSerializer(data=caadtransportsect_data)
        if caadtransportsect_serializer.is_valid():
            caadtransportsect_serializer.save()
            return Response(caadtransportsect_serializer.data, status=status.HTTP_201_CREATED)
        return Response(caadtransportsect_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            caadtransportsect = CaadTransportVerification.objects.get(pk=pk)
        except CaadTransportVerification.DoesNotExist:
            return Response(
                {"res": "CAAD Transport Verification not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        caadtransportsect_serializer = CaadTransportVerificationSerializer(caadtransportsect, data=request.data)
        if caadtransportsect_serializer.is_valid():
            caadtransportsect_serializer.save()
            return Response(caadtransportsect_serializer.data, status=status.HTTP_200_OK)
        return Response(caadtransportsect_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            caadtransportsect = CaadTransportVerification.objects.get(pk=pk)
        except CaadTransportVerification.DoesNotExist:
            return Response(
                {"res": "CAAD Transport Section Verification not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        caadtransportsect.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



