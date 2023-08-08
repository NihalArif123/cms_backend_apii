from .models import *
def get_internship(std_cnic):
        try:
            student_registration = StudentRegistration.objects.get(std_cnic=std_cnic)
        except StudentRegistration.DoesNotExist:
           return JsonResponse({"message": "Student registration not found"}, status=404)
        try:
            internship = Internships.objects.get(registration_no=student_registration.reg_form_id)
        except internship.DoesNotExist:
           return JsonResponse({"message": "Internship not found"}, status=404)
        return internship.internship_id


def get_identity(internship_id):
        try:
            identity = IdentitycardProforma.objects.get(internship_id=internship_id)
        except IdentitycardProforma.DoesNotExist:
           return JsonResponse({"message": "Identity not found"}, status=404)
        return identity.identity_id