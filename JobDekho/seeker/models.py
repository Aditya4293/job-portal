from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from provider.models import *

# Create your models here.


GENDER = (
    ('Select','Select'),
    ('Male','Male'),
    ('Female','Female')
)

class state_data(models.Model):
    state = models.CharField(max_length=200)

    def __str__(self):
        return str(self.state)

class city_data(models.Model):
    state_name = models.ForeignKey(state_data,max_length=200,on_delete=models.PROTECT)
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.city + " - " +str(self.state_name)

class seeker_names(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Seeker_Profile_Model(models.Model):
    user = models.OneToOneField(seeker_names, on_delete=models.CASCADE,primary_key=True)
    avatar = ResizedImageField(size=[450, 450], crop=['middle','center'],upload_to="seeker_profile/",null=True,blank=True, default="/seeker_profile/avatar.jpeg")
    fname = models.CharField(max_length=50,null=True,blank=True)
    lname = models.CharField(max_length=50,null=True,blank=True)
    tel = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='M')
    age = models.IntegerField(default=15, null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    area = models.ForeignKey(city_data,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=seeker_names)
def create_Seeker_Profile_Model(sender, instance, created, **kwargs):
    if created:
        Seeker_Profile_Model.objects.create(user=instance)

@receiver(post_save, sender=seeker_names)
def save_user_Seeker_Profile_Model(sender, instance, **kwargs):
    instance.seeker_profile_model.save()

# More details model
EDUCATION = (
    ('Select Education','Select Education'),
    ('10th','10th'),
    ('12th','12th'),
    ('Graduate','Graduate'),
    ('Post Graduate','Post Graduate')
)

COURSE = (
    ('Select Course','Select Course'),
    ('BCA','BCA'),
    ('BCOM','BCOM'),
    ('BSC','BSC'),
    ('B-ARCH','B-ARCH'),
    ('BE','BE'),
    ('BTECH','BTECH'),
    ('BBA','BBA'),
    ('BA','BA'),
    ('BMM','BMM')
)

SPECIALIZATION = (
    ('Select Specialization','Select Specialization'),
    ('Computer Science','Computer Science'),
    ('Computer Science Engineering','Computer Science Engineering'),
    ('Web Development','Web Development'),
    ('Android Development','Android Development'),
    ('IOS Development','IOS Development'),
    ('Human Resource','Human Resource')
)

UNIVERSITY = (
    ('Select University','Select University'),
    ('Gujarat University','Gujarat University'),
    ('LPU','LPU'),
    ('Other','Other')
)

COURSE_TYPE = (
    ('Full-Time','Full-Time'),
    ('Part-Time','Part-Time'),
    ('Distance Learning','Distance Learning')
)

PASSING_YEAR = (
    ('Select Passing Year','Select Passing Year'),
    ('2023','2023'),
    ('2022','2022'),
    ('2021','2021'),
    ('2020','2020'),
    ('2019','2019'),
    ('2018','2018'),
    ('2017','2017'),
    ('2016','2016'),
    ('2015','2015'),
    ('2014','2014'),
    ('2013','2013'),
    ('2012','2012'),
    ('2011','2011'),
    ('2010','2010'),
    ('2009','2009'),
    ('2008','2008'),
    ('2007','2007'),
    ('2006','2006'),
    ('2005','2005'),
    ('2004','2004'),
    ('2003','2003'),
    ('2002','2002'),
    ('2001','2001'),
    ('2000','2000')
)

MONTH = (
    ('Month','Month'),
    ('January','January'),
    ('February','February'),
    ('March','March'),
    ('April','April'),
    ('May','May'),
    ('June','June'),
    ('July','July'),
    ('August','August'),
    ('September','September'),
    ('October','October'),
    ('November','November'),
    ('December','December')
)

YEAR = (
    ('Year','Year'),
    ('2023','2023'),
    ('2022','2022'),
    ('2021','2021'),
    ('2020','2020'),
    ('2019','2019'),
    ('2018','2018'),
    ('2017','2017'),
    ('2016','2016'),
    ('2015','2015'),
    ('2014','2014')
)

SKILL = (
    ('HTML','HTML'),
    ('CSS','CSS'),
    ('Javascipt','Javascript'), 
    ('Bootstrap','Bootstrap'),
    ('ReactJS','ReactJS'),
    ('AngularJS','AngularJS'),
    ('VueJS','VueJS'),
    ('C language','C language'),
    ('C++','C++'),
    ('Python','Python'),
    ('Java','Java'),
    ('Web Design','Web Design'),
    ('Photoshop','Photoshop'),
    ('Django','Django')
)

class Resume(models.Model):
    user = models.ForeignKey(seeker_names,on_delete=models.CASCADE,null=True,blank=True)
    resume = models.FileField(upload_to="Docs/")

    def __str__(self):
        return str(self.resume)


class Headline(models.Model):
    user = models.ForeignKey(seeker_names,on_delete=models.CASCADE,null=True,blank=True)
    headline = models.TextField(max_length=200)

    def __str__(self):
        return self.headline


class Summary(models.Model):
    user = models.ForeignKey(seeker_names,on_delete=models.CASCADE,null=True,blank=True)
    summary = models.TextField(max_length=200)

    def __str__(self):
        return self.summary


class Education(models.Model):
    user = models.ForeignKey(seeker_names,on_delete=models.CASCADE,null=True,blank=True)
    education = models.CharField(max_length=50,choices=EDUCATION,default="Select Education")
    course = models.CharField(max_length=50,choices=COURSE,default="Select Course")
    specialization = models.CharField(max_length=50,choices=SPECIALIZATION,default="Select Specialization")
    university = models.CharField(max_length=50,choices=UNIVERSITY,default="Select University")
    course_type = models.CharField(max_length=50,choices=COURSE_TYPE,default="Full-Time")
    passing_year = models.CharField(max_length=50,choices=PASSING_YEAR,default="Select Passing Year")

    def __str__(self):
        return self.education


class Project(models.Model):
    user = models.ForeignKey(seeker_names,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=50)
    start_month = models.CharField(max_length=50,choices=MONTH,default="Month")
    start_year = models.CharField(max_length=50,choices=YEAR,default="Year")
    end_month =  models.CharField(max_length=50,choices=MONTH,default="Month")
    end_year = models.CharField(max_length=50,choices=YEAR,default="Year")
    url = models.URLField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Certificate(models.Model):
    user = models.ForeignKey(seeker_names,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50)
    issuing_org = models.CharField(max_length=50)
    issue_month = models.CharField(max_length=50,choices=MONTH,default="Month")
    issue_year = models.CharField(max_length=50,choices=YEAR,default="Year")
    expiry_month = models.CharField(max_length=50,choices=MONTH,default="Month")
    expiry_year = models.CharField(max_length=50,choices=YEAR,default="Year")
    credential_id = models.CharField(max_length=100)
    credential_url = models.URLField(max_length=100)


    def __str__(self):
        return self.name


class Social(models.Model):
    user = models.ForeignKey(seeker_names,on_delete=models.CASCADE,null=True,blank=True)
    profile_name = models.CharField(max_length=50)
    profile_url = models.URLField(max_length=100)
    profile_des = models.CharField(max_length=200)

    def __str__(self):
        return self.profile_name


class Skills(models.Model):
    user = models.ForeignKey(seeker_names,on_delete=models.CASCADE,null=True,blank=True)
    skill = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return str(self.skill)

class ApplyJob(models.Model):
    STATUS_CHOICES = (
        ('new', _('New')),
        ('reviewed', _('Reviewed')),
        ('rejected', _('Rejected')),
        ('accepted', _('Accepted')),
    )

    job = models.ForeignKey(PostJob, on_delete=models.CASCADE, verbose_name=_("Job"), related_name='applications')
    applicant = models.ForeignKey(seeker_names, on_delete=models.CASCADE, verbose_name=_("Applicant"))
    name = models.CharField(max_length=50, verbose_name=_("Full Name"))
    email = models.EmailField(max_length=50, verbose_name=_("Email"))
    phone = models.CharField(max_length=10, verbose_name=_("Phone"), null=True, blank=True)
    resume = models.FileField(upload_to="resumes/", verbose_name=_("Resume"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Job Application")
        verbose_name_plural = _("Job Applications")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.job.title})"
    

class ScheduleMeeting(models.Model):
    application = models.ForeignKey(ApplyJob, on_delete=models.CASCADE, related_name='meetings')
    date = models.DateField(verbose_name=_("Date"))
    time = models.TimeField(verbose_name=_("Time"))
    location = models.CharField(max_length=10000, verbose_name=_("Location"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Schedule Meeting")
        verbose_name_plural = _("Schedule Meetings")
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.application.name} - {self.date} at {self.time}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Newsletter(models.Model):
    email = models.EmailField(unique=False)

    def __str__(self):
        return str(self.email)
