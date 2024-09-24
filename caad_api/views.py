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
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)
#from PyPDF2 import PdfReader
#import io 
#from django.core.files.uploadedfile import InMemoryUploadedFile

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
                # Create a Student instance with some fields
                student_data = {
                    'std_email': email,
                    'std_cnic': cnic,
                    'std_name': std_name,
                    'verification_code': verification_code,
                    'verification_status': "false",
                    'std_password': password,
                }

                #  student = Student(std_email=email, std_cnic=cnic, std_name=std_name, verification_code=verification_code,verification_status="false",std_password=password)
                student_serializer = StudentSerializer(data=student_data)
                if student_serializer.is_valid():
                    student = student_serializer.save()  # Save the Student object

                else:
                    return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
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

class studentPictures(APIView):
    def get(self, request, cnic, *args, **kwargs):
        try:
        # Fetch the StudentPictures instance for the given CNIC
            stdpics = StudentPictures.objects.filter(std_cnic=cnic)

            if stdpics is not None:
                # Serialize the image data using the serializer
                serializer = StudentPicturesSerializer(stdpics, many=True)

                # Retrieve the serialized data
                serialized_data = serializer.data

                # Get the binary image data from the serialized data
                image_data = serialized_data[0].get('image')

                # Create a response containing the binary image data
                response = Response(serialized_data, status=200)
                response['Content-Type'] = 'application/json'

                return response
            else:
                return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, *args, **kwargs):
        try:
            # If the object doesn't exist, create a new instance
                stdpics=StudentPictures()
                student=Student(std_cnic=request.data.get('std_cnic'))
                stdpics.std_cnic=student
                image = request.FILES['image']
                file_content = image.read()
                stdpics.image= file_content
                stdpics.img_name=request.data.get('img_name')
                serializer = StudentPicturesSerializer(instance=stdpics,data= request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"res": "An error occurred while saving picture"}, status=500)


    def put(self, request, cnic, *args, **kwargs):
        
        stdpics_data = StudentPictures.objects.filter(std_cnic=cnic).first()
        print(stdpics_data.std_cnic)
        if stdpics_data is not None:
            
            image = request.FILES['image']
            file_content = image.read()
            stdpics_data.image= file_content
            stdpics_data.img_name=request.data.get('img_name')

            serializer = StudentPicturesSerializer(instance=stdpics_data,data= request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"res": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class documentsUpload(APIView):
    def get(self, request, cnic, *args, **kwargs):
        try:
        # Fetch the Documents instance for the given CNIC
            docs = DocumentsUpload.objects.filter(std_cnic=cnic)

            if docs is not None:
                # Serialize the image data using the serializer
                serializer = DocumentsUploadSerializer(docs, many=True)

                # Retrieve the serialized data
                serialized_data = serializer.data

                # Get the binary image data from the serialized data
                image_data_list = [item.get('image') for item in serialized_data]


                # Create a response containing the binary image data
                response = Response(serialized_data, status=200)
                response['Content-Type'] = 'application/json'
                return response
            else:
                return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
            try:
                docs_data = DocumentsUpload()
                student = Student(std_cnic=request.data.get('std_cnic'))
                docs_data.std_cnic = student
                image = request.FILES['image']
                if image.content_type == 'application/pdf':
                    pdf_read=image.read()
                    docs_data.image = pdf_read
                else:
                    file_content = image.read()
                    docs_data.image = file_content
                try:
                    document = Documents.objects.get(doc_id=request.data.get('doc'))
                    docs_data.doc = document
                except Documents.DoesNotExist:
                    return Response({'error': 'Document with the given doc_id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

                docs_data.img_name = request.data.get('name')
                docs_data.save()
                serializer = DocumentsUploadSerializer(instance=docs_data, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    def put(self, request, cnic, *args, **kwargs):
        print("put called", cnic)
        docs_data = DocumentsUpload.objects.filter(uploaddoc_id=request.data.get('uploaddoc_id'),std_cnic=cnic).first()

        if docs_data is not None:
            image = request.FILES['image']
            file_content = image.read()
            docs_data.image= file_content
            docs_data.img_name=request.data.get('name')

            serializer = DocumentsUploadSerializer(instance=docs_data,data= request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"res": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class studentApi(APIView):
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
            student = serializer.save()
            print(student.std_cnic)
            
            student_pictures_data = {
                'std_cnic': student.std_cnic,
            }
            
            student_pictures_serializer = StudentPicturesSerializer(
                data=student_pictures_data
            )
            
            if student_pictures_serializer.is_valid():
                student_pictures_serializer.save()
                return Response("Insert Successfully", status=status.HTTP_201_CREATED)
            else:
                # Handle errors for the CaadRegistrationVerification serializer
                return Response("Error in Student Pictures serialization", status=status.HTTP_400_BAD_REQUEST)
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
        student=Student.objects.get(std_cnic=request.data.get('std_cnic'))
        print(request.data)
       # sup_id=UniversitySupervisor.objects.get(supervisor_id=request.data.get('university_supervisor_id'))
        std_reg=StudentRegistration()
        std_reg.std_cnic=student
        #std_reg.university_supervisor=sup_id
        serializer = StudentRegistrationSerializer(instance=std_reg, data=request.data, partial = True)
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
class AdminApi(APIView):
    def get(self, request, cnic,*args, **kwargs):
        students= Admin.objects.get(cnic=cnic)
        if not students:
            return Response(
                {"res": "Admin not found"},
                status=400
            )
        Admin_serializer = AdminSerializer(students)
        return Response(Admin_serializer.data,status=200)
    def post(self, request, *args, **kwargs):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            print(admin.cnic)
            
            # student_pictures_data = {
            #     'std_cnic': student.std_cnic,
            # }
            
            # student_pictures_serializer = StudentPicturesSerializer(
            #     data=student_pictures_data
            # )
            
            # if student_pictures_serializer.is_valid():
            #     student_pictures_serializer.save()
            #     return Response("Insert Successfully", status=status.HTTP_201_CREATED)
            # else:
            #     # Handle errors for the CaadRegistrationVerification serializer
            #     return Response("Error in Student Pictures serialization", status=status.HTTP_400_BAD_REQUEST)
            # return Response("Insert Successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

    def put(self, request, cnic, *args, **kwargs):
        student_data = Admin.objects.get(cnic=cnic)
        if not student_data:
            return Response(
                {"res": "Object  does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AdminSerializer(instance = student_data, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cnic, *args, **kwargs):
        student_data = Admin.objects.get(cnic=cnic)
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
class LoginProformaApi(APIView):

    def get(self, request, cnic=None, *args, **kwargs):
        logger.info(f"Get request with cnic:{cnic}")
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)

    def get_single_entry(self, request, cnic, *args, **kwargs):
        try: 
            logger.info(f"Fetching student with CNIC: {cnic}")
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            login_data = LoginProforma.objects.get(internship_id=internship_data)

            # Serialize and return the data
            login_serializer = LoginProformaSerializer(login_data)
            logger.info(f"login data is here nihal:{login_serializer.data}")
            response_data = login_serializer.data
            response_data['student_name'] = student.std_name
            response_data['std_cnic']=student.std_cnic
            return Response(response_data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"res": f"Student not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except StudentRegistration.DoesNotExist:
            return Response({"res": f"Student registration not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except Internships.DoesNotExist:
            return Response({"res": f"Internships not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except LoginProforma.DoesNotExist:
            return Response({"res": f"LoginProforma data not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"res": "An unexpected error occurred bbnb", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_all_entries(self, request, *args, **kwargs):
        try:
            response_data = []
            students = Student.objects.all()
            for student in students:
                try:
                    student_reg = StudentRegistration.objects.filter(std_cnic=student).first()
                    internship_data = Internships.objects.filter(registration_no=student_reg).first()
                    login_data = LoginProforma.objects.filter(internship_id=internship_data).first()
                    
                    login_serializer = LoginProformaSerializer(login_data)
                    data = login_serializer.data
                    data['student_name'] = student.std_name
                    data['std_cnic']=student.std_cnic
                    response_data.append(data)
                except (StudentRegistration.DoesNotExist, Internships.DoesNotExist, LoginProforma.DoesNotExist):
                    continue

            if response_data:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"res": "No login data found for any student."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"res": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        login_prof_data = request.data
        try:
            std_cnic = login_prof_data['std_cnic']
            student_reg = StudentRegistration.objects.get(std_cnic=std_cnic)
            internship = Internships.objects.get(registration_no=student_reg)

            login_obj = LoginProforma()
            login_obj.internship = internship
            login_prof_serializer = LoginProformaSerializer(instance=login_obj, data=login_prof_data, partial=True)
            if login_prof_serializer.is_valid():
                login = login_prof_serializer.save()

                it_dept_data = {
                    'login_form': login.login_form_id,
                }
                it_dept_serializer = ItDeptLoginSerializer(data=it_dept_data)
                if it_dept_serializer.is_valid():
                    it_dept_serializer.save()

                return Response({"message": "Insert successfully"}, status=status.HTTP_201_CREATED)
            return Response(login_prof_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StudentRegistration.DoesNotExist:
            return Response({"message": f"Student registration not found for CNIC: {std_cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except Internships.DoesNotExist:
            return Response({"message": f"Internship data not found for CNIC: {std_cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"message": "Failed to create login proforma", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, cnic, *args, **kwargs):
        login_prof_data = request.data
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student.std_cnic)
            internship_data = Internships.objects.get(registration_no=student_reg)
            login_data = LoginProforma.objects.get(internship=internship_data)

            login_prof_serializer = LoginProformaSerializer(login_data, data=login_prof_data, partial=True)
            if login_prof_serializer.is_valid():
                login_prof = login_prof_serializer.save()
                if login_prof.application_status.lower() == 'approved':
                    self.enable_forms_for_student(student)
                    self.send_approval_email(student.std_email, student.std_name)
                return Response(login_prof_serializer.data, status=status.HTTP_200_OK)
            return Response(login_prof_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({"res": f"Student not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except StudentRegistration.DoesNotExist:
            return Response({"res": f"Student registration not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except Internships.DoesNotExist:
            return Response({"res": f"Internships not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except LoginProforma.DoesNotExist:
            return Response({"res": f"LoginProforma data not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"res": "An unexpected error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, cnic, *args, **kwargs):
        try:
            login_data = LoginProforma.objects.get(internship__registration_no=StudentRegistration.objects.get(std_cnic=cnic))
            login_data.delete()
            return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
        except LoginProforma.DoesNotExist:
            return Response({"res": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"res": "An unexpected error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_approval_email(self, student_email, student_name):
        subject = 'Login Proforma Approval'
        message = (
            f'Dear {student_name},\n\n'
            'Your login proforma application has been approved.\n\n'
            'Please follow the further instructions provided.\n\n'
            'Thank you.'
        )
        from_email = 'caadportal@gmail.com'
        recipient_list = [student_email]

        send_mail(subject, message, from_email, recipient_list)

    def enable_forms_for_student(self, student):
        try:
            student.forms_enable = True
            student.save()
            logger.info(f"Forms enabled for student CNIC: {student.std_cnic}")
        except Exception as e:
            logger.error(f"Failed to enable forms for student CNIC: {student.std_cnic}. Error: {str(e)}")

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
class Adminlogin(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cnic = request.data.get('cnic')
            password = request.data.get('password')  # Get the password from the request
            print(cnic)
            try:
                # Query the database to find a user with the provided CNIC and id
                user = Admin.objects.get(cnic=cnic, password=password)
                # Return a success response since both CNIC and password match
                return Response({"message": "Login successful","cnic": cnic}, status=200)

            except Admin.DoesNotExist:
                # User with the provided CNIC and password doesn't exist, return an error response
                return Response({'error': 'Invalid CNIC or password'}, status=400)
        except Exception as e:
                    return Response({"res": "An error occurred while sending the verification code"}, status=500)
class InternshipsApi(APIView):
    def get(self, request, cnic=None, *args, **kwargs):
        logger.info(f"Received GET request with CNIC: {cnic}")
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)

    def get_single_entry(self, request, cnic, *args, **kwargs):
        try:
            logger.info(f"Fetching student with CNIC: {cnic}")
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            internship_serializer = InternshipsSerializer(internship_data)
            logger.info(f"Internship data: {internship_serializer.data}")
            return Response(internship_serializer.data, status=200)
        except Student.DoesNotExist:
            return Response({"res": "Student not found for CNIC: " + cnic}, status=404)
        except StudentRegistration.DoesNotExist:
            return Response({"res": "Student registration not found for CNIC: " + cnic}, status=404)
        except Internships.DoesNotExist:
            logger.error(f"Student internships not found for CNIC: {cnic}")
            return Response({"res": "Student Internships not found for CNIC: " + cnic}, status=404)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return Response({"res": "An unexpected error occurred", "error": str(e)}, status=500)

    def get_all_entries(self, request, *args, **kwargs):
        try:
            students = Student.objects.all()
            response_data = []
            for student in students:
                try:
                    student_reg = StudentRegistration.objects.filter(std_cnic=student).first()
                    internship_data = Internships.objects.filter(registration_no=student_reg).first()
                    internship_serializer = InternshipsSerializer(internship_data)
                    response_data.append(internship_serializer.data)
                except StudentRegistration.DoesNotExist:
                    continue
                except Internships.DoesNotExist:
                    continue

            if response_data:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"res": "No internship data found for any student."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"res": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        Internships_data = request.data
        try:
            std_cnic = Internships_data['cnic']
        except KeyError:
            return Response({"message": "Missing 'std_cnic' field in the request data"}, status=400)
        try:
            student_registration = StudentRegistration.objects.get(std_cnic=std_cnic)
        except StudentRegistration.DoesNotExist:
            return Response({"message": "Student registration not found for CNIC: " + std_cnic}, status=404)
        category_name = Internships_data['category']
        try:
            category = HostedresearcherCategory.objects.get(category_name=category_name)
        except HostedresearcherCategory.DoesNotExist:
            return Response({"message": "Category not found"}, status=404)
        university_supervisor = {
            'supervisor_name': Internships_data['supervisor_name'],
            'supervisor_department': Internships_data['supervisor_department'],
            'supervisor_designation': Internships_data['supervisor_designation'],
            'supervisor_email': Internships_data['supervisor_email'],
            'supervisor_fax_no': Internships_data['supervisor_fax_no'],
            'supervisor_phone_no': Internships_data['supervisor_phone_no'],
        }
        uni_supervisor_serializer = UniversitySupervisorSerializer(data=university_supervisor)
        if uni_supervisor_serializer.is_valid():
            university_supervisor = uni_supervisor_serializer.save()
        else:
            return Response("Error in University Supervisor serialization", status=status.HTTP_400_BAD_REQUEST)
            
        new_data = {
            'accomodation_required': Internships_data['accomodation_required'],
            'proposed_research_area': Internships_data['proposed_research_area'],
            'proposed_research_start_time': Internships_data['proposed_research_start_time'],
            'proposed_research_end_time': Internships_data['proposed_research_end_time'],
            'accomodation_start_time': Internships_data['accomodation_start_time'],
            'accomodation_end_time': Internships_data['accomodation_end_time'],
            'proposed_research_department': Internships_data['proposed_research_department'],
            'is_supervisor_from_ncp': Internships_data['is_supervisor_from_ncp'],
            'is_cosupervisor_from_ncp': Internships_data['is_cosupervisor_from_ncp'],
            'consulted_date_of_ncp_supervisor': Internships_data['consulted_date_of_ncp_supervisor'],
            'apply_date': Internships_data['apply_date']
        }
        internship_obj = Internships()
        internship_obj.university_supervisor = university_supervisor
        internship_obj.category = category
        internship_obj.registration_no = student_registration
        internship_obj.ncp_employee_id = "139"
        Internships_serializer = InternshipsSerializer(instance=internship_obj, data=new_data, partial=True)
        if Internships_serializer.is_valid():
            internship = Internships_serializer.save()
            
            caad_registration_verification_data = {
                'internship': internship.internship_id,
            }
            
            caad_registration_verification_serializer = CaadRegistrationVerificationSerializer(
                data=caad_registration_verification_data
            )
            
            if caad_registration_verification_serializer.is_valid():
                caad_registration_verification_serializer.save()
                return Response("Inserted Successfully", status=status.HTTP_201_CREATED)
            else:
                return Response("Error in Caad Registration Verification serialization", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Error in Internships serialization", status=status.HTTP_400_BAD_REQUEST)

    def send_approval_email(self, student_email, student_name):
        subject = 'Fee Submission Reminder!'
        message =  (
        f'Dear {student_name},\n\n'
        'Your internship application has been approved.\n\n'
        'Now you should pay the following dues and submit the challan form.\n\n'
        'i. Registration Fee (Rs. 750/- for Internees students, Rs. 1000/- for M.Phil/Ph.D students, Rs. 1500/- Research Associates & '
        'Post-Doctoral Fellows and Rs. 2000/- for employees of University/R&D Organization and Others from HEC recognized '
        'institutions/Government Departments).\n\n'
        'ii. Security Fee (Rs. 5000/- for internees students, Rs. 10,000/- for M.Phil/MS & Ph.D Student), security fee is refundable upon '
        'completion of research work and subject to submission of Final Clearance Certificate & NCP Identity Card/Entry Card).\n\n'
        'iii. Bench Fee: If the student/parent university institute choose research supervisor from NCP as a co-supervisor, then the bench '
        'fee will be charged (Rs. 4000/- per semester for M.Phil students and Rs. 6000/- per semester for Ph.D student).'
    )
        from_email = 'caadportal@gmail.com'
        recipient_list = [student_email]

        send_mail(subject, message, from_email, recipient_list)

    def put(self, request, cnic, *args, **kwargs):
      try:
        student = Student.objects.get(std_cnic=cnic)
        student_reg = StudentRegistration.objects.get(std_cnic=student)
        internship_data = Internships.objects.get(registration_no=student_reg)

        data = {
            "application_status": request.data.get("application_status", internship_data.application_status),
            "remarks": request.data.get("remarks", internship_data.remarks),
        }
        
        internship_serializer = InternshipsSerializer(internship_data, data=data, partial=True)
        if internship_serializer.is_valid():
            updated_internship = internship_serializer.save()

            # Check if the updated status is 'approved'
            if updated_internship.application_status.lower() == 'Approved':
                # Logic to enable forms here
                self.enable_forms_for_student(student)

                # Optionally send an approval email
                self.send_approval_email(student.std_email, student.std_name)

            return Response(internship_serializer.data, status=status.HTTP_200_OK)
        return Response(internship_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
      except Student.DoesNotExist:
        return Response({"res": "Student not found for CNIC: " + cnic}, status=status.HTTP_404_NOT_FOUND)
      except StudentRegistration.DoesNotExist:
        return Response({"res": "Student registration not found for CNIC: " + cnic}, status=status.HTTP_404_NOT_FOUND)
      except Internships.DoesNotExist:
        return Response({"res": "Student internships not found for CNIC: " + cnic}, status=status.HTTP_404_NOT_FOUND)
      except Exception as e:
        logger.error(f"Error during update: {str(e)}")
        return Response({"res": "An unexpected error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def enable_forms_for_student(self, student):
    try:
        # Assuming formsenable is a field or a related setting that needs to be updated
        # This is just a placeholder and should be replaced with actual model and field names
        student.forms_enable = True
        student.save()
        logger.info(f"Forms enabled for student CNIC: {student.std_cnic}")
    except Exception as e:
        logger.error(f"Failed to enable forms for student {student.std_cnic}: {str(e)}")

    def delete(self, request, cnic, *args, **kwargs):
        try:
            internship_data = Internships.objects.get(internship_id=cnic)
            if not internship_data:
                return Response({"res": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            internship_data.delete()
            return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
        except Internships.DoesNotExist:
            return Response({"res": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
class IdentitycardApi(APIView):
    def get(self, request, cnic=None, *args, **kwargs):
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)

    def get_single_entry(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            identity_data = IdentitycardProforma.objects.get(internship_id=internship_data)
            Identity_serializer = IdentitycardProformaSerializer(identity_data)
            
            # Add student name to the response
            response_data = Identity_serializer.data
            response_data['std_name'] = student.std_name
            response_data['std_cnic'] = student.std_cnic

            return Response(response_data, status=200)
        except Student.DoesNotExist:
            return Response({"res": "Student not found for CNIC: " + cnic}, status=404)
        except StudentRegistration.DoesNotExist:
            return Response({"res": "Student registration not found for CNIC: " + cnic}, status=404)
        except Internships.DoesNotExist:
            return Response({"res": "Student internships not found for CNIC: " + cnic}, status=404)
        except IdentitycardProforma.DoesNotExist:
            return Response({"res": "Student identity card proforma not found for CNIC: " + cnic}, status=404)

    def get_all_entries(self, request, *args, **kwargs):
        try:
            identity_data_list = IdentitycardProforma.objects.all()
            response_data = []

            for identity_data in identity_data_list:
                internship_data = identity_data.internship
                student_reg = internship_data.registration_no
                student = student_reg.std_cnic
                
                identity_serializer = IdentitycardProformaSerializer(identity_data)
                identity_data_response = identity_serializer.data
                identity_data_response['std_name'] = student.std_name
                identity_data_response['std_cnic'] = student.std_cnic
                response_data.append(identity_data_response)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, *args, **kwargs):
        identity_data = request.data
        print(identity_data)
        try:
            std_cnic = identity_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)

        internship=services.get_internship(std_cnic)
        identity_obj=IdentitycardProforma()
        identity_obj.internship= internship
        identity_serializer = IdentitycardProformaSerializer(instance=identity_obj,data=identity_data,partial=True)
        if identity_serializer.is_valid():
            identity=identity_serializer.save()
            caad_identity_verification_data = {
                'identity': identity.identity_id,
            }
            caad_identity_verification_serializer =CaadIdentityVerificationSerializer(
                data=caad_identity_verification_data
            )
            if caad_identity_verification_serializer.is_valid():
                caad_identity_verification_serializer.save() 
                return Response("Insert Successfully", status=status.HTTP_201_CREATED)
            else:
                # Handle errors for the CaadRegistrationVerification serializer
                return Response("Error in CaadIdentityVerification serialization", status=status.HTTP_400_BAD_REQUEST)
          
        return Response(identity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    
    def put(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            identity_data = IdentitycardProforma.objects.get(internship_id=internship_data)
            
            # Update only application_status and remarks fields from request data
            data = {
                "application_status": request.data.get("application_status", identity_data.application_status),
                "remarks": request.data.get("remarks", identity_data.remarks),
            }
            
            identity_serializer = IdentitycardProformaSerializer(identity_data, data=data, partial=True)
            if identity_serializer.is_valid():
                identity_serializer.save()
                return Response(identity_serializer.data, status=status.HTTP_200_OK)
            return Response(identity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Student.DoesNotExist:
            return Response(
                {"res": "Student not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except StudentRegistration.DoesNotExist:
            return Response(
                {"res": "Student registration not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except Internships.DoesNotExist:
            return Response(
                {"res": "Student internships not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except IdentitycardProforma.DoesNotExist:
            return Response(
                {"res": "Student identity card proforma not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
    
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




class EvaluationProformaApi(APIView):
    def get(self, request, cnic=None, *args, **kwargs):
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)

    def get_single_entry(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            evaluation_data = EvaluationProforma.objects.get(internship_id=internship_data)
            evaluation_serializer = EvaluationProformaSerializer(evaluation_data)

            # Add student name to the response
            response_data = evaluation_serializer.data
            response_data['std_name'] = student.std_name
            response_data['std_cnic'] = student.std_cnic

            return Response(response_data, status=200)
        except Student.DoesNotExist:
            return Response({"res": "Student not found for CNIC: " + cnic}, status=404)
        except StudentRegistration.DoesNotExist:
            return Response({"res": "Student registration not found for CNIC: " + cnic}, status=404)
        except Internships.DoesNotExist:
            return Response({"res": "Student internships not found for CNIC: " + cnic}, status=404)
        except EvaluationProforma.DoesNotExist:
            return Response({"res": "Student evaluation proforma not found for CNIC: " + cnic}, status=404)

    def get_all_entries(self, request, *args, **kwargs):
        try:
            evaluation_data_list = EvaluationProforma.objects.all()
            response_data = []

            for evaluation_data in evaluation_data_list:
                internship_data = evaluation_data.internship
                student_reg = internship_data.registration_no
                student = student_reg.std_cnic

                evaluation_serializer = EvaluationProformaSerializer(evaluation_data)
                evaluation_data_response = evaluation_serializer.data
                evaluation_data_response['std_name'] = student.std_name
                evaluation_data_response['std_cnic'] = student.std_cnic
                response_data.append(evaluation_data_response)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        evaluation_data = request.data
        try:
            std_cnic = evaluation_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)

        internship = services.get_internship(std_cnic)
        eval_obj = EvaluationProforma(internship=internship)
        evaluation_serializer = EvaluationProformaSerializer(instance=eval_obj, data=evaluation_data, partial=True)
        if evaluation_serializer.is_valid():
            evaluation = evaluation_serializer.save()

            # Create and save CAAD evaluation verification
            caad_evaluation_verification_data = {
                'evaluation': evaluation.evaluation_id,
            }
            caad_evaluation_verification_serializer = CaadEvaluationVerificationSerializer(
                data=caad_evaluation_verification_data
            )
            if caad_evaluation_verification_serializer.is_valid():
                caad_evaluation_verification_serializer.save()
                return Response("Insert Successfully", status=status.HTTP_201_CREATED)
            else:
                return Response("Error in CaadEvaluationVerification serialization", status=status.HTTP_400_BAD_REQUEST)

        return Response(evaluation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            evaluation_data = EvaluationProforma.objects.get(internship_id=internship_data)

            # Update only research_status and research_summary fields from request data
            data = {
                "research_status": request.data.get("research_status", evaluation_data.research_status),
                "research_summary": request.data.get("research_summary", evaluation_data.research_summary),
            }

            evaluation_serializer = EvaluationProformaSerializer(evaluation_data, data=data, partial=True)
            if evaluation_serializer.is_valid():
                evaluation_serializer.save()
                return Response(evaluation_serializer.data, status=status.HTTP_200_OK)
            return Response(evaluation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Student.DoesNotExist:
            return Response(
                {"res": "Student not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except StudentRegistration.DoesNotExist:
            return Response(
                {"res": "Student registration not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except Internships.DoesNotExist:
            return Response(
                {"res": "Student internships not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except EvaluationProforma.DoesNotExist:
            return Response(
                {"res": "Student evaluation proforma not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            evaluation = EvaluationProforma.objects.get(pk=pk)
        except EvaluationProforma.DoesNotExist:
            return Response(
                {"res": "Evaluation Proforma not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        evaluation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    def get(self, request, cnic=None, *args, **kwargs):
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)

    def get_single_entry(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            clearance_data = ClearancePerforma.objects.get(internship_id=internship_data)
            clearance_serializer = ClearancePerformaSerializer(clearance_data)
            
            # Add student name to the response
            response_data = clearance_serializer.data
            response_data['std_name'] = student.std_name
            response_data['std_cnic'] = student.std_cnic

            return Response(response_data, status=200)
        except Student.DoesNotExist:
            return Response({"res": "Student not found for CNIC: " + cnic}, status=404)
        except StudentRegistration.DoesNotExist:
            return Response({"res": "Student registration not found for CNIC: " + cnic}, status=404)
        except Internships.DoesNotExist:
            return Response({"res": "Student internships not found for CNIC: " + cnic}, status=404)
        except ClearancePerforma.DoesNotExist:
            return Response({"res": "Student clearance request not found for CNIC: " + cnic}, status=404)

    def get_all_entries(self, request, *args, **kwargs):
        try:
            clearance_data_list = ClearancePerforma.objects.all()
            response_data = []

            for clearance_data in clearance_data_list:
                internship_data = clearance_data.internship
                student_reg = internship_data.registration_no
                student = student_reg.std_cnic
                
                clearance_serializer = ClearancePerformaSerializer(clearance_data)
                clearance_data_response = clearance_serializer.data
                clearance_data_response['std_name'] = student.std_name
                clearance_data_response['std_cnic'] = student.std_cnic
                response_data.append(clearance_data_response)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, *args, **kwargs):
        clearance_data = request.data
        print(clearance_data)
        try:
            std_cnic = clearance_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)

        internship = services.get_internship(std_cnic)
        clearance_obj = ClearancePerforma(internship=internship)
        clearance_serializer = ClearancePerformaSerializer(instance=clearance_obj, data=clearance_data, partial=True)
        
        if clearance_serializer.is_valid():
            clearance = clearance_serializer.save()

            caadclearance_data = {'clearance': clearance.clearance_id}
            caadclearance_serializer = CaadClearanceVerificationSerializer(data=caadclearance_data)

            if caadclearance_serializer.is_valid():
                caadclearance_serializer.save()
                return Response("Insert Successfully", status=status.HTTP_201_CREATED)
            else:
                clearance.delete()
                return Response("Error in CaadClearanceVerification serialization", status=status.HTTP_400_BAD_REQUEST)

        return Response(clearance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            clearance_data = ClearancePerforma.objects.get(internship_id=internship_data)
            
            # Update only application_status and remarks fields from request data
            data = {
                "application_status": request.data.get("application_status", clearance_data.application_status),
                "remarks": request.data.get("remarks", clearance_data.remarks),
            }
            
            clearance_serializer = ClearancePerformaSerializer(clearance_data, data=data, partial=True)
            if clearance_serializer.is_valid():
                clearance_serializer.save()
                return Response(clearance_serializer.data, status=status.HTTP_200_OK)
            return Response(clearance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Student.DoesNotExist:
            return Response(
                {"res": "Student not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except StudentRegistration.DoesNotExist:
            return Response(
                {"res": "Student registration not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except Internships.DoesNotExist:
            return Response(
                {"res": "Student internships not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except ClearancePerforma.DoesNotExist:
            return Response(
                {"res": "Student clearance request not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            clearance = ClearancePerforma.objects.get(pk=pk)
        except ClearancePerforma.DoesNotExist:
            return Response(
                {"res": "Clearance request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        clearance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        caadidentity_serializer = CaadIdentityVerificationSerializer(data=caadidentity_data)
        if caadidentity_serializer.is_valid():
            caadidentity_serializer.save()
            return Response(caadidentity_serializer.data, status=status.HTTP_201_CREATED)
        return Response(caadidentity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        try:
            caadidentity = CaadIdentityVerification.objects.get(identity_id=id)
            print(request.data)
            print(caadidentity)
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
    def get(self, request, cnic=None, *args, **kwargs):
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)

    def get_single_entry(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            internship_data = Internships.objects.get(registration_no=student_reg)
            sitting_data = LateSittingProforma.objects.get(internship_id=internship_data)
            sitting_serializer = LateSittingProformaSerializer(sitting_data)
            
            # Add student name and CNIC to the response
            response_data = sitting_serializer.data
            response_data['std_name'] = student.std_name
            response_data['std_cnic'] = student.std_cnic

            return Response(response_data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"res": "Student not found for CNIC: " + cnic}, status=status.HTTP_404_NOT_FOUND)
        except StudentRegistration.DoesNotExist:
            return Response({"res": "Student registration not found for CNIC: " + cnic}, status=status.HTTP_404_NOT_FOUND)
        except Internships.DoesNotExist:
            return Response({"res": "Student internships not found for CNIC: " + cnic}, status=status.HTTP_404_NOT_FOUND)
        except LateSittingProforma.DoesNotExist:
            return Response({"res": "Student late sitting request not found for CNIC: " + cnic}, status=status.HTTP_404_NOT_FOUND)

    def get_all_entries(self, request, *args, **kwargs):
        try:
            late_sitting_data_list = LateSittingProforma.objects.all()
            response_data = []

            for sitting_data in late_sitting_data_list:
                internship_data = sitting_data.internship
                student_reg = internship_data.registration_no
                student = student_reg.std_cnic
                
                sitting_serializer = LateSittingProformaSerializer(sitting_data)
                sitting_data_response = sitting_serializer.data
                sitting_data_response['std_name'] = student.std_name
                sitting_data_response['std_cnic'] = student.std_cnic
                response_data.append(sitting_data_response)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        late_sitting_data = request.data
        print(late_sitting_data)
        try:
            std_cnic = late_sitting_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            internship = services.get_internship(std_cnic)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        late_sitting_obj = LateSittingProforma()
        late_sitting_obj.internship = internship
        late_sitting_serializer = LateSittingProformaSerializer(instance=late_sitting_obj, data=late_sitting_data, partial=True)
        
        if late_sitting_serializer.is_valid():
            late_sitting = late_sitting_serializer.save()
            caad_late_sitting_verification_data = {
                'latesit': late_sitting.latesit_id,
            }
            caad_late_sitting_verification_serializer = CaadLatesittingVerificationSerializer(
                data=caad_late_sitting_verification_data
            )
            if caad_late_sitting_verification_serializer.is_valid():
                caad_late_sitting_verification_serializer.save()
                return Response(late_sitting_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(caad_late_sitting_verification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(late_sitting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            late_sitting = LateSittingProforma.objects.get(pk=pk)
        except LateSittingProforma.DoesNotExist:
            return Response({"res": "Late Sitting Proforma not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "application_status": request.data.get("application_status", late_sitting.application_status),
            "remarks": request.data.get("remarks", late_sitting.remarks),
        }
        
        late_sitting_serializer = LateSittingProformaSerializer(late_sitting, data=data, partial=True)
        if late_sitting_serializer.is_valid():
            late_sitting_serializer.save()
            return Response(late_sitting_serializer.data, status=status.HTTP_200_OK)
        return Response(late_sitting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            late_sitting = LateSittingProforma.objects.get(pk=pk)
        except LateSittingProforma.DoesNotExist:
            return Response({"res": "Late Sitting Proforma not found"}, status=status.HTTP_404_NOT_FOUND)
        
        late_sitting.delete()
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
    def get(self, request, cnic,*args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            Internship_data = Internships.objects.get(registration_no=student_reg)
            transport_data = TransportMemberProforma.objects.get(internship_id=Internship_data)
            tansport_serializer = TransportMemberProformaSerializer(transport_data)
            return Response(tansport_serializer.data,status=200)
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
        except TransportMemberProforma.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student Transport Request not found for CNIC: " + cnic},
                status=404
            )

    def post(self, request, *args, **kwargs):
        transport_data = request.data
        try:
            std_cnic = transport_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)
        internship=services.get_internship(std_cnic)
        identity=services.get_identity(internship.internship_id)
        transport_obj=TransportMemberProforma()
        transport_obj.internship=internship
        transport_obj.identity=identity
        transportform_serializer = TransportMemberProformaSerializer(instance =transport_obj, data=transport_data, partial=True)
        if transportform_serializer.is_valid():
            transport=transportform_serializer.save()
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

    def get(self, request,cnic=None ,*args, **kwargs):
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)
    def get_single_entry(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            Internship_data = Internships.objects.get(registration_no=student_reg)
            accomodation_data = AccomodationProforma.objects.get(internship_id=Internship_data)
            acc_serializer = AccomodationProformaSerializer(accomodation_data)
            
            response_data = acc_serializer.data
            response_data['std_name'] = student.std_name
            response_data['std_cnic'] = student.std_cnic

            return Response(response_data,status=200)
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
        except AccomodationProforma.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student accommodation not found for CNIC: " + cnic},
                status=404
            )
    def get_all_entries(self, request, *args, **kwargs):
        try:
            acc_data_list = AccomodationProforma.objects.all()
            response_data = []

            for accomodation_data in acc_data_list:
                internship_data = accomodation_data.internship
                student_reg = internship_data.registration_no
                student = student_reg.std_cnic
                
                acc_serializer = AccomodationProformaSerializer(accomodation_data)
                acc_data_response = acc_serializer.data
                acc_data_response['std_name'] = student.std_name
                acc_data_response['std_cnic'] = student.std_cnic
                response_data.append(acc_data_response)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        except AccomodationProforma.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student accommodation not found for CNIC: " + cnic},
                status=404
            )
    def post(self, request, *args, **kwargs):
        accomodation_prof_data = request.data
        print( accomodation_prof_data)
        try:
            std_cnic = accomodation_prof_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=400)

        internship=services.get_internship(std_cnic)
        identity=services.get_identity(internship.internship_id)
        acc_obj=AccomodationProforma()
        acc_obj.internship=internship
        acc_obj.identity=identity
        accomodation_prof_serializer = AccomodationProformaSerializer(instance =acc_obj, data=accomodation_prof_data, partial=True)
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
   
    def put(self, request,  *args, **kwargs):
        try:
           student = Student.objects.get(std_cnic=cnic)
           student_reg = StudentRegistration.objects.get(std_cnic=student)
           internship_data = Internships.objects.get(registration_no=student_reg)
           accomodation_prof_data = request.data
           accomodation_prof = AccomodationProforma.objects.get(pk=pk)
           data = {
                "application_status": request.data.get("application_status", identity_data.application_status),
                "remarks": request.data.get("remarks", accomodation_prof.remarks),
           }
           
           accomodation_prof_serializer = AccomodationProformaSerializer(accomodation_prof, data=accomodation_prof_data)
           if accomodation_prof_serializer.is_valid():
            accomodation_prof_serializer.save()
            return Response({"message": "Updated successfully"})
           return Response(accomodation_prof_serializer.errors, status=400)
        except Student.DoesNotExist:
            return Response(
                {"res": "Student not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except StudentRegistration.DoesNotExist:
            return Response(
                {"res": "Student registration not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except Internships.DoesNotExist:
            return Response(
                {"res": "Student internships not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
        except IdentitycardProforma.DoesNotExist:
            return Response(
                {"res": "Student identity card proforma not found for CNIC: " + cnic},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, pk):
        accomodation_prof = AccomodationProforma.objects.get(pk=pk)
        accomodation_prof.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# End here Accomodation Proforma API
  
class NcpPublications(APIView):

    def get(self, request, cnic=None, *args, **kwargs):
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)

    def get_single_entry(self, request, cnic, *args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            evaluation_data = EvaluationProforma.objects.get(registration_no=student_reg)
            publication_data = NcpPublications.objects.get(evaluation=evaluation_data)
            
            pub_serializer = NcpPublicationsSerializer(publication_data)
            response_data = pub_serializer.data
            response_data['std_name'] = student.std_name
            response_data['std_cnic'] = student.std_cnic

            return Response(response_data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"res": f"Student not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except StudentRegistration.DoesNotExist:
            return Response({"res": f"Student registration not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except EvaluationProforma.DoesNotExist:
            return Response({"res": f"Evaluation proforma not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except NcpPublications.DoesNotExist:
            return Response({"res": f"NCP publications not found for CNIC: {cnic}"}, status=status.HTTP_404_NOT_FOUND)

    def get_all_entries(self, request, *args, **kwargs):
        try:
            publication_data_list = NcpPublications.objects.all()
            response_data = []

            for publication_data in publication_data_list:
                evaluation_data = publication_data.evaluation
                student_reg = evaluation_data.registration_no
                student = student_reg.std_cnic

                pub_serializer = NcpPublicationsSerializer(publication_data)
                pub_data_response = pub_serializer.data
                pub_data_response['std_name'] = student.std_name
                pub_data_response['std_cnic'] = student.std_cnic
                response_data.append(pub_data_response)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        publication_data = request.data
        try:
            std_cnic = publication_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(std_cnic=std_cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            evaluation_data = EvaluationProforma.objects.get(registration_no=student_reg)
            
            pub_obj = NcpPublications(evaluation=evaluation_data)
            pub_serializer = NcpPublicationsSerializer(instance=pub_obj, data=publication_data, partial=True)
            
            if pub_serializer.is_valid():
                pub_serializer.save()
                return Response({"message": "Insert successfully"}, status=status.HTTP_201_CREATED)
            return Response(pub_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({"res": f"Student not found for CNIC: {std_cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except StudentRegistration.DoesNotExist:
            return Response({"res": f"Student registration not found for CNIC: {std_cnic}"}, status=status.HTTP_404_NOT_FOUND)
        except EvaluationProforma.DoesNotExist:
            return Response({"res": f"Evaluation proforma not found for CNIC: {std_cnic}"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        try:
            publication_data = NcpPublications.objects.get(pk=pk)
            pub_serializer = NcpPublicationsSerializer(publication_data, data=request.data, partial=True)
            
            if pub_serializer.is_valid():
                pub_serializer.save()
                return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
            return Response(pub_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NcpPublications.DoesNotExist:
            return Response({"res": "NCP publications not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        try:
            publication_data = NcpPublications.objects.get(pk=pk)
            publication_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NcpPublications.DoesNotExist:
            return Response({"res": "NCP publications not found"}, status=status.HTTP_404_NOT_FOUND)
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
    def get(self, request, cnic,*args, **kwargs):
        try:
            student = Student.objects.get(std_cnic=cnic)
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            Internship_data = Internships.objects.get(registration_no=student_reg)
            extension_data = ExtensionProforma.objects.get(internship_id=Internship_data)
            ext_serializer = ExtensionProformaSerializer(extension_data)
            return Response(ext_serializer.data,status=200)
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
        except ExtensionProforma.DoesNotExist:
            # Handle the case where the record doesn't exist
            return Response(
                {"res": "Student extension not found for CNIC: " + cnic},
                status=404
            )

    def post(self, request):
        extension_prof_data = request.data
        print(extension_prof_data)
        try:
            std_cnic = extension_prof_data['std_cnic']
        except KeyError:
            return Response({"message": "Missing std_cnic"}, status=404)

        internship = services.get_internship(std_cnic)
        ex_obj=ExtensionProforma()
        ex_obj.internship=internship
        extension_prof_serializer = ExtensionProformaSerializer(instance =ex_obj, data=extension_prof_data, partial=True)
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




class ApplicationStatsApi(APIView):
    def get(self, request, *args, **kwargs):
        stats = {}

        # ID Card Applications
        stats['identitycard'] = {
            'totalapp': IdentitycardProforma.objects.count(),
            'accapp': IdentitycardProforma.objects.filter(application_status='accepted').count(),
            'rejapp': IdentitycardProforma.objects.filter(application_status='rejected').count(),
            'pendapp': IdentitycardProforma.objects.filter(application_status='pending').count(),
        }

        # Internship Applications
        stats['internships'] = {
            'totalapp': Internships.objects.count(),
            'accapp': Internships.objects.filter(application_status='accepted').count(),
            'rejapp': Internships.objects.filter(application_status='rejected').count(),
            'pendapp': Internships.objects.filter(application_status='pending').count(),
        }

        # Add similar logic for other application types if needed

        return Response(stats)
    

import logging

logger = logging.getLogger(__name__)

class NcpDuesApi(APIView):

    def get(self, request, cnic=None, *args, **kwargs):
        logger.info(f"Received GET request with CNIC: {cnic}")
        if cnic:
            return self.get_single_entry(request, cnic, *args, **kwargs)
        else:
            return self.get_all_entries(request, *args, **kwargs)

    def get_single_entry(self, request, cnic, *args, **kwargs):
        try:
            logger.info(f"Fetching Ncp Dues for CNIC: {cnic}")
            student = Student.objects.get(std_cnic=cnic)
            logger.debug(f"Found student: {student}")
            student_reg = StudentRegistration.objects.get(std_cnic=student)
            logger.debug(f"Found student registration: {student_reg}")
            internship_data = Internships.objects.get(registration_no=student_reg)
            logger.debug(f"Found internship data: {internship_data}")
            dues_data = NcpDues.objects.get(internship_id=internship_data)
            logger.debug(f"Found dues data: {dues_data}")
            dues_serializer = NcpDuesSerializer(dues_data)
            logger.info(f"Dues data serialized: {dues_serializer.data}")
            response_data = dues_serializer.data
            response_data['std_name'] = student.std_name
            response_data['std_cnic'] = student.std_cnic
            return Response(response_data, status=200)
        except Student.DoesNotExist:
            logger.error(f"Student not found for CNIC: {cnic}")
            return Response({"res": "Student not found for CNIC: " + cnic}, status=404)
        except NcpDues.DoesNotExist:
            logger.error(f"Ncp Dues not found for CNIC: {cnic}")
            return Response({"res": "Ncp Dues not found for CNIC: " + cnic}, status=404)
        except Exception as e:
            logger.error(f"An unexpected error occurred during GET single entry: {str(e)}", exc_info=True)
            return Response({"res": "An unexpected error occurred", "error": str(e)}, status=500)

    def get_all_entries(self, request, *args, **kwargs):
        try:
            logger.info("Fetching all Ncp Dues entries")
            dues_data_list = NcpDues.objects.all()
            response_data = []
            for dues_data in dues_data_list:
                internship_data = dues_data.internship
                student_reg = internship_data.registration_no
                student = student_reg.std_cnic   
                logger.debug(f"Processing dues data for student: {student}")
                dues_serializer = NcpDuesSerializer(dues_data)
                dues_data_response = dues_serializer.data
                dues_data_response['std_name'] = student.std_name
                dues_data_response['std_cnic'] = student.std_cnic
                response_data.append(dues_data_response)
            logger.info(f"Fetched {len(dues_data_list)} Ncp Dues entries")
            return Response(response_data, status=200)
        except Exception as e:
            logger.error(f"An unexpected error occurred during GET all entries: {str(e)}", exc_info=True)
            return Response({"res": "An unexpected error occurred", "error": str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            dues_data = request.data
            logger.debug(f"Received Ncp Dues data for posting: {dues_data}")
            std_cnic = dues_data.get('std_cnic')
            if not std_cnic:
                logger.error("Missing 'std_cnic' field in the request data")
                return Response({"message": "Missing 'std_cnic' field in the request data"}, status=400)
            
            internship = services.get_internship(std_cnic)
            if not internship:
                logger.error(f"Internship not found for CNIC: {std_cnic}")
                return Response({"res": "Internship not found for CNIC: " + std_cnic}, status=404)
            
            dues_obj = NcpDues()
            dues_obj.internship = internship
            dues_serializer = NcpDuesSerializer(data=dues_data, partial=True)
            if dues_serializer.is_valid():
                dues_serializer.save()
                logger.info("Ncp Dues entry created successfully.")
                return Response("Inserted Successfully", status=201)
            else:
                logger.error(f"Error in Ncp Dues data: {dues_serializer.errors}")
                return Response(dues_serializer.errors, status=400)
        except Exception as e:
            logger.error(f"An unexpected error occurred during POST: {str(e)}", exc_info=True)
            return Response({"res": "An unexpected error occurred", "error": str(e)}, status=500)

    def put(self, request, cnic, *args, **kwargs):
        try:
            logger.info(f"Received PUT request for CNIC: {cnic}")
            student = Student.objects.get(std_cnic=cnic)
            logger.debug(f"Found student: {student}")
            dues_data = NcpDues.objects.get(internship_id=student.std_cnic)
            logger.debug(f"Found dues data: {dues_data}")

            data = {
                "application_status": request.data.get("application_status", dues_data.application_status),
                "remarks": request.data.get("remarks", dues_data.remarks),
            }
            
            dues_serializer = NcpDuesSerializer(dues_data, data=data, partial=True)
            if dues_serializer.is_valid():
                updated_dues = dues_serializer.save()
                logger.info("Ncp Dues updated successfully.")
                return Response(dues_serializer.data, status=200)
            else:
                logger.error(f"Error in Ncp Dues update: {dues_serializer.errors}")
                return Response(dues_serializer.errors, status=400)
        except Student.DoesNotExist:
            logger.error(f"Student not found for CNIC: {cnic}")
            return Response({"res": "Student not found for CNIC: " + cnic}, status=404)
        except NcpDues.DoesNotExist:
            logger.error(f"Ncp Dues not found for CNIC: {cnic}")
            return Response({"res": "Ncp Dues not found for CNIC: " + cnic}, status=404)
        except Exception as e:
            logger.error(f"An unexpected error occurred during PUT: {str(e)}", exc_info=True)
            return Response({"res": "An unexpected error occurred", "error": str(e)}, status=500)

    def delete(self, request, cnic, *args, **kwargs):
        try:
            logger.info(f"Received DELETE request for CNIC: {cnic}")
            student = Student.objects.get(std_cnic=cnic)
            logger.debug(f"Found student: {student}")
            dues_data = NcpDues.objects.get(internship_id=student.std_cnic)
            logger.debug(f"Found dues data: {dues_data}")
            dues_data.delete()
            logger.info("Ncp Dues deleted successfully.")
            return Response(status=204)
        except Student.DoesNotExist:
            logger.error(f"Student not found for CNIC: {cnic}")
            return Response({"res": "Student not found for CNIC: " + cnic}, status=404)
        except NcpDues.DoesNotExist:
            logger.error(f"Ncp Dues not found for CNIC: {cnic}")
            return Response({"res": "Ncp Dues not found for CNIC: " + cnic}, status=404)
        except Exception as e:
            logger.error(f"An unexpected error occurred during DELETE: {str(e)}", exc_info=True)
            return Response({"res": "An unexpected error occurred", "error": str(e)}, status=500)
