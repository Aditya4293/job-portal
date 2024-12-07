from django.shortcuts import render, get_object_or_404
from .accounts import *
from provider.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
from .render import Render
# Create your views here.


def index(request):
   jobs = PostJob.objects.order_by('-created_at')[:8]
   reversed_jobs = reversed(jobs[:10])
   job_categories = {}
   for category in JobCategory.objects.values_list('name', 'id'):
      job_count = PostJob.objects.filter(category_id=category[1]).count()
      job_categories[category[0]] = job_count
   sorted_categories = dict(sorted(job_categories.items(), key=lambda item: item[1], reverse=True)[:8])
   cities = city_data.objects.annotate(job_count=Count('postjob')).order_by('-job_count')
   context = {
       'jobs': jobs,
       'reversed_jobs':reversed_jobs,
       'job_categories':sorted_categories,
       'cities':cities
   }
   return render(request, "index.html",context)


def job_search(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    # Filter jobs by query and/or category
    jobs = PostJob.objects.all()
    if query:
        jobs = jobs.filter(Q(title__icontains=query) |
            Q(location__city__icontains=query) |
            Q(location__state_name__state__icontains=query))
    if category_id:
        jobs = jobs.filter(category_id=category_id)

    # Pagination
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Top job categories
    job_categories = JobCategory.objects.annotate(job_count=Count('postjob')).order_by('-job_count')
    cities = city_data.objects.annotate(job_count=Count('postjob')).order_by('-job_count')
    return render(request, 'job_search.html', {'page_obj': page_obj, 'query': query, 'job_categories': job_categories,'cities':cities})


def search_cat(request, category_id):
    # Retrieve jobs for the selected category
    job_category = JobCategory.objects.get(id=category_id)
    job_list = PostJob.objects.filter(category=job_category)
    paginator = Paginator(job_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Top job categories
    job_categories = JobCategory.objects.annotate(job_count=Count('postjob')).order_by('-job_count')
    cities = city_data.objects.annotate(job_count=Count('postjob')).order_by('-job_count')

    return render(request, 'job_search.html', {'page_obj': page_obj, 'job_categories': job_categories,'cities':cities})

def search_cat_city(request, category_id):
    # Retrieve jobs for the selected category
    job_category = city_data.objects.get(id=category_id)
    job_list = PostJob.objects.filter(location=job_category)
    paginator = Paginator(job_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Top job categories
    job_categories = JobCategory.objects.annotate(job_count=Count('postjob')).order_by('-job_count')
    cities = city_data.objects.annotate(job_count=Count('postjob')).order_by('-job_count')

    return render(request, 'job_search.html', {'page_obj': page_obj, 'job_categories': job_categories,'cities':cities})

def seeker_job_profile(request):
   if request.session.get("seeker") != None:
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
   res = Resume.objects.filter(user=user.seeker_names)
   head = Headline.objects.filter(user=user.seeker_names)
   summ = Summary.objects.filter(user=user.seeker_names)
   edu = Education.objects.all().filter(user=user.seeker_names)
   pro = Project.objects.filter(user=user.seeker_names)
   certi = Certificate.objects.filter(user=user.seeker_names)
   social = Social.objects.filter(user=user.seeker_names)
   skills = Skills.objects.filter(user=user.seeker_names)
   return render(
      request,
      "Seeker/seeker_job_profile.html",
      {
         "img": seeker_image.avatar.url,
         "resume": res,
         "headline": head,
         "summary": summ,
         "education": edu,
         "project": pro,
         "certificate": certi,
         "social": social,
         "skills":skills,
      },
   )


def Seeker_Resume(request):
   if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user

   prev_res = Resume.objects.filter(user=user.seeker_names)
   if request.method == "POST":
      res = Resume_Form(request.POST, request.FILES)
      if res.is_valid():
         res_user = res.save(commit=False)
         res_user.user = user.seeker_names
         if prev_res:
               print(prev_res)
               prev_res.delete()
         res_user.save()
         return redirect("Seeker:seeker_job_profile")
      else:
         print("Form is invalid")
   else:
      res = Resume_Form()
   template = "Seeker/seeker_settings/resume.html"
   return render(request, template, {"img": seeker_image.avatar.url,"data": res})


def Seeker_Certificate(request):
   if request.session.get("seeker") != None:
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user

      prev_certi = Certificate.objects.filter(user=user.seeker_names)
      if request.method == "POST":
         cf = Certificate_Form(request.POST)
         if cf.is_valid():
               cf_user = cf.save(commit=False)
               cf_user.user = user.seeker_names
               # if prev_certi:
               #    print(prev_certi)
               #    prev_certi.delete()
               cf_user.save()
               return redirect("Seeker:seeker_job_profile")
         else:
               print("Form is invalid")
      else:
         cf = Certificate_Form()
      template = "Seeker/seeker_settings/certificate.html"
      return render(request, template, {"img": seeker_image.avatar.url,"data": cf})
   else:
      return redirect("Seeker:seeker_login")


def Seeker_Education(request):
   if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user

      prev_edu = Education.objects.filter(user=user.seeker_names)
      if request.method == "POST":
         ef = Education_Form(request.POST)
         if ef.is_valid():
               edu_user = ef.save(commit=False)
               edu_user.user = user.seeker_names
               # if prev_edu:
               #    print(prev_edu)
               #    prev_edu.delete()
               edu_user.save()
               return redirect("Seeker:seeker_job_profile")
         else:
               print("Form is invalid")
      else:
         ef = Education_Form()
      template = "Seeker/seeker_settings/education.html"
      return render(request, template, {"img": seeker_image.avatar.url,"data": ef})
   else:
      return redirect("Seeker:seeker_login")


def Seeker_Headline(request):
   if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_headline = Headline.objects.filter(user=user.seeker_names)

      if request.method == "POST":
         hf = Headline_Form(request.POST)
         if hf.is_valid():
               hf_user = hf.save(commit=False)
               hf_user.user = user.seeker_names
               if prev_headline:
                  print(prev_headline)
                  prev_headline.delete()
               hf_user.save()
               return redirect("Seeker:seeker_job_profile")
         else:
               print("Form is invalid")
      else:
         hf = Headline_Form()
      template = "Seeker/seeker_settings/headline.html"
      return render(request, template, {"img": seeker_image.avatar.url,"data": hf})
   else:
      return redirect("Seeker:seeker_login")


def Seeker_Project(request):
   if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user

      prev_pro = Project.objects.filter(user=user.seeker_names)
      if request.method == "POST":
         pf = Project_Form(request.POST)
         if pf.is_valid():
               pf_user = pf.save(commit=False)
               pf_user.user = user.seeker_names
               # if prev_pro:
               #    print(prev_pro)
               #    prev_pro.delete()
               pf_user.save()
               return redirect("Seeker:seeker_job_profile")
         else:
               print("Form is invalid")
      else:
         pf = Project_Form()
      template = "Seeker/seeker_settings/project.html"
      return render(request, template, {"img": seeker_image.avatar.url,"data": pf})
   else:
      return redirect("Seeker:seeker_login")


def Seeker_Skills(request):
   if request.session.get("seeker") != None:
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_headline = Skills.objects.filter(user=user.seeker_names)

      if request.method == "POST":
         hf = Skill_Form(request.POST)
         if hf.is_valid():
               hf_user = hf.save(commit=False)
               hf_user.user = user.seeker_names
               hf_user.save()
               return redirect("Seeker:seeker_job_profile")
         else:
               print("Form is invalid")
      else:
         hf = Skill_Form()
      template = "Seeker/seeker_settings/skills.html"
      return render(request, template, {"img": seeker_image.avatar.url,"skill": hf})
   else:
      return redirect("Seeker:seeker_login")


def Seeker_Social(request):
   if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user

      prev_soc = Social.objects.filter(user=user.seeker_names)
      if request.method == "POST":
         sp = Social_Form(request.POST)
         if sp.is_valid():
               sp_user = sp.save(commit=False)
               sp_user.user = user.seeker_names
               # if prev_soc:
               #    print(prev_soc)
               #    prev_soc.delete()
               sp_user.save()
               return redirect("Seeker:seeker_job_profile")
         else:
               print("Form is invalid")
      else:
         sp = Social_Form()
      template = "Seeker/seeker_settings/social.html"
      return render(request, template, {"img": seeker_image.avatar.url,"data": sp})
   else:
      return redirect("Seeker:seeker_login")


def Seeker_Summary(request):
   if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Summary.objects.filter(user=user.seeker_names)
      if request.method == "POST":
         sf = Summary_Form(request.POST)
         if sf.is_valid():
               sf_user = sf.save(commit=False)
               sf_user.user = user.seeker_names
               if prev_summ:
                  print(prev_summ)
                  prev_summ.delete()
               sf_user.save()
               return redirect("Seeker:seeker_job_profile")
         else:
               print("Form is invalid")
      else:
         sf = Summary_Form()
      template = "Seeker/seeker_settings/summary.html"
      return render(request, template, {"img": seeker_image.avatar.url,"data": sf})
   else:
      return redirect("Seeker:seeker_login")

def apply_job(request, job_id):
   if request.session.get("seeker") != None:
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      job = get_object_or_404(PostJob, pk=job_id)
      if request.method == 'POST':
           form = ApplyJobForm(request.POST, request.FILES)
           if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = user.seeker_names
            application.save()
            return redirect("Seeker:seeker_job_profile")
      else:
         form = ApplyJobForm()
      return render(request, 'Seeker/SeekJob/apply_job.html', {'job': job, 'form': form,"img": seeker_image.avatar.url})
   else:
      return redirect("Seeker:seeker_login")

def applied_jobs(request):
   if request.session.get("seeker") != None:
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      applications = ApplyJob.objects.filter(applicant=user.seeker_names).order_by('-created_at')
      context = {'applications': applications,"img": seeker_image.avatar.url}
      return render(request, 'Seeker/SeekJob/applied_jobs.html', context)
   else:
      return redirect("Seeker:seeker_login")

def seeker_viewjob(request, job_id):
   if request.session.get("seeker") != None:
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      try:
         job = PostJob.objects.get(id=job_id)
      except PostJob.DoesNotExist:
         return redirect('Seeker:applied_jobs')
      context = {
         'job': job,
         "img": seeker_image.avatar.url
      }
      return render(request, 'Seeker/SeekJob/seeker_viewjob.html', context)
   else:
      try:
         job = PostJob.objects.get(id=job_id)
      except PostJob.DoesNotExist:
         return redirect('Seeker:applied_jobs')
      context = {
         'job': job,
      }
      return render(request, 'Seeker/SeekJob/seeker_viewjob.html', context)


from django.urls import reverse

def contact(request):
    previous_page = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            subject = 'Thank you for contacting us'
            message = f'Dear {contact.name},\nThank you for contacting us. We will get back to you as soon as possible.'
            email_from = settings.EMAIL_HOST_USER
            email_to = [contact.email, ]
            send_mail(subject, message, email_from, email_to)
            return redirect('Seeker:index')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form,'previous_page': previous_page})

def aboutus(request):
   previous_page = request.META.get('HTTP_REFERER')
   context = {
        'previous_page': previous_page
        }
   return render(request,'aboutus.html',context)


def MyResume(request):
   if request.session.get("seeker") != None:
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )

   res = Resume.objects.filter(user=user.seeker_names)
   head = Headline.objects.filter(user=user.seeker_names)
   summ = Summary.objects.filter(user=user.seeker_names)
   edu = Education.objects.all().filter(user=user.seeker_names)
   pro = Project.objects.filter(user=user.seeker_names)
   certi = Certificate.objects.filter(user=user.seeker_names)
   social = Social.objects.filter(user=user.seeker_names)
   skills = Skills.objects.filter(user=user.seeker_names)
   context = {
      "seeker_profile_user":seeker_profile_user,
      "resume": res,
      "headline": head,
      "summary": summ,
      "education": edu,
      "project": pro,
      "certificate": certi,
      "social": social,
      "skills":skills,
      'request': request
   }

   return Render.render('Resume/MyResume.html', context)


