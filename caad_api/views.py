from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from caad_api import services

@api_view(['GET', 'POST','PUT','DELETE'])
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
@csrf_exempt
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

@csrf_exempt
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
@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
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
@csrf_exempt
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

@csrf_exempt
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
@csrf_exempt
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

@csrf_exempt
def IdentitycardProformaApi(request,id=0):
    if request.method=='GET':
        identitycard=IdentitycardProforma.objects.all()
        identitycard_serializer=IdentitycardProformaSerializer(identitycard,many=True)
        return JsonResponse(identitycard_serializer.data,safe=False)
    elif request.method=='POST':
        identitycard_data=JSONParser().parse(request)
        try:
            std_cnic = identitycard_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        internship_id=services.get_internship(std_cnic)
        identitycard_data['internship'] = internship_id
        identitycard_serializer=IdentitycardProformaSerializer(data=identitycard_data)
        if identitycard_serializer.is_valid():
            identity=identitycard_serializer.save()
            caad_identity_verification_data = {
                'identity': identity.identity_id,
            }
            caad_identity_verification_serializer = CaadIdentityVerificationSerializer(
                data=caad_identity_verification_data
            )
            if caad_identity_verification_serializer.is_valid():
                caad_identity_verification_serializer.save() 
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method=='PUT':
        identitycard_data=JSONParser().parse(request)
        identitycard=IdentitycardProforma.objects.get(identity_performa_id=identitycard_data['identity_id'])
        identitycard_serializer=IdentitycardProformaSerializer(identitycard,data=identitycard_data)
        if identitycard_serializer.is_valid():
            identitycard_serializer.save()
            return JsonResponse("Updated the identity card successfuly",safe=False)
        return JsonResponse("Failed to update")
    elif request.method=='DELETE':
        identitycard=IdentitycardProforma.objects.get(identity_id=id)
        identitycard.delete()
        return JsonResponse("Deleted identity card Successfully, yay",safe=False)


@csrf_exempt
def CaadIdentityApi(request,id=0):
    if request.method=='GET':
        caadidentity=CaadIdentityVerification.objects.all()
        caadidentity_serializer=CaadIdentityVerificationSerializer(caadidentity,many=True)
        return JsonResponse(caadidentity_serializer.data,safe=False)
    elif request.method=='POST':
        caadidentity_data=JSONParser().parse(request)
        caadidentity_serializer=CaadIdentityVerificationSerializer(data=caadidentity_data)
        if caadidentity_serializer.is_valid():
            caadidentity_serializer.save()
            return JsonResponse("Added a CAAD Identity Verification Successfully",safe=False)
        return JsonResponse("Failed to add CAAD Verification",safe=False)
    elif request.method=='PUT':
        caadidentity_data=JSONParser().parse(request)
        caadidentity=CaadIdentityVerification.objects.get(caad_identity_id=caadidentity_data['caad_identity_id'])
        caadidentity_serializer=CaadIdentityVerificationSerializer(caadidentity,data=caadidentity_data)
        if caadidentity_serializer.is_valid():
            caadidentity_serializer.save()
            return JsonResponse("Updated the caad identity verification successfuly",safe=False)
        return JsonResponse("Failed to update caad identity verification")
    elif request.method=='DELETE':
        caadidentity=CaadIdentityVerification.objects.get(caad_identity_id=id)
        caadidentity.delete()
        return JsonResponse("Deleted caad identity verification Successfully, yay",safe=False)


@csrf_exempt
def LateSittingApi(request,id=0):
    if request.method=='GET':
        latesitting=LateSittingProforma.objects.all()
        latesitting_serializer=LateSittingProformaSerializer(latesitting,many=True)
        return JsonResponse(latesitting_serializer.data,safe=False)
    elif request.method=='POST':
        latesitting_data=JSONParser().parse(request)
        try:
            std_cnic = latesitting_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        internship_id=services.get_internship(std_cnic)
        latesitting_data['internship']=internship_id
        latesitting_serializer=LateSittingProformaSerializer(data=latesitting_data)
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
            return JsonResponse("Added a Late Sitting Form Successfully",safe=False)
        return JsonResponse("Failed to add Late Sitting Form",safe=False)
    elif request.method=='PUT':
        latesitting_data=JSONParser().parse(request)
        latesitting=LateSittingProforma.objects.get(late_form_id=latesitting_data['latesit_id'])
        latesitting_serializer=LateSittingProformaSerializer(latesitting,data=latesitting_data)
        if latesitting_serializer.is_valid():
            latesitting_serializer.save()
            return JsonResponse("Updated the late sitting form successfuly",safe=False)
        return JsonResponse("Failed to update the late sitting form")
    elif request.method=='DELETE':
        latesitting=LateSittingProforma.objects.get(latesit_id=id)
        latesitting.delete()
        return JsonResponse("Deleted the late form Successfully, yay",safe=False)

