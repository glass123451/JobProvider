# Register Form
from django import forms
from django.contrib.auth.models import User

from jobprovider.models import Employer


class RegisterStudentForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

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

    Type_of_gender = (
        ('01', 'Male'),
        ('02', 'Female')
    )

    age = forms.IntegerField(required=True)
    gender = forms.CharField(widget=forms.Select(choices=Type_of_gender))
    phone = forms.CharField(max_length=10)
    faculty = forms.CharField(widget=forms.Select(choices=Type_of_faculty))
    def clean(self):
        clean_data = super().clean()
        username = clean_data.get('username')
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        age = clean_data.get('age')
        if len(username) < 6:
            raise forms.ValidationError('Username ต้องมากกว่า 6 ตัวอักษร')
        elif len(password) < 6:
            raise forms.ValidationError('รหัสผ่าน ต้องมากกว่า 6 ตัวอักษร')
        elif len(username) > 15:
            raise forms.ValidationError('Username ต้องอยู่ระหว่าง 6-15')
        elif age < 10:
            raise forms.ValidationError('อายุของนักศึกษาห้ามต่ำกว่า 10 ปี')

        elif password != confirm_password:
            raise forms.ValidationError('รหัสผ่าน กับ ยืนยันรหัสผ่าน ไม่ตรงกัน')

class RegisterEmployerForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    phone = forms.CharField(max_length=10)
    company = forms.CharField(max_length=100, required=False)

    def clean(self):
        clean_data = super().clean()
        username = clean_data.get('username')
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if len(username) < 6:
            raise forms.ValidationError('Username ต้องมากกว่า 6 ตัวอักษร')
        elif len(password) < 6:
            raise forms.ValidationError('รหัสผ่าน ต้องมากกว่า 6 ตัวอักษร')
        elif len(username) > 15:
            raise forms.ValidationError('Username ต้องอยู่ระหว่าง 6-15')

        elif password != confirm_password:
            raise forms.ValidationError('รหัสผ่าน กับ ยืนยันรหัสผ่าน ไม่ตรงกัน')

class EditEmployerForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)
    company = forms.CharField(max_length=100, required=False)

class JobForm(forms.Form):
    job_title = forms.CharField(max_length=100, required=True)
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
        ('16', 'Any')
    )
    Type_of_gender = (
        ('01', 'Male'),
        ('02', 'Female'),
        ('03', 'Any')
    )
    Type_of_job = (
        ('01', 'Part-time'),
        ('02', 'Internship')
    )
    faculty = forms.CharField(widget=forms.Select(choices=Type_of_faculty))
    age = forms.IntegerField()
    gender = forms.CharField(widget=forms.Select(choices=Type_of_gender))
    area = forms.CharField(max_length=100)
    salary = forms.IntegerField()
    job_type = forms.CharField(widget=forms.Select(choices=Type_of_job), required=True)

    def clean(self):
        clean_data = super().clean()
        age = clean_data.get('age')
        salary = clean_data.get('salary')

        if age < 10:
            raise forms.ValidationError('อายุต้องมากกว่า 10')
        elif salary < 1:
            raise forms.ValidationError('เงินเดือนที่ใส่ห้ามต่ำกว่า 1')


class OtherForm(forms.Form):
    requirement = forms.CharField(max_length=50, required=True)

class EditStudentForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)
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
    faculty = forms.CharField(widget=forms.Select(choices=Type_of_faculty))

class SkillForm(forms.Form):
    requirement = forms.CharField(max_length=50, required=True)