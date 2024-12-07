from django.shortcuts import render,get_object_or_404,redirect
from .accounts import *
from .models import *
from .forms import *
from seeker.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db import IntegrityError
from .render import Render
from django.utils import timezone

def post_job(request):
    if request.session.get('provider') != None:
        epl = request.session.get('provider')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Provider:provider_login')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
    if provider_profile_user.avatar is None:
        provider_image = None
    else:
        provider_image = provider_profile_user
    if request.method == 'POST':
        form = PostJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = user.provider_names
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('Provider:managejobs')
    else:
        form = PostJobForm()
    template = "Provider/Job/post_job.html"
    context = {
        'img': provider_image.avatar.url,
        'job_form': form,
    }
    return render(request, template, context)


def edit_job(request, job_id):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')

    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
    if provider_profile_user.avatar is None:
        provider_image = None
    else:
        provider_image = provider_profile_user

    try:
        job = PostJob.objects.get(id=job_id)
    except PostJob.DoesNotExist:
        messages.error(request, "Job not found.")
        return redirect('Provider:dashboard')

    if job.user != user.provider_names:
        messages.error(request, "You are not authorized to edit this job.")
        return redirect('Provider:managejobs')

    if request.method == 'POST':
        form = PostJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('Provider:viewjob', job_id=job.id)
    else:
        form = PostJobForm(instance=job)

    template = "Provider/Job/edit_job.html"
    context = {
        'img': provider_image.avatar.url,
        'job_form': form,
    }
    return render(request, template, context)

def delete_job(request, job_id):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')

    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])

    try:
        job = PostJob.objects.get(id=job_id)
    except PostJob.DoesNotExist:
        messages.error(request, "Job not found.")
        return redirect('Provider:dashboard')

    if job.user != user.provider_names:
        messages.error(request, "You are not authorized to edit this job.")
        return redirect('Provider:managejobs')
    else:
        job.delete()
        return redirect('Provider:managejobs')

def managejobs(request):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
    if provider_profile_user.avatar is None:
        provider_image = None
    else:
        provider_image = provider_profile_user
    provider_names = user.provider_names
    jobs = PostJob.objects.filter(user=provider_names)
    paginator = Paginator(jobs, 4)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)
    context = {
        'jobs': jobs,
        'img': provider_image.avatar.url,
    }
    return render(request, 'Provider/Job/managejobs.html', context)

def viewjob(request, job_id):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
    if provider_profile_user.avatar is None:
        provider_image = None
    else:
        provider_image = provider_profile_user
    provider_names = user.provider_names
    try:
        job = PostJob.objects.get(id=job_id, user=provider_names)
    except PostJob.DoesNotExist:
        return redirect('Provider:managejobs')
    context = {
        'job': job,
        'img': provider_image.avatar.url,
    }
    return render(request, 'Provider/Job/viewjob.html', context)

def all_applicants_list(request):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
    if provider_profile_user.avatar is None:
        provider_image = None
    else:
        provider_image = provider_profile_user
    provider_names = user.provider_names
    if not provider_names:
        return redirect('Provider:provider_login')
    
    applicants_list = ApplyJob.objects.filter(job__user=provider_names).order_by('-created_at')
    
    paginator = Paginator(applicants_list,10)  # Show 10 applicants per page
    page = request.GET.get('page')
    applicants = paginator.get_page(page)

    return render(request, 'Provider/Job/all_applicants_list.html', {'applicants': applicants, 'img': provider_image.avatar.url})

