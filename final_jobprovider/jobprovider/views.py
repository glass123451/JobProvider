from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group


# Create your views here.
# from jobprovider.forms import RegisterStudentForm
from jobprovider.forms import RegisterStudentForm, RegisterEmployerForm, EditEmployerForm, JobForm, OtherForm, \
    EditStudentForm
from jobprovider.models import Job, Other, Employer, Student, Skill, Applied


def index(request):
    return HttpResponse("eiei")

def mylogin(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next_url')
            print(next_url)
            if next_url:
                print('NEXT')
                return redirect(next_url)
            else:
                print('No Next')
                if user.groups.filter(name='Student').exists():
                    return redirect('search_job')
                else:
                    return  redirect('search_unemp')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'
            print('error')

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
        context['access'] = "Access Denied, please Sign in with another account"


    print(User.objects.filter(last_name__icontains = 'ea').query)
    return render(request=request, template_name='jobprovider/login.html', context=context)

@login_required
def mylogout(request):
    logout(request)
    return redirect('mylogin')

def search_job(request):
    context = {}
    job_all = Job.objects.all()
    job_filter = []
    faculty_all = [
        'วิศวกรรมศาสตร์',
        'สถาปัตยกรรมศาสตร์',
        'ครุศาสตร์อุตสาหกรรมและเทคโนโลยี',
        'เทคโนโลยีการเกษตร',
        'วิทยาศาสตร์',
        'อุตสาหกรรมเกษตร',
        'เทคโนโลยีสารสนเทศ',
        'วิทยาลัยนานาชาติ',
        'วิทยาลัยนาโนเทคโนโลยี',
        'วิทยาลัยนวัตกรรมการผลิตขั้นสูง',
        'การบริหารและจัดการ',
        'วิทยาลัยอุตสาหกรรมการบินนานาชาติ',
        'ศิลปศาสตร์',
        'แพทยศาสตร์',
        'วิทยาลัยวิศวกรรมสังคีต'
    ]

    gender_all = [
        'Male',
        'Female'
    ]
    # change gender number to name
    gender = ''
    for i in range(len(gender_all)):
        if gender_all[i] == request.POST.get('gender'):
            gender = '0' + str(i+1)

    # change faculty number to name
    faculty = 0
    for i in range(len(faculty_all)):
        if faculty_all[i] == request.POST.get('faculty'):
            faculty = i+1
            if faculty < 10:
                faculty = '0' + str(faculty)
            else:
                faculty = str(faculty)

    if request.method == 'GET':
        print('GET')
        context['job_all'] = job_all

    else:
        print('POST')
        print(request.POST.get('faculty'))
        for job in job_all:
            print("request.POST.get('faculty') " + str(request.POST.get('faculty') is None))
            print("request.POST.get('age') " + str(request.POST.get('age') is None))
            print("request.POST.get('gender') "+ str(request.POST.get('gender') is None))
            print("request.POST.get('area') "+ str(request.POST.get('area') is None))
            print("request.POST.get('salary') "+ str(request.POST.get('salary') is None))
            print(request.POST.get('age'))
            print(request.POST.get('area'))
            print(request.POST.get('salary'))

            # good search
            # done
            if request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('gender') is None and request.POST.get('area') == '' and request.POST.get('salary') == '':
                print('Imhere')
                job_filter = job_all
            # 4 blank
            elif request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('gender') is None and request.POST.get('area') == '':
                if (int(request.POST.get('salary'))) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('gender') is None and request.POST.get('salary') == '':
                if request.POST.get('area') in job.area:
                    job_filter.append(job)

            elif request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('salary') == '' and request.POST.get('area') == '':
                if gender == job.gender:
                    job_filter.append(job)

            elif request.POST.get('faculty') is None and request.POST.get('gender') is None and request.POST.get('salary') == '' and request.POST.get('area') == '':
                if int(request.POST.get('age')) >= int(job.age):
                    job_filter.append(job)

            elif request.POST.get('age') == '' and request.POST.get('gender') is None and request.POST.get('salary') == '' and request.POST.get('area') == '':
                if faculty == job.faculty:
                    job_filter.append(job)

            # 3 black
            elif request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('gender') is None:
                if request.POST.get('area') in job.area and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('area') == '':
                if gender == job.gender and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('salary') == '':
                if gender == job.gender and request.POST.get('area') in job.area:
                    job_filter.append(job)
            # faculty done
            elif request.POST.get('age') == '' and request.POST.get('gender') is None and request.POST.get('area') == '':
                if faculty == job.faculty and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('age') == '' and request.POST.get('gender') is None and request.POST.get('salary') == '':
                if faculty == job.faculty and request.POST.get('area') in job.area:
                    job_filter.append(job)

            elif request.POST.get('age') == '' and request.POST.get('salary') == '' and request.POST.get('area') == '':
                if faculty == job.faculty and gender == job.gender:
                    job_filter.append(job)
            # faculty, age done

            elif request.POST.get('gender') is None and request.POST.get('salary') == '' and request.POST.get('area') == '':
                if faculty == job.faculty and int(request.POST.get('age')) >= int(job.age):
                    job_filter.append(job)
            # 2 blank
            elif request.POST.get('faculty') is None and request.POST.get('age') == '':
                if gender == job.gender and request.POST.get('area') in job.area and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('faculty') is None and request.POST.get('gender') is None:
                if int(request.POST.get('age')) >= int(job.age) and request.POST.get('area') in job.area and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('faculty') is None and request.POST.get('area') == '':
                if int(request.POST.get('age')) >= int(job.age) and gender == job.gender and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('faculty') is None and request.POST.get('salary') == '':
                if int(request.POST.get('age')) >= int(job.age) and gender == job.gender and request.POST.get('area') in job.area:
                    job_filter.append(job)
            # faculty done
            elif request.POST.get('age') == '' and request.POST.get('gender') is None:
                if faculty == job.faculty and request.POST.get('area') in job.area and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('age') == '' and request.POST.get('area') == '':
                if faculty == job.faculty and gender == job.gender and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('age') == '' and request.POST.get('salary') == '':
                if faculty == job.faculty and gender == job.gender and request.POST.get('area') in job.area:
                    job_filter.append(job)
            # faculty , age done
            elif request.POST.get('gender') is None and request.POST.get('area') == '':
                if faculty == job.faculty and int(request.POST.get('age')) >= int(job.age) and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('gender') is None and request.POST.get('salary') == '':
                if faculty == job.faculty and int(request.POST.get('age')) >= int(job.age) and request.POST.get('area') in job.area:
                    job_filter.append(job)
            # faculty, age, gender done

            elif request.POST.get('area') == '' and request.POST.get('salary') == '':
                if faculty == job.faculty and int(request.POST.get('age')) >= int(job.age) and gender == job.gender:
                    job_filter.append(job)
            # 1 black
            elif request.POST.get('faculty') is None:
                if int(request.POST.get('age')) >= int(job.age) and gender == job.gender and request.POST.get('area') in job.area and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('age') == '':
                if faculty == job.faculty and gender == job.gender and request.POST.get('area') in job.area and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('gender') is None:
                if faculty == job.faculty and int(request.POST.get('age')) >= int(job.age) and request.POST.get('area') in job.area and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('area') == '':
                if faculty == job.faculty and int(request.POST.get('age')) >= int(job.age) and gender == job.gender and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

            elif request.POST.get('salary') == '':
                if faculty == job.faculty and int(request.POST.get('age')) >= int(job.age) and gender == job.gender and request.POST.get('area') in job.area:
                    job_filter.append(job)

            else:
                if faculty == job.faculty and int(request.POST.get('age')) >= int(job.age) and gender == job.gender and request.POST.get('area') in job.area and int(request.POST.get('salary')) <= int(job.salary):
                    job_filter.append(job)

        context['job_all'] = job_filter

    return render(request, 'jobprovider/search_job.html', context=context)

@login_required
@permission_required('jobprovider.change_job')
def manage_job(request):

    context = {}

    if request.method == 'POST':
        formjob = JobForm(request.POST)
        if formjob.is_valid():
            job = Job.objects.create(
                create_by=request.user.employer,
                job_title=formjob.cleaned_data.get('job_title'),
                faculty=formjob.cleaned_data.get('faculty'),
                age=formjob.cleaned_data.get('age'),
                gender=formjob.cleaned_data.get('gender'),
                area=formjob.cleaned_data.get('area'),
                salary=formjob.cleaned_data.get('salary'),
                job_type=formjob.cleaned_data.get('job_type'),
            )
            context['success'] = 'Yes'

            job.save()

        employer = request.user.employer
        if employer:
            job_of_user = Job.objects.filter(create_by_id=employer.id)
            print(job_of_user.query)
        else:
            job_of_user = None
        requirement_all = Other.objects.all()

        form = JobForm(request.POST)
        context['job_of_user'] = job_of_user
        context['requirement_all'] = requirement_all
        context['form'] = form


    else:
        employer = request.user.employer
        if employer:
            job_of_user = Job.objects.filter(create_by_id=employer.id)
        else:
            job_of_user = None
        requirement_all = Other.objects.all()

        form = JobForm()
        context['job_of_user'] = job_of_user
        context['requirement_all'] = requirement_all
        context['form'] = form

    return render(request, 'jobprovider/manage_job.html', context=context)

def job_detail(request, job_id):
    context = {}
    job = Job.objects.get(pk=job_id)
    requirements = job.other_set.all()
    employer = Employer.objects.get(pk=job.create_by_id)
    user_employer = User.objects.get(pk=employer.user_id)
    user = request.user
    if user:
        context['user'] = user

    context['user_employer'] = user_employer
    context['employer'] = employer
    context['job'] = job
    context['requirements'] = requirements
    return render(request, 'jobprovider/job_detail.html', context=context)

@login_required
@permission_required('jobprovider.add_student')
def apply(request, job_id):
    job = Job.objects.get(pk=job_id)
    employer = Employer.objects.get(pk=job.create_by_id)
    employer_user = User.objects.get(pk=employer.user_id)
    employer_user_email = employer_user.email
    print(employer_user_email)
    user = request.user

    applied = Applied.objects.create(
        applied_job=job,
        student_id=user.student.id
    )
    applied.save()

    text = ("มีการร้องขอการสมัครงาน %s จากคุณ %s %s Email: %s" %(job.job_title, user.first_name, user.last_name, user.email))


    email_for_employer = EmailMessage('ร้องขอการสมัครงาน', text, to=[employer_user_email])
    email_for_employer.send()

    job = Job.objects.get(pk=job_id)
    requirements = job.other_set.all()
    employer = Employer.objects.get(pk=job.create_by_id)
    user = User.objects.get(pk=employer.user_id)

    context = {}
    context['user'] = user
    context['employer'] = employer
    context['job'] = job
    context['requirements'] = requirements
    context['success'] = 'Your detail have been sent to employer email'
    return render(request, 'jobprovider/job_detail.html', context=context)

def search_unemp(request):
    context = {}
    unemp_all = Student.objects.filter(is_unemp=True)
    unemp_filter = []
    faculty_all = [
        'วิศวกรรมศาสตร์',
        'สถาปัตยกรรมศาสตร์',
        'ครุศาสตร์อุตสาหกรรมและเทคโนโลยี',
        'เทคโนโลยีการเกษตร',
        'วิทยาศาสตร์',
        'อุตสาหกรรมเกษตร',
        'เทคโนโลยีสารสนเทศ',
        'วิทยาลัยนานาชาติ',
        'วิทยาลัยนาโนเทคโนโลยี',
        'วิทยาลัยนวัตกรรมการผลิตขั้นสูง',
        'การบริหารและจัดการ',
        'วิทยาลัยอุตสาหกรรมการบินนานาชาติ',
        'ศิลปศาสตร์',
        'แพทยศาสตร์',
        'วิทยาลัยวิศวกรรมสังคีต'
    ]

    gender_all = [
        'Male',
        'Female'
    ]
    # change gender number to name
    gender = ''
    for i in range(len(gender_all)):
        if gender_all[i] == request.POST.get('gender'):
            gender = '0' + str(i + 1)

    # change faculty number to name
    faculty = 0
    for i in range(len(faculty_all)):
        if faculty_all[i] == request.POST.get('faculty'):
            faculty = i + 1
            if faculty < 10:
                faculty = '0' + str(faculty)
            else:
                faculty = str(faculty)

    if request.method == 'GET':
        context['unemps'] = unemp_all
    else:
        for unemp in unemp_all:
            skills = []
            skills_skill = []
            print("request.POST.get('faculty') " + str(request.POST.get('faculty') is None)) #True
            print("request.POST.get('age') " + str(request.POST.get('age') is None)) #False
            print("request.POST.get('gender') "+ str(request.POST.get('gender') is None)) #True
            print("request.POST.get('skill') "+ str(request.POST.get('skill') is None)) #False
            print(request.POST.get('age'))
            print(request.POST.get('area'))
            print(request.POST.get('salary'))
            print(request.POST.get('skill'))
            skills = Skill.objects.filter(student=unemp.id)
            print(skills)
            for i in skills:
                skills_skill.append(i.skill)
                print(skills_skill)

            # 4 blank
            if request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('gender') is None and request.POST.get('skill') == '':
                unemp_filter = unemp_all

            # 3 blank
            elif request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('gender') is None:
                if request.POST.get('skill') in skills_skill:
                    unemp_filter.append(unemp)
            elif request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('skill') == '':
                if gender == unemp.gender:
                    unemp_filter.append(unemp)
            elif request.POST.get('faculty') is None and request.POST.get('skill') == '' and request.POST.get('gender') is None:
                if int(request.POST.get('age')) == int(unemp.age):
                    unemp_filter.append(unemp)
            elif request.POST.get('gender') is None and request.POST.get('age') == '' and request.POST.get('skill') == '':
                if faculty == unemp.faculty:
                    unemp_filter.append(unemp)

            # 2 blank
            elif request.POST.get('faculty') is None and request.POST.get('age') == '':
                if request.POST.get('skill') in skills_skill and gender == unemp.gender:
                    unemp_filter.append(unemp)
            elif request.POST.get('faculty') is None and request.POST.get('gender') is None:
                if request.POST.get('skill') in skills_skill and int(request.POST.get('age')) == int(unemp.age):
                    unemp_filter.append(unemp)
            elif request.POST.get('faculty') is None and request.POST.get('skill') == '':
                if int(request.POST.get('age')) == int(unemp.age) and gender == unemp.gender:
                    unemp_filter.append(unemp)
            elif request.POST.get('age') == '' and request.POST.get('gender') is None:
                if request.POST.get('skill') in skills_skill and faculty == unemp.faculty:
                    unemp_filter.append(unemp)
            elif request.POST.get('age') == '' and request.POST.get('skill') == '':
                if faculty == unemp.faculty and gender == unemp.gender:
                    unemp_filter.append(unemp)
            elif request.POST.get('skill') == '' and request.POST.get('gender') is None:
                if faculty == unemp.faculty and int(request.POST.get('age')) == int(unemp.age):
                    unemp_filter.append(unemp)

            #1 blank
            elif request.POST.get('faculty') is None:
                if request.POST.get('skill') in skills_skill and gender == unemp.gender and int(request.POST.get('age')) == int(unemp.age):
                    unemp_filter.append(unemp)

            elif request.POST.get('age') == '':
                if request.POST.get('skill') in skills_skill and gender == unemp.gender and faculty == unemp.faculty:
                    unemp_filter.append(unemp)

            elif request.POST.get('gender') is None:
                if request.POST.get('skill') in skills_skill and int(request.POST.get('age')) == int(unemp.age) and faculty == unemp.faculty:
                    unemp_filter.append(unemp)

            elif request.POST.get('skill') == '':
                if gender == unemp.gender and int(request.POST.get('age')) == int(unemp.age) and faculty == unemp.faculty:
                    unemp_filter.append(unemp)
            # 0 blank
            else:
                if gender == unemp.gender and int(request.POST.get('age')) == int(unemp.age) and faculty == unemp.faculty and request.POST.get('skill') in skills_skill:
                    unemp_filter.append(unemp)
            # if request.POST.get('faculty') is None and request.POST.get('age') == '' and request.POST.get('gender') is None and request.POST.get('skill') == '':

        context['unemps'] = unemp_filter
    return render(request, 'jobprovider/search_unemp.html', context=context)

@login_required
@permission_required('jobprovider.add_employer')
def unemp_detail(request, unemp_id):
    unemp = Student.objects.get(pk=unemp_id)
    user_unemp = User.objects.get(pk=unemp.user_id)
    skills = unemp.skill_set.all()

    user = request.user
    jobs = user.employer.job_set.all()

    context = {}
    context['unemp'] = unemp
    context['user_unemp'] = user_unemp
    context['skills'] = skills
    context['user'] = user
    context['jobs'] = jobs

    return  render(request, 'jobprovider/student_detail.html', context=context)

@login_required
@permission_required('jobprovider.add_employer')
def offer(request, unemp_id, job_id):
    job = Job.objects.get(pk=job_id)

    unemp = Student.objects.get(pk=unemp_id)

    user = request.user
    text = ("มีการร้องขอการจ้างงาน %s จากคุณ %s %s Email: %s ที่อยู่งาน %s, เงินเดือน %s" %(job.job_title, user.first_name, user.last_name, user.email, job.area, job.salary))


    email_for_student = EmailMessage('ร้องขอการจ้างงาน', text, to=[unemp.user.email])
    email_for_student.send()

    unemp = Student.objects.get(pk=unemp_id)
    user_unemp = User.objects.get(pk=unemp.user_id)
    skills = unemp.skill_set.all()

    user = request.user
    jobs = user.employer.job_set.all()

    context = {}
    context['unemp'] = unemp
    context['user_unemp'] = user_unemp
    context['skills'] = skills
    context['user'] = user
    context['jobs'] = jobs
    context['success'] = 'You and your job detail have been sent to student email'

    return render(request, 'jobprovider/student_detail.html', context=context)


def register_student(request):
    context = {}
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST)
        dup = ''
        for i in User.objects.all():
            if i.username == request.POST.get('username'):
                dup = i.username
        if dup != '':
            context['form'] = form
            context['dup'] = True
            return render(request, 'jobprovider/register_student.html', context=context)

        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data.get('username'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
            )

            user.set_password(form.cleaned_data.get('password'))

            user.save()

            my_group = Group.objects.get(name='Student')
            my_group.user_set.add(user)

            student = Student.objects.create(
                user=user,
                faculty=form.cleaned_data.get('faculty'),
                age=form.cleaned_data.get('age'),
                phone=form.cleaned_data.get('phone'),
                gender=form.cleaned_data.get('gender'),
            )

            return redirect('mylogin')

    else:
        form = RegisterStudentForm()

    context['form'] = form

    return render(request, 'jobprovider/register_student.html', context=context)


