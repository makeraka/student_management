from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomUser (AbstractUser):
    user_type_data = ((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    
# Model de la création d'admin
class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour les staff
class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    adresse = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour les cours
class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour les sujets (matières)
class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    cours_id = models.ForeignKey(Courses, on_delete=models.CASCADE,default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour la création des étudiants dans la base de données pour une gestion automatique
class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    genre = models.CharField(max_length=255)
    profile_pic = models.FileField()
    adresse = models.TextField()
    cours_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour l'attendance
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour le rapport d'attendance
class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour les rapports de congés étudiants
class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.DateField()  # Utilisez DateField pour les dates
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour les rapports de congés du personnel
class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.DateField()  # Utilisez DateField pour les dates
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour les retours étudiants
class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour les retours du personnel
class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()

# Model pour les notifications étudiants
class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Utilisez DateTimeField pour les horodatages
    objects = models.Manager()
    

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender, instance,created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)       
        if instance.user_type==2:
            Staffs.objects.create(admin=instance)
        if instance.user_type==3:
            Students.objects.create(admin=instance,cours_id=Courses.objects.get(id=1),session_start_year="2020-01-01",session_end_year="2021-01-01",adresse="", profile_pic='',genre="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs) :
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()
    
        
    