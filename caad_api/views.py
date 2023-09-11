from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from .models import *
from .serializers import *
from caad_api import services
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import F

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


class login(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cnic = request.data.get('cnic')
            password = request.data.get('password')  # Get the password from the request
            print(cnic)
            try:
                # Query the database to find a user with the provided CNIC and matching password
                user = Student.objects.get(std_cnic=cnic, std_password=password)
                # Return a success response since both CNIC and password match
                return Response({"message": "Login successful","cnic": cnic}, status=200)

            except Student.DoesNotExist:
                # User with the provided CNIC and password doesn't exist, return an error response
                return Response({'error': 'Invalid CNIC or password'}, status=400)
        except Exception as e:
                    return Response({"res": "An error occurred while sending the verification code"}, status=500)
class send_verification_email(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            cnic = request.data.get('cnic')
            std_name = request.data.get('std_name')
            password=request.data.get('password')
            if not email or not cnic or not std_name:
                return Response({"res": "Required data not provided"}, status=400)
            try:
                student = Student.objects.get(std_cnic=cnic)
                print("Student object found:", student)
                if student.verification_status=="true":
                    return Response({"Student Already Exists and Verified"}, status=400)
                else:
                    verification_code = services.generate_verification_code()
                    student.email = email
                    student.verification_code = verification_code
                    student.save()
            except ObjectDoesNotExist:
                verification_code = services.generate_verification_code()
                student = Student(std_email=email, std_cnic=cnic, std_name=std_name, verification_code=verification_code,verification_status="false",std_password=password)
                student.save()
            
            message = f'Your verification code is: {verification_code}'
            send_mail('Verification Code', message, 'caadportal@gmail.com', [email])
            return Response({"res": "Email Sent Successfully"}, status=200)
        except Exception as e:
            return Response({"res": "An error occurred while sending the verification code"}, status=500)
class verify_code(APIView):
    def post(self, request, *args, **kwargs):
        try:
            
            code_to_verify = int(request.data.get('code'))
            cnic=request.data.get('cnic')
            try:
                student = Student.objects.get(std_cnic=cnic)
                print(student.verification_status)
                print("chdc",student.verification_code==code_to_verify)
                if student.verification_code==code_to_verify:
                    student.verification_status="true"
                    print(student.verification_status)
                    student.save()
                    print(student)
                    return Response({"Sign Up Successfull"},status=200)
                else:
                    return Response({"res":"Code does not match.Try again"},status=400)

            except ObjectDoesNotExist:
                    return Response({"res":"student not"},status=400)
        except Exception as e:
             return Response({"res": "An error occurred while verifying the verification code"}, status=500)
class studentApi(APIView):
    # def get(self, request, *args, **kwargs):
    #     students = Student.objects.all()
    #     if not students:
    #         return Response(
    #             {"res": "Students not found"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     students_serializer = StudentSerializer(students,many=True)
    #     return Response(students_serializer.data,status=status.HTTP_200_OK)
    def get(self, request, cnic,*args, **kwargs):
        students= Student.objects.get(std_cnic=cnic)
        if not students:
            return Response(
                {"res": "Students not found"},
                status=400
            )
        students_serializer = StudentSerializer(students)
        return Response(students_serializer.data,status=200)
    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

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
    def get(self, request, cnic,*args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            # Process the student registration data here
            student_reg_serializer = StudentRegistrationSerializer(student_reg)
            return Response(student_reg_serializer.data,status=200)
        except Student.DoesNotExist:
        # Handle the case where the student record doesn't exist
            return Response(
            {"res": "Student not found for CNIC: " + cnic},
            status=404
            )
        except StudentRegistration.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student registration not found for CNIC: " + cnic},
                status=404
            )
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
    def get(self, request, cnic,*args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            Internship_data = Internships.objects.get(registration_no=student_reg)
            Internships_serializer = InternshipsSerializer(Internship_data)
            return Response(Internships_serializer.data,status=200)
        except Student.DoesNotExist:
        # Handle the case where the student record doesn't exist
            return Response(
            {"res": "Student not found for CNIC: " + cnic},
            status=404
            )
        except StudentRegistration.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student registration not found for CNIC: " + cnic},
                status=404
            )
        except Internships.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student Internships not found for CNIC: " + cnic},
                status=404
            )
    
    def post(self, request, *args, **kwargs):
        Internships_data=request.data
        try:
            std_cnic = Internships_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        try:
            student_registration = StudentRegistration.objects.get(std_cnic=std_cnic)
        except StudentRegistration.DoesNotExist:
           return Response({"message": "Student registration not found"}, status=404)
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
        serializer = ClearancePerformaSerializer(instance = ClearancePerforma_data, data=request.data, partial = True)
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
    def get(self, request, cnic,*args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            Internship_data = Internships.objects.get(registration_no=student_reg)
            identity_data = IdentitycardProforma.objects.get(identity_id=Internship_data)
            Identity_serializer = IdentitycardProformaSerializer(identity_data)
            return Response(Identity_serializer.data,status=200)
        except Student.DoesNotExist:
        # Handle the case where the student record doesn't exist
            return Response(
            {"res": "Student not found for CNIC: " + cnic},
            status=404
            )
        except StudentRegistration.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student registration not found for CNIC: " + cnic},
                status=404
            )
        except Internships.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student Internships not found for CNIC: " + cnic},
                status=404
            )
        except IdentitycardProforma.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student Identity not found for CNIC: " + cnic},
                status=404
            )
    
    
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
    # def get(self, request,id,*args, **kwargs):
    #     try:
    #         latesit = LateSittingProforma.objects.select_related(
    #         'internship__registration_no__std_cnic'
    #          ).get(internship__registration_no__std_cnic=id)
        
    #         data = {
    #             'latesit_id': latesit.latesit_id,
    #             'late_performa_submitdate': latesit.late_performa_submitdate,
    #             'latesitting_reason': latesit.latesitting_reason,
    #             'workarea_during_latework': latesit.workarea_during_latework,
    #             'lab_contact_no': latesit.lab_contact_no,
    #             'latesitting_startdate': latesit.latesitting_startdate,
    #             'latesitting_enddate': latesit.latesitting_enddate,
    #             'emergency_contact_name': latesit.emergency_contact_name,
    #             'emergency_contact_number': latesit.emergency_contact_number,
    #             'emergency_contact_landline': latesit.emergency_contact_landline,
    #             'attendant_during_latework': latesit.attendant_during_latework,
    #             'recommended_by_supervisor': latesit.recommended_by_supervisor,
    #             'std_name': latesit.internship.registration_no.std_cnic.std_name,
    #             'std_cnic': latesit.internship.registration_no.std_cnic.std_cnic,
    #             'ncp_assigned_regno': latesit.internship.ncp_assigned_regno,
    #             'std_phone_no': latesit.internship.registration_no.std_cnic.std_phone_no,

    #         # Other fields...
    #     }

    #         return Response(data)
    #     except IdentitycardProforma.DoesNotExist:
    #         return Response({'error': 'Identity card not found'}, status=404)
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
    def get(self, request,id,*args, **kwargs):
        try:
            transport = TransportMemberProforma.objects.select_related(
            'internship__registration_no__std_cnic'
             ).get(internship__registration_no__std_cnic=id)
            identitycard = transport.identity_card.identity_id
            data = {
                'identitycard': identitycard,
                'transport_application_date': transport.transport_application_date,
                'transport_req_start_date': transport.transport_req_start_date,
                'transport_req_end_date' : transport.transport_req_end_date,
                'pick_drop_point': transport.pick_drop_point,
                'lab_contact_no':transport.lab_contact_no,
                'application_status': transport.application_status,
                'std_name': transport.internship.registration_no.std_cnic.std_name,
                'std_phone_no': transport.internship.registration_no.std_cnic.std_phone_no,
                'proposed_research_area': transport.internship.proposed_research_area,
                'ncp_assigned_regno': transport.internship.ncp_assigned_regno,
                'proposed_research_end_time':transport.internship.proposed_research_end_time,
                

            # Other fields...
        }

            return Response(data)
        except IdentitycardProforma.DoesNotExist:
            return Response({'error': 'Identity card not found'}, status=404)


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

