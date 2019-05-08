from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Type_of_faculty = (
        ('01', 'วิศวกรรมศาสตร์'),
        ('02', 'สถาปัตยกรรมศาสตร์'),
        ('03', 'ครุศาสตร์อุตสาหกรรมและเทคโนโลยี'),
        ('04', 'เทคโนโลยีการเกษตร'),
        ('05', 'วิทยาศาสตร์'),
        ('06', 'อุตสาหกรรมเกษตร'),
        ('07', 'เทคโนโลยีสารสนเทศ'),
        ('08', 'วิทยาลัยนานาชาติ'),
        ('09', 'วิทยาลัยนาโนเทคโนโลยี'),
        ('10', 'วิทยาลัยนวัตกรรมการผลิตขั้นสูง'),
        ('11', 'การบริหารและจัดการ'),
        ('12', 'วิทยาลัยอุตสาหกรรมการบินนานาชาติ'),
        ('13', 'ศิลปศาสตร์'),
        ('14', 'แพทยศาสตร์'),
        ('15', 'วิทยาลัยวิศวกรรมสังคีต'),
    )

    faculty = models.CharField(max_length=2, choices=Type_of_faculty, default='01')
    age = models.IntegerField(default=0)
    phone = models.CharField(max_length=10)

    TYPE_of_gender = (
        ('01', 'Male'),
        ('02', 'Female')
    )
    gender = models.CharField(max_length=2, choices=TYPE_of_gender, default='01')
    is_unemp = models.BooleanField(default=False)
    def __str__(self):
        return "(%s) %s %s" %(self.user.id, self.user.first_name, self.user.last_name)

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=10)
    company = models.CharField(max_length=255)

    def __str__(self):
        return "(%s) %s %s" %(self.user.id, self.user.first_name, self.user.last_name)

class Job(models.Model):
    create_by = models.ForeignKey(Employer, on_delete=models.CASCADE)

    Type_of_faculty = (
        ('01', 'วิศวกรรมศาสตร์'),
        ('02', 'สถาปัตยกรรมศาสตร์'),
        ('03', 'ครุศาสตร์อุตสาหกรรมและเทคโนโลยี'),
        ('04', 'เทคโนโลยีการเกษตร'),
        ('05', 'วิทยาศาสตร์'),
        ('06', 'อุตสาหกรรมเกษตร'),
        ('07', 'เทคโนโลยีสารสนเทศ'),
        ('08', 'วิทยาลัยนานาชาติ'),
        ('09', 'วิทยาลัยนาโนเทคโนโลยี'),
        ('10', 'วิทยาลัยนวัตกรรมการผลิตขั้นสูง'),
        ('11', 'การบริหารและจัดการ'),
        ('12', 'วิทยาลัยอุตสาหกรรมการบินนานาชาติ'),
        ('13', 'ศิลปศาสตร์'),
        ('14', 'แพทยศาสตร์'),
        ('15', 'วิทยาลัยวิศวกรรมสังคีต'),
        ('16', 'Any'),
    )
    TYPE_of_job = (
        ('01', 'Part-time'),
        ('02', 'Internship')
    )
    TYPE_of_gender = (
        ('01', 'Male'),
        ('02', 'Female'),
        ('03', 'Any')
    )
    job_title = models.TextField()
    faculty = models.CharField(max_length=2, choices=Type_of_faculty, default='03')
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=2, choices=TYPE_of_gender, default='03')
    area = models.TextField()
    salary = models.IntegerField(default=0)
    job_type = models.CharField(max_length=2, choices=TYPE_of_job, default='01')
    def __str__(self):
        return "(โดย %s) %s" %(self.create_by, self.job_title)

class Other(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    requirement = models.CharField(max_length=50)


class Skill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    skill = models.CharField(max_length=50)


class Applied(models.Model):
    applied_job = models.ForeignKey(Job, on_delete=models.CASCADE)

    student_id = models.IntegerField()