@csrf_exempt
def CaadLatesittingVerificationApi(request,caad_latesitting_id=0):
    if request.method=="GET":
        CaadLatesittingVerifications_data = CaadLatesittingVerification.objects.all()
        CaadLatesittingVerifications_serializer =CaadLatesittingVerificationSerializer(CaadLatesittingVerifications_data, many=True)
        return JsonResponse(CaadLatesittingVerifications_serializer.data,safe=False)
    elif request.method == 'POST':
        CaadLatesittingVerifications_data=JSONParser().parse(request)
        CaadLatesittingVerifications_serializer = CaadLatesittingVerificationSerializer(data=CaadLatesittingVerifications_data) 
        if CaadLatesittingVerifications_serializer.is_valid():
            CaadLatesittingVerifications_serializer.save()
            return JsonResponse({"message": "Added successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'PUT':
        CaadLatesittingVerifications_data=JSONParser().parse(request)
        CaadLatesittingVerificationsdata=CaadLatesittingVerification.objects.get(caad_latesitting_id=CaadLatesittingVerifications_data['caad_latesitting_id'])
        CaadLatesittingVerifications_serializer = CaadLatesittingVerificationSerializer(CaadLatesittingVerificationsdata,data=CaadLatesittingVerifications_data) 
        if CaadLatesittingVerifications_serializer.is_valid():
            CaadLatesittingVerifications_serializer.save()
            return JsonResponse({"message": "Updated successfully"})
        return JsonResponse("no added sucessfully",safe=False)
    elif request.method == 'DELETE':
        CaadLatesittingVerifications_data=CaadLatesittingVerification.objects.get(caad_latesitting_id=caad_latesitting_id)
        CaadLatesittingVerifications_data.delete()
        return JsonResponse("Deleted sucessfully",safe=False)

@csrf_exempt
def TransportMemFormApi(request,id=0):
    if request.method=='GET':
        transportform=TransportMemberProforma.objects.all()
        transportform_serializer=TransportMemberProformaSerializer(transportform,many=True)
        return JsonResponse(transportform_serializer.data,safe=False)
    elif request.method=='POST':
        transportform_data=JSONParser().parse(request)
        try:
            std_cnic = transportform_data['std_cnic']
        except KeyError:
            return JsonResponse({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        internship_id=services.get_internship(std_cnic)
        identity_id=services.get_identity(internship_id)
        transportform_data['internship'] = internship_id
        transportform_data['identity_card'] = identity_id
        transportform_serializer=TransportMemberProformaSerializer(data=transportform_data)
        if transportform_serializer.is_valid():
            transport=transportform_serializer.save()
            caad_transport_verification_data = {
                'transport_form': transport.transport_form_id,
            }
            caad_transport_verification_serializer = CaadTransportVerificationSerializer(
                data=caad_transport_verification_data
            )
            if caad_transport_verification_serializer.is_valid():
                caad_transport_verification_serializer.save()

            return JsonResponse("Added a Transport Membership Form Successfully",safe=False)
        return JsonResponse("Failed to add Transport Membership Form",safe=False)
    elif request.method=='PUT':
        transportform_data=JSONParser().parse(request)
        transportform=TransportMemberProforma.objects.get(transport_form_id=transportform_data['transport_form_id'])
        transportform_serializer=TransportMemberProformaSerializer(transportform,data=transportform_data)
        if transportform_serializer.is_valid():
            transportform_serializer.save()
            return JsonResponse("Updated the Transport Membership form successfuly",safe=False)
        return JsonResponse("Failed to update the Transport Membership form")
    elif request.method=='DELETE':
        transportform=TransportMemberProforma.objects.get(transport_form_id=id)
        transportform.delete()
        return JsonResponse("Deleted the Transport Form Successfully, yay",safe=False)


@csrf_exempt
def CaadTransportVerificationApi(request,id=0):
    if request.method=='GET':
        transportsect=CaadTransportVerification.objects.all()
        transportsect_serializer=CaadTransportVerificationSerializer(transportsect,many=True)
        return JsonResponse(transportsect_serializer.data,safe=False)
    elif request.method=='POST':
        transportsect_data=JSONParser().parse(request)
        transportsect_serializer=CaadTransportVerificationSerializer(data=transportsect_data)
        if transportsect_serializer.is_valid():
            transportsect_serializer.save()
            return JsonResponse("Added a Transport Section Confirmation Successfully",safe=False)
        return JsonResponse("Failed to add Transport Confirmation",safe=False)
    elif request.method=='PUT':
        transportsect_data=JSONParser().parse(request)
        transportsect=CaadTransportVerification.objects.get(transport_confirmation_id=transportsect_data['transport_confirmation_id'])
        transportsect_serializer=CaadTransportVerificationSerializer(transportsect,data=transportsect_data)
        if transportsect_serializer.is_valid():
            transportsect_serializer.save()
            return JsonResponse("Updated the Transport Section Confirmation successfuly",safe=False)
        return JsonResponse("Failed to update the Transport Section Confirmation")
    elif request.method=='DELETE':
        transportsect=CaadTransportVerification.objects.get(transport_confirmation_id=id)
        transportsect.delete()
        return JsonResponse("Deleted the Transport Section Confirmation Successfully, yay",safe=False)



# Accomodation Proforma API
@api_view(['GET', 'POST','PUT','DELETE'])
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
  

# Accomodation Type API
@api_view(['GET', 'POST','PUT','DELETE'])
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


# Caad Accomodation Verification
@api_view(['GET', 'POST','PUT','DELETE'])
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
@api_view(['GET', 'POST','PUT','DELETE'])
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
@api_view(['GET', 'POST','PUT','DELETE'])
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
#Extension Proforma
@api_view(['GET', 'POST','PUT','DELETE'])
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

#CAAD Extension Proforma Verification
@api_view(['GET', 'POST','PUT','DELETE'])
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

#Login Proforma
@api_view(['GET', 'POST','PUT','DELETE'])
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

#Login Proforma
@api_view(['GET', 'POST','PUT','DELETE'])
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
