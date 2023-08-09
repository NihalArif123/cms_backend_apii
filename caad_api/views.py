from rest_framework.response import Response
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
    