# ------------------------------NASIR APIS------------------------------------

class AccomodationProformaApi(APIView):

    def get(self, request,id,*args, **kwargs):
        try:
            accomodation = AccomodationProforma.objects.select_related(
            'internship__registration_no__std_cnic'
             ).get(internship__registration_no__std_cnic=id)
            Identitycard = accomodation.identity_card.identity_id
            data = {
                # 'std_cnic':accomodation.internship.registration_no.std_cnic.std_cnic,
                'std_name': accomodation.internship.registration_no.std_cnic.std_name,
                'ncp_assigned_regno': accomodation.internship.ncp_assigned_regno, 
                'proposed_research_area': accomodation.internship.proposed_research_area,  
                'proposed_research_end_time': accomodation.internship.proposed_research_end_time, 
                'present_university_name': accomodation.internship.registration_no.present_university_name,
                'std_phone_no': accomodation.internship.registration_no.std_cnic.std_phone_no,      
                'landline_no': accomodation.internship.registration_no.landline_no,  
                'identity_no':Identitycard,    
            }
            return Response(data)
        except AccomodationProforma.DoesNotExist:
            return Response({'error': 'Accomodation Proforma not found'}, status=404)

    
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
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        return Response(status=status.HTTP_204_NO_CONTENT)
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
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        return Response(status=status.HTTP_204_NO_CONTENT)
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
            return Response({"message": "Missing std_cnic"}, status=404)

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
        return Response("Deleted sucessfully", safe=False)

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
        return Response("Deleted sucessfully", safe=False)
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
            return Response({"message": "Missing std_cnic"}, status=404)

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
        return Response("Deleted sucessfully", safe=False)


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
        return Response("Deleted sucessfully", safe=False)
#END