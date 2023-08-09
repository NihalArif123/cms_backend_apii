from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from .models import *
from .serializers import *
from caad_api import services


def studentApi(request,std_cnic=0):
    if request.method=="GET":
        students = Student.objects.all()
        students_serializer = StudentSerializer(students, many=True)
        return JsonResponse(students_serializer.data,safe=False)
    elif request.method == 'POST':
        students_serializer = StudentSerializer(data=request.data) 
        if students_serializer.is_valid():
            students_serializer.save()
            return Response({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        student_data=request.data
        student=Student.objects.get(std_cnic=student_data['std_cnic'])
        students_serializer = StudentSerializer(student,data=student_data) 
        if students_serializer.is_valid():
            students_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        student=Student.objects.get(std_cnic=std_cnic)
        student.delete()
        return JsonResponse("Deleted sucessfully",safe=False)

def studentRegistrationApi(request,std_cnic=0):
    if request.method=="GET":
        studentsReg = StudentRegistration.objects.all()
        studentsReg_serializer = StudentRegistrationSerializer(studentsReg, many=True)
        return JsonResponse(studentsReg_serializer.data,safe=False)
    elif request.method == 'POST':
        studentreg_data=JSONParser().parse(request)
        studentsReg_serializer = StudentRegistrationSerializer(data=studentreg_data) 
        if studentsReg_serializer.is_valid():
            studentsReg_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        studentReg_data=JSONParser().parse(request)
        studentReg=StudentRegistration.objects.get(std_cnic=studentReg_data['std_cnic'])
        studentsReg_serializer = StudentRegistrationSerializer(studentReg,data=studentReg_data) 
        if studentsReg_serializer.is_valid():
            studentsReg_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        studentReg=StudentRegistration.objects.get(std_cnic=std_cnic)
        studentReg.delete()
        return JsonResponse("Deleted sucessfully",safe=False)


def studentRegistrationApi(request,std_cnic=0):
    if request.method=="GET":
        studentsReg = StudentRegistration.objects.all()
        studentsReg_serializer = StudentRegistrationSerializer(studentsReg, many=True)
        return JsonResponse(studentsReg_serializer.data,safe=False)
    elif request.method == 'POST':
        studentreg_data=JSONParser().parse(request)
        studentsReg_serializer = StudentRegistrationSerializer(data=studentreg_data) 
        if studentsReg_serializer.is_valid():
            studentsReg_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        studentReg_data=JSONParser().parse(request)
        studentReg=StudentRegistration.objects.get(std_cnic=studentReg_data['std_cnic'])
        studentsReg_serializer = StudentRegistrationSerializer(studentReg,data=studentReg_data) 
        if studentsReg_serializer.is_valid():
            studentsReg_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        studentReg=StudentRegistration.objects.get(std_cnic=std_cnic)
        studentReg.delete()
        return JsonResponse("Deleted sucessfully",safe=False)

def CaadRegistrationVerificationApi(request,caad_registration_verification=0):
    if request.method=="GET":
        CaadRegistrationVerifications_data = CaadRegistrationVerification.objects.all()
        CaadRegistrationVerification_serializer =CaadRegistrationVerificationSerializer(CaadRegistrationVerifications_data, many=True)
        return JsonResponse(CaadRegistrationVerification_serializer.data,safe=False)
    elif request.method == 'POST':
        CaadRegistrationVerifications_data=JSONParser().parse(request)
        CaadRegistrationVerifications_serializer =CaadRegistrationVerificationSerializer(data=CaadRegistrationVerifications_data) 
        if CaadRegistrationVerifications_serializer.is_valid():
            CaadRegistrationVerifications_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        CaadRegistrationVerifications_data=JSONParser().parse(request)
        CaadRegistrationVerificationsdata=CaadRegistrationVerification.objects.get(caad_registration_verification=CaadRegistrationVerifications_data['caad_registration_verification'])
        CaadRegistrationVerifications_serializer = CaadRegistrationVerificationSerializer(CaadRegistrationVerificationsdata,data=CaadRegistrationVerifications_data) 
        if CaadRegistrationVerifications_serializer.is_valid():
            CaadRegistrationVerifications_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        CaadRegistrationVerifications_data=CaadRegistrationVerification.objects.get(caad_registration_verification=caad_registration_verification)
        CaadRegistrationVerifications_data.delete()
        return JsonResponse("Deleted sucessfully",safe=False)


def InternshipsApi(request,internship_id=0):
    if request.method=="GET":
        Internships_data = Internships.objects.all()
        Internships_serializer = InternshipsSerializer(Internships_data, many=True)
        return JsonResponse(Internships_serializer.data,safe=False)
    elif request.method == 'POST':
        Internships_data=JSONParser().parse(request)
        try:
            std_cnic = Internships_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        try:
            student_registration = StudentRegistration.objects.get(std_cnic=std_cnic)
        except StudentRegistration.DoesNotExist:
           return JsonResponse({"message": "Student registration not found"}, status=404)
        Internships_data['registration_no'] = student_registration.reg_form_id
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
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        Internships_data=JSONParser().parse(request)
        Internshipdata=Internships.objects.get(internship_id=Internships_data['internship_id'])
        Internships_serializer = InternshipsSerializer(Internshipdata,data=Internships_data) 
        if Internships_serializer.is_valid():
            Internships_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        Internshipdata=Internships.objects.get(internship_id=internship_id)
        Internshipdata.delete()
        return JsonResponse("Deleted sucessfully",safe=False)


def EvaluationProformaApi(request,evaluation_id=0):
    if request.method=="GET":
        Evaluations_data = EvaluationProforma.objects.all()
        Evaluation_serializer = EvaluationProformaSerializer(Evaluations_data, many=True)
        return JsonResponse(Evaluation_serializer.data,safe=False)
    elif request.method == 'POST':
        Evaluations_data=JSONParser().parse(request)
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
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        Evaluations_data=JSONParser().parse(request)
        Evaluationsdata=EvaluationProforma.objects.get(evaluation_id=Evaluations_data['evaluation_id'])
        Evaluations_serializer = EvaluationProformaSerializer(Evaluationsdata,data=Evaluations_data) 
        if Evaluations_serializer.is_valid():
            Evaluations_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        Evaluationsdata=EvaluationProforma.objects.get(evaluation_id=evaluation_id)
        Evaluationsdata.delete()
        return JsonResponse("Deleted sucessfully",safe=False)


def NcpPublicationsApi(request,ncppublications_id=0):
    if request.method=="GET":
        Publications_data = NcpPublications.objects.all()
        NcpPublications_serializer = NcpPublicationsSerializer(Publications_data, many=True)
        return JsonResponse(NcpPublications_serializer.data,safe=False)
    elif request.method == 'POST':
        Publications_data=JSONParser().parse(request)
        Publications_serializer = NcpPublicationsSerializer(data=Publications_data) 
        if Publications_serializer.is_valid():
            Publications_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        Publications_data=JSONParser().parse(request)
        Publicationsdata=NcpPublications.objects.get(ncppublications_id=Publications_data['ncppublications_id'])
        Publications_serializer = NcpPublicationsSerializer(Publicationsdata,data=Publications_data) 
        if Publications_serializer.is_valid():
            Publications_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        Publicationsdata=NcpPublications.objects.get(ncppublications_id=ncppublications_id)
        Publicationsdata.delete()
        return JsonResponse("Deleted sucessfully",safe=False)


def CaadEvaluationVerificationApi(request,caad_evaluation_id=0):
    if request.method=="GET":
        CaadEvaluationVerifications_data = CaadEvaluationVerification.objects.all()
        CaadEvaluationVerification_serializer =CaadEvaluationVerificationSerializer(CaadEvaluationVerifications_data, many=True)
        return JsonResponse(CaadEvaluationVerification_serializer.data,safe=False)
    elif request.method == 'POST':
        CaadEvaluationVerifications_data=JSONParser().parse(request)
        CaadEvaluationVerification_serializer = CaadEvaluationVerificationSerializer(data=CaadEvaluationVerifications_data) 
        if CaadEvaluationVerification_serializer.is_valid():
            CaadEvaluationVerification_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        CaadEvaluationVerifications_data=JSONParser().parse(request)
        CaadEvaluationVerificationsdata=CaadEvaluationVerification.objects.get(caad_evaluation_id=CaadEvaluationVerifications_data['caad_evaluation_id'])
        CaadEvaluationVerification_serializer = CaadEvaluationVerificationSerializer(CaadEvaluationVerificationsdata,data=CaadEvaluationVerifications_data) 
        if CaadEvaluationVerification_serializer.is_valid():
            CaadEvaluationVerification_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        CaadEvaluationVerifications_data=CaadEvaluationVerification.objects.get(caad_evaluation_id=caad_evaluation_id)
        CaadEvaluationVerifications_data.delete()
        return JsonResponse("Deleted sucessfully",safe=False)

def ClearancePerformaApi(request,clearance_id=0):
    if request.method=="GET":
        ClearancePerforma_data = ClearancePerforma.objects.all()
        ClearancePerforma_serializer =ClearancePerformaSerializer(ClearancePerforma_data, many=True)
        return JsonResponse(ClearancePerforma_serializer.data,safe=False)
    elif request.method == 'POST':
        ClearancePerforma_data=JSONParser().parse(request)
        try:
            std_cnic = ClearancePerforma_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        internship_id=services.get_internship(std_cnic)
        identity_id=get_identity(internship_id)
        ClearancePerforma_data['internship'] = internship_id
        ClearancePerforma_data['identity'] = identity_id
        ClearancePerforma_data_serializer = ClearancePerformaSerializer(data=ClearancePerforma_data) 
        if ClearancePerforma_data_serializer.is_valid():
            clearance=ClearancePerforma_data_serializer.save()
            caad_clearance_verification_data = {
                'clearance': clearance.clearance_id,
            }
            caad_clearance_verification_serializer = CaadClearanceVerificationSerializer(
                data=caad_clearance_verification_data
            )
            if caad_clearance_verification_serializer.is_valid():
                caad_clearance_verification_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        ClearancePerforma_data=JSONParser().parse(request)
        ClearancePerformadata=ClearancePerforma.objects.get(clearance_id=ClearancePerforma_data['clearance_id'])
        ClearancePerforma_serializer = ClearancePerformaSerializer(ClearancePerformadata,data=ClearancePerforma_data) 
        if ClearancePerforma_serializer.is_valid():
            ClearancePerforma_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        ClearancePerforma_data=ClearancePerforma.objects.get(clearance_id=clearance_id)
        ClearancePerforma_data.delete()
        return JsonResponse("Deleted sucessfully",safe=False)


def NcpDuesApi(request,dues_id=0):
    if request.method=="GET":
        NcpDues_data = NcpDues.objects.all()
        NcpDues_serializer =NcpDuesSerializer(NcpDues_data, many=True)
        return JsonResponse(NcpDues_serializer.data,safe=False)
    elif request.method == 'POST':
        NcpDues_data=JSONParser().parse(request)
        NcpDues_data_serializer = NcpDuesSerializer(data=NcpDues_data) 
        if NcpDues_data_serializer.is_valid():
            NcpDues_data_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        NcpDues_data=JSONParser().parse(request)
        NcpDuesdata=NcpDues.objects.get(dues_id=NcpDues_data['dues_id'])
        NcpDues_serializer = NcpDuesSerializer(NcpDuesdata,data=NcpDues_data) 
        if NcpDues_serializer.is_valid():
            NcpDues_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        NcpDues_data=NcpDues.objects.get(dues_id=dues_id)
        NcpDues_data.delete()
        return JsonResponse("Deleted sucessfully",safe=False)

def CaadClearanceVerificationApi(request,caad_clearance_id=0):
    if request.method=="GET":
        CaadClearanceVerifications_data = CaadClearanceVerification.objects.all()
        CaadClearanceVerifications_serializer =CaadClearanceVerificationSerializer(CaadClearanceVerifications_data, many=True)
        return JsonResponse(CaadClearanceVerifications_serializer.data,safe=False)
    elif request.method == 'POST':
        CaadClearanceVerifications_data=JSONParser().parse(request)
        CaadClearanceVerifications_serializer = CaadClearanceVerificationSerializer(data=CaadClearanceVerifications_data) 
        if CaadClearanceVerifications_serializer.is_valid():
            CaadClearanceVerifications_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        CaadClearanceVerifications_data=JSONParser().parse(request)
        CaadClearanceVerificationsdata=CaadClearanceVerification.objects.get(caad_clearance_id=CaadClearanceVerifications_data['caad_clearance_id'])
        CaadClearanceVerifications_serializer = CaadClearanceVerificationSerializer(CaadClearanceVerificationsdata,data=CaadClearanceVerifications_data) 
        if CaadClearanceVerifications_serializer.is_valid():
            CaadClearanceVerifications_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        CaadClearanceVerifications_data=CaadClearanceVerification.objects.get(caad_clearance_id=caad_clearance_id)
        CaadClearanceVerifications_data.delete()
        return JsonResponse("Deleted sucessfully",safe=False)

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




def AccomodationProformaApi(request,id=0):
    if request.method=="GET":
        accomodation_prof = AccomodationProforma.objects.all()
        accomodation_prof_serializer = AccomodationProformaSerializer(accomodation_prof, many=True)
        return Response(accomodation_prof_serializer.data)
    elif request.method == 'POST':
        accomodation_prof_data = JSONParser().parse(request)
        try:
            std_cnic = accomodation_prof_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing std_cnic"}, status=400)

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
        return JsonResponse(accomodation_prof_serializer.errors, status=400)
    elif request.method == 'PUT':
        accomodation_prof_data=JSONParser().parse(request)
        accomodation_prof=AccomodationProforma.objects.get(ac_id=accomodation_prof_data['ac_id'])
        accomodation_prof_serializer = AccomodationProformaSerializer(accomodation_prof,data=accomodation_prof_data) 
        if accomodation_prof_serializer.is_valid():
            accomodation_prof_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        accomodation_prof=AccomodationProforma.objects.get(ac_id=id)
        accomodation_prof.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
# End here Accomodation Proforma API
  


def AccomodationTypeApi(request,id=0):
    if request.method=="GET":
        accomodation_type = AccomodationType.objects.all()
        accomodation_type_serializer = AccomodationTypeSerializer(accomodation_type, many=True)
        return Response(accomodation_type_serializer.data)
    elif request.method == 'POST':
        accomodation_type_data=JSONParser().parse(request)
        accomodation_type_serializer = AccomodationTypeSerializer(data=accomodation_type_data) 
        if accomodation_type_serializer.is_valid():
            accomodation_type_serializer.save()
            return Response({"message": "Insert successfully"})
        return JsonResponse("Failed to Insert",safe=False)
    elif request.method == 'PUT':
        accomodation_type_data=JSONParser().parse(request)
        accomodation_type=AccomodationType.objects.get(accomodation_id=accomodation_type_data['accomodation_id'])
        accomodation_type_serializer = AccomodationTypeSerializer(accomodation_type,data=accomodation_type_data) 
        if accomodation_type_serializer.is_valid():
            accomodation_type_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        accomodation_type=AccomodationType.objects.get(accomodation_id=id)
        accomodation_type.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
#End



def CaadAccomodationApi(request,id=0):
    if request.method=="GET":
        ncpChk_accomodation = CaadAccomodationVerification.objects.all()
        ncpChk_accomodation_serializer = CaadAccomodationVerificationSerializer(ncpChk_accomodation, many=True)
        return Response(ncpChk_accomodation_serializer.data)
    elif request.method == 'POST':
        ncpChk_accomodation_data=JSONParser().parse(request)
        ncpChk_accomodation_serializer = CaadAccomodationVerificationSerializer(data=ncpChk_accomodation_data) 
        if ncpChk_accomodation_serializer.is_valid():
            ncpChk_accomodation_serializer.save()
            return Response({"message": "Insert successfully"})
        return JsonResponse("Failed to Insert",safe=False)
    elif request.method == 'PUT':
        ncpChk_accomodation_data=JSONParser().parse(request)
        ncpChk_accomodation=CaadAccomodationVerification.objects.get(caad_hr3_id=ncpChk_accomodation_data['caad_hr3_id'])
        ncpChk_accomodation_serializer = CaadAccomodationVerificationSerializer(ncpChk_accomodation,data=ncpChk_accomodation_data) 
        if ncpChk_accomodation_serializer.is_valid():
            ncpChk_accomodation_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        ncpChk_accomodation=CaadAccomodationVerification.objects.get(caad_hr3_id=id)
        ncpChk_accomodation.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
#End

#NCP check accomodation

def NcpCheckAccApi(request,id=0):
    if request.method=="GET":
        caad_accomodation = NcpAccomodationCheck.objects.all()
        caad_accomodation_serializer = NcpAccomodationCheckSerializer(caad_accomodation, many=True)
        return Response(caad_accomodation_serializer.data)
    elif request.method == 'POST':
        caad_accomodation_data=JSONParser().parse(request)
        caad_accomodation_serializer = NcpAccomodationCheckSerializer(data=caad_accomodation_data) 
        if caad_accomodation_serializer.is_valid():
            caad_accomodation_serializer.save()
            return Response({"message": "Insert successfully"})
        return JsonResponse("Failed to Insert",safe=False)
    elif request.method == 'PUT':
        caad_accomodation_data=JSONParser().parse(request)
        caad_accomodation=NcpAccomodationCheck.objects.get(ncp_chk_id=caad_accomodation_data['ncp_chk_id'])
        caad_accomodation_serializer = NcpAccomodationCheckSerializer(caad_accomodation,data=caad_accomodation_data) 
        if caad_accomodation_serializer.is_valid():
            caad_accomodation_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        caad_accomodation=NcpAccomodationCheck.objects.get(ncp_chk_id=id)
        caad_accomodation.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
#END

#NCP approval accomodation
def NcpApprovalAccApi(request,id=0):
    if request.method=="GET":
        ncpAppr_accomodation = NcpAccomodationApproval.objects.all()
        ncpAppr_accomodation_serializer = NcpAccomodationApprovalSerializer(ncpAppr_accomodation, many=True)
        return Response(ncpAppr_accomodation_serializer.data)
    elif request.method == 'POST':
        ncpAppr_accomodation_data=JSONParser().parse(request)
        ncpAppr_accomodation_serializer = NcpAccomodationApprovalSerializer(data=ncpAppr_accomodation_data) 
        if ncpAppr_accomodation_serializer.is_valid():
            ncpAppr_accomodation_serializer.save()
            return Response({"message": "Insert successfully"})
        return JsonResponse("Failed to Insert",safe=False)
    elif request.method == 'PUT':
        ncpAppr_accomodation_data=JSONParser().parse(request)
        ncpAppr_accomodation=NcpAccomodationApproval.objects.get(ncp_allotted_id=ncpAppr_accomodation_data['ncp_allotted_id'])
        ncpAppr_accomodation_serializer = NcpAccomodationApprovalSerializer(ncpAppr_accomodation,data=ncpAppr_accomodation_data) 
        if ncpAppr_accomodation_serializer.is_valid():
            ncpAppr_accomodation_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        ncpAppr_accomodation=NcpAccomodationApproval.objects.get(ncp_allotted_id=id)
        ncpAppr_accomodation.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
#END
def ExtensionProformaApi(request,id=0):
    if request.method=="GET":
        extension_prof = ExtensionProforma.objects.all()
        extension_prof_serializer = ExtensionProformaSerializer(extension_prof, many=True)
        return Response(extension_prof_serializer.data)
    elif request.method == 'POST':
        extension_prof_data=JSONParser().parse(request)
        try:
            std_cnic=extension_prof_data['std_cnic']
        except KeyError:
            return JsonResponse({"message":"Missing std_cnic"},status=404)
        internship=services.get_internship(std_cnic)
        extension_prof_data['internship']=internship
        extension_prof_serializer = ExtensionProformaSerializer(data=extension_prof_data) 
        if extension_prof_serializer.is_valid():
            extension=extension_prof_serializer.save()
            caad_extension_verification_data={
                'extension_form':extension.extension_form_id,
            }
            caad_extension_verification_serializer=CaadExtensionVerificationSerializer(
                data=caad_extension_verification_data
            )
            if caad_extension_verification_serializer.is_valid():
                caad_extension_verification_serializer.save()
            return Response({"message": "Insert successfully"})
        return JsonResponse("Failed to Insert",safe=False)
    elif request.method == 'PUT':
        extension_prof_data=JSONParser().parse(request)
        extension_prof=ExtensionProforma.objects.get(extension_form_id=extension_prof_data['extension_form_id'])
        extension_prof_serializer = ExtensionProformaSerializer(extension_prof,data=extension_prof_data) 
        if extension_prof_serializer.is_valid():
            extension_prof_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        extension_prof=ExtensionProforma.objects.get(extension_form_id=id)
        extension_prof.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
#END

def CaadExtensionVerificationApi(request,id=0):
    if request.method=="GET":
        caad_extension_prof = CaadExtensionVerification.objects.all()
        caad_extension_prof_serializer = CaadExtensionVerificationSerializer(caad_extension_prof, many=True)
        return Response(caad_extension_prof_serializer.data)
    elif request.method == 'POST':
        caad_extension_prof_data=JSONParser().parse(request)
        caad_extension_prof_serializer = CaadExtensionVerificationSerializer(data=caad_extension_prof_data) 
        if caad_extension_prof_serializer.is_valid():
            caad_extension_prof_serializer.save()
            return Response({"message": "Insert successfully"})
        return JsonResponse("Failed to Insert",safe=False)
    elif request.method == 'PUT':
        caad_extension_prof_data=JSONParser().parse(request)
        caad_extension_prof=ExtensionProforma.objects.get(caad_extension_id=caad_extension_prof_data['caad_extension_id'])
        caad_extension_prof_serializer = CaadExtensionVerificationSerializer(caad_extension_prof,data=caad_extension_prof_data) 
        if caad_extension_prof_serializer.is_valid():
            caad_extension_prof_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        caad_extension_prof=CaadExtensionVerification.objects.get(caad_extension_id=id)
        caad_extension_prof.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
#END

def LoginProformaApi(request,id=0):
    if request.method=="GET":
        login_prof = LoginProforma.objects.all()
        login_prof_serializer = LoginProformaSerializer(login_prof, many=True)
        return Response(login_prof_serializer.data)
    elif request.method == 'POST':
        login_prof_data=JSONParser().parse(request)
        try:
            std_cnic=login_prof_data['std_cnic']
        except KeyError:
            return JsonResponse({"message":"Missing std_cnic"},status=404)
        internship=services.get_internship(std_cnic)
        login_prof_data['internship']=internship
        login_prof_serializer = LoginProformaSerializer(data=login_prof_data) 
        if login_prof_serializer.is_valid():
            login=login_prof_serializer.save()
            it_dept_data={
                'login_form':login.login_form_id,
            }
            it_dept_serializer=ItDeptLoginSerializer(
                data=it_dept_data
            )
            if it_dept_serializer.is_valid():
                it_dept_serializer.save()
            return Response({"message": "Insert successfully"})
        return JsonResponse("Failed to Insert",safe=False)
    elif request.method == 'PUT':
        login_prof_data=JSONParser().parse(request)
        login_prof=ExtensionProforma.objects.get(login_form_id=login_prof_data['login_form_id'])
        login_prof_serializer = LoginProformaSerializer(login_prof,data=login_prof_data) 
        if login_prof_serializer.is_valid():
            login_prof_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        login_prof=LoginProforma.objects.get(login_form_id=id)
        login_prof.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
#END

def ItDeptLoginApi(request,id=0):
    if request.method=="GET":
        it_login = ItDeptLogin.objects.all()
        it_login_serializer = ItDeptLoginSerializer(it_login, many=True)
        return Response(it_login_serializer.data)
    elif request.method == 'POST':
        it_login_data=JSONParser().parse(request)
        it_login_serializer = ItDeptLoginSerializer(data=it_login_data) 
        if it_login_serializer.is_valid():
            it_login_serializer.save()
            return Response({"message": "Insert successfully"})
        return JsonResponse("Failed to Insert",safe=False)
    elif request.method == 'PUT':
        it_login_data=JSONParser().parse(request)
        it_login=ItDeptLogin.objects.get(user_id=it_login_data['user_id'])
        it_login_serializer = ItDeptLoginSerializer(it_login,data=it_login_data) 
        if it_login_serializer.is_valid():
            it_login_serializer.save()
            return Response({"message": "Updated successfully"})
        return JsonResponse("Failed to Update",safe=False)
    elif request.method == 'DELETE':
        it_login=ItDeptLogin.objects.get(user_id=id)
        it_login.delete()
        return JsonResponse("Deleted sucessfully",safe=False)
#END