def newsletter_view(request):
   if request.method == "GET":
      email = request.GET.get('newsletter_data')
      print(email)
      nl = Newsletter(email=email)
      nl.save()
      return redirect("Seeker:index")
   else:
      pass
   return render(request, 'common.html')

def delete_Resume(request): 
    if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Resume.objects.filter(user=user.seeker_names)
      prev_summ.delete()
      return redirect('Seeker:seeker_job_profile')
    else:
        return redirect("Seeker:seeker_login")
        
def delete_Headline(request): 
    if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Headline.objects.filter(user=user.seeker_names)
      prev_summ.delete()
      return redirect('Seeker:seeker_job_profile')
    else:
        return redirect("Seeker:seeker_login")
        
def delete_Summary(request): 
    if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Summary.objects.filter(user=user.seeker_names)
      prev_summ.delete()
      return redirect('Seeker:seeker_job_profile')
    else:
        return redirect("Seeker:seeker_login")
        
def delete_Education(request): 
    if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Education.objects.filter(user=user.seeker_names)
      prev_summ.delete()
      return redirect('Seeker:seeker_job_profile')
    else:
        return redirect("Seeker:seeker_login")
        
def delete_Project(request): 
    if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Project.objects.filter(user=user.seeker_names)
      prev_summ.delete()
      return redirect('Seeker:seeker_job_profile')
    else:
        return redirect("Seeker:seeker_login")
        
def delete_Certificate(request): 
    if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Certificate.objects.filter(user=user.seeker_names)
      prev_summ.delete()
      return redirect('Seeker:seeker_job_profile')
    else:
        return redirect("Seeker:seeker_login")
        
def delete_Social(request): 
    if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Social.objects.filter(user=user.seeker_names)
      prev_summ.delete()
      return redirect('Seeker:seeker_job_profile')        
    else:
        return redirect("Seeker:seeker_login")
    
def delete_Skills(request): 
    if request.session.get("seeker") != None:
      
      epl = request.session.get("seeker")
      user = User.objects.get(username=epl["username"])
      seeker_profile_user = Seeker_Profile_Model.objects.get(
         user=user.seeker_names.seeker_profile_model
      )
      if seeker_profile_user.avatar is None:
         seeker_image = None
      else:
         seeker_image = seeker_profile_user
      prev_summ = Skills.objects.filter(user=user.seeker_names)
      prev_summ.delete()
      return redirect('Seeker:seeker_job_profile')        
    else:
        return redirect("Seeker:seeker_login")