def register_employer(request):
    context = {}
    if request.method == 'POST':
        form = RegisterEmployerForm(request.POST)
        dup = ''
        for i in User.objects.all():
            if i.username == request.POST.get('username'):
                dup = i.username
        if dup != '':
            context['form'] = form
            context['dup'] = True
            return render(request, 'jobprovider/register_employer.html', context=context)

        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data.get('username'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
            )

            user.set_password(form.cleaned_data.get('password'))

            user.save()

            my_group = Group.objects.get(name='Employer')
            my_group.user_set.add(user)

            employer = Employer.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone'),
                company=form.cleaned_data.get('company')
            )

            return redirect('mylogin')

    else:
        form = RegisterEmployerForm()

    context['form'] = form

    return render(request, 'jobprovider/register_employer.html', context=context)

@login_required
@permission_required('jobprovider.change_employer')
def edit_employer(request):
    context = {}
    user = User.objects.get(pk=request.user.id)
    print('TEST')
    print(user.first_name)
    if request.method == 'POST':
        form = EditEmployerForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            #     objects.update(
            #     first_name=form.cleaned_data.get('first_name'),
            #     last_name=form.cleaned_data.get('last_name'),
            #     email=form.cleaned_data.get('email'),
            # )

            employer = user.employer
            employer.phone = form.cleaned_data.get('phone')
            employer.company = form.cleaned_data.get('company')
            employer.save()
            context['success'] = 'Edit profile Success'

            form = EditEmployerForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': employer.phone,
                'company': employer.company,
            })
    else:
        form = EditEmployerForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.employer.phone,
            'company': user.employer.company,
        })
    context['form'] = form
    return render(request, 'jobprovider/edit_profile_emp.html', context=context)