def view_employee(request, applicant_id):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
    if provider_profile_user.avatar is None:
        provider_image = None
    else:
        provider_image = provider_profile_user
    applicant = ApplyJob.objects.get(id=applicant_id)
    user = seeker_names.objects.get(user=applicant.applicant.user)
    res = Resume.objects.filter(user=user)
    head = Headline.objects.filter(user=user)
    summ = Summary.objects.filter(user=user)
    edu = Education.objects.all().filter(user=user)
    pro = Project.objects.filter(user=user)
    certi = Certificate.objects.filter(user=user)
    social = Social.objects.filter(user=user)
    skills = Skills.objects.filter(user=user)
    context = {
        'employee': user,
        'applicant':applicant,
        "resume": res,
        "headline": head,
        "summary": summ,
        "education": edu,
        "project": pro,
        "certificate": certi,
        "social": social,
        "skills":skills,
        'img': provider_image.avatar.url
    }

    return render(request, 'Provider/Job/view_employee.html', context)


def update_service_decision(request):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        decision = request.POST.get('job_decision')
        print(request_id,decision)
        job_request = ApplyJob.objects.get(pk=request_id)
        print(job_request.applicant)
        user_get = User.objects.get(username=job_request.applicant)
        print(user_get)
        if decision == 'yes':
            job_request.status = "Reviewed"
            job_request.save()
            return redirect('Provider:schedule_meeting',applicant_id=user_get.id,job_id=job_request.id)
        elif decision == 'no':
            job_request.status = "Rejected"
            job_request.save()

            return redirect('Provider:all_applicants_list')
        else:
            job_request.seek_decision = "Reviewed"
            job_request.save()
    else:
        return redirect('Provider:all_applicants_list')

    return render(request, 'Provider/Job/update_service_decision.html')

def schedule_meeting(request, applicant_id, job_id):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
    if provider_profile_user.avatar is None:
        provider_image = None
    else:
        provider_image = provider_profile_user
    myuser = User.objects.get(pk=applicant_id)
    myuser = (myuser.seeker_names)
    myjob = ApplyJob.objects.get(pk=job_id)
    print(myjob.job.title)
    applicant = ApplyJob.objects.filter(applicant=myuser) and ApplyJob.objects.filter(job=myjob.job.id)
    print(applicant)
    user_get = User.objects.get(pk=applicant_id)
    print(user_get)
    if request.method == 'POST':
        form = ScheduleMeetingForm(request.POST, company_profile=provider_profile_user)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            location = form.cleaned_data['location']
            note = form.cleaned_data['notes']
            try:
                meeting = form.save(commit=False)
                meeting.application = myjob
                meeting.save()
                subject = f'{myjob.job.title} Job Request Reviewed '
                message = f'Hello {user_get.username},\nYour job application for the job role {myjob.job.title} at {provider_profile_user.c_name} has been reviewed and we scheduled an interview on the date {date} at {time}. Please keep in mind that {note}. \n\nAddress: {location}\n\nThank you,\n{provider_profile_user}\n{provider_profile_user.c_name}.'
                email_from = settings.EMAIL_HOST_USER
                email_to = [user_get.email, ]
                send_mail(subject, message, email_from, email_to)
                return redirect('Provider:all_applicants_list')
            except IntegrityError:
                messages.error(request,'Meeting is already scheduled')
                return redirect('Provider:all_applicants_list')
    else:
        form = ScheduleMeetingForm(company_profile=provider_profile_user)

    return render(request, 'Provider/Job/schedule_meeting.html', {'form': form, 'img': provider_image.avatar.url})

def manage_job_report(request):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])
    provider_names = user.provider_names
    jobs = PostJob.objects.filter(user=provider_names)
    today = timezone.now()
    context = {
        'jobs': jobs,
        'today': today,
        'request': request
    }
    return Render.render('Provider/Reports/manage_job_report.html', context)

def all_applicants_list_report(request):
    if request.session.get('provider') is None:
        return redirect('Provider:provider_login')
    epl = request.session.get('provider')
    user = User.objects.get(username=epl['username'])

    provider_names = user.provider_names
    if not provider_names:
        return redirect('Provider:provider_login')
    
    applicants = ApplyJob.objects.filter(job__user=provider_names).order_by('-created_at')

    today = timezone.now()
    context = {
        'applicants': applicants,
        'today': today,
        'request': request
    }
    return Render.render('Provider/Reports/all_applicants_list_report.html', context)