@login_required
@permission_required('jobprovider.delete_job')
def delete(request, job_id):
    job = Job.objects.get(pk=job_id)
    applied = Applied.objects.filter(applied_job=job_id)
    for i in applied:
        student = Student.objects.get(pk=i.student_id)
        print(job.job_title)
        email_for_student = EmailMessage(('งาน (%s) %s ที่คุณยื่นสมัครถูกลบแล้ว' %(job_id, job.job_title)), 'งานที่คุณยื่นสมัครถูกลบ', to=[student.user.email])
        email_for_student.send()
    job.delete()
    return redirect('manage_job')

@login_required
@permission_required('jobprovider.change_student')
def change(request):
    user = User.objects.get(pk=request.user.id)
    student = user.student
    if student.is_unemp == False:
        student.is_unemp = True
        student.save()
    else:
        student.is_unemp = False
        student.save()
    return redirect('search_job')

@login_required
@permission_required('jobprovider.change_other')
def add_req(request, job_id):
    context = {}
    if request.method == 'POST':
        other = Other.objects.create(
            requirement= request.POST.get('requirement'),
            job=Job.objects.get(pk=job_id)
        )
        other.save()
        context['success'] = 'Add Requirement to %s Success' %(Job.objects.get(pk=job_id).job_title)

    context['user'] = request.user
    context['job_id'] = job_id
    return render(request, 'jobprovider/add_req.html', context=context)

@login_required
@permission_required('jobprovider.change_student')
def edit_student(request):
    context = {}
    user = User.objects.get(pk=request.user.id)
    print('TEST')
    print(user.first_name)
    if request.method == 'POST':
        form = EditStudentForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            #     objects.update(
            #     first_name=form.cleaned_data.get('first_name'),
            #     last_name=form.cleaned_data.get('last_name'),
            #     email=form.cleaned_data.get('email'),
            # )

            student = user.student
            student.phone = form.cleaned_data.get('phone')
            student.faculty = form.cleaned_data.get('faculty')
            student.save()

            context['success'] = 'Edit profile Success'
            form = EditStudentForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': student.phone,
                'faculty': student.faculty,
            })
    else:
        form = EditStudentForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.student.phone,
            'faculty': user.student.faculty,
        })
    skills = user.student.skill_set.all()
    context['skills'] = skills
    context['form'] = form
    return render(request, 'jobprovider/edit_profile_student.html', context=context)

@login_required
@permission_required('jobprovider.delete_skill')
def delete_skill(request, skill_id):
    skill = Skill.objects.get(pk=skill_id)
    skill.delete()
    return redirect('edit_student')

@login_required
@permission_required('jobprovider.add_skill')
def add_skill(request):
    context = {}
    if request.method == 'POST':
        skill = Skill.objects.create(
            skill= request.POST.get('skill'),
            student=request.user.student
        )
        skill.save()
        context['success'] = 'Add Skill to Your Profile Success'

    return render(request, 'jobprovider/add_skill.html', context=context)