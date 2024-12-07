from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
# from seeker.models import ApplyJob

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

class provider_names(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class Provider_Profile_Model(models.Model):
    user = models.OneToOneField(provider_names, on_delete=models.CASCADE,primary_key=True)
    avatar = ResizedImageField(size=[450, 450], crop=['middle','center'],upload_to="provider_profile/",null=True,
    blank=True,default="/provider_profile/default.png")
    fname = models.CharField(max_length=50,null=True,blank=True)
    lname = models.CharField(max_length=50,null=True,blank=True)
    tel = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='M')
    age = models.IntegerField(default=15, null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    area = models.ForeignKey(city_data,on_delete=models.CASCADE,null=True,blank=True)
    c_name = models.CharField(max_length=50,null=True,blank=True)
    c_email = models.CharField(max_length=50,null=True,blank=True)
    c_website = models.CharField(max_length=50,null=True,blank=True)
    c_descrip = models.TextField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.user)






@receiver(post_save, sender=provider_names)
def create_Provider_Profile_Model(sender, instance, created, **kwargs):
    if created:
        Provider_Profile_Model.objects.create(user=instance)

@receiver(post_save, sender=provider_names)
def save_user_Provider_Profile_Model(sender, instance, **kwargs):
    instance.provider_profile_model.save()


class JobCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Job categories"

    def __str__(self):
        return self.name


class PostJob(models.Model):
    user = models.ForeignKey(provider_names, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name=_("Job title"))
    description = models.TextField(verbose_name=_("Job description"))
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, verbose_name=_("Job category"))
    location = models.ForeignKey(city_data, on_delete=models.CASCADE, verbose_name=_("Job location"))
    salary_min = models.PositiveIntegerField(verbose_name=_("Minimum salary"), validators=[MinValueValidator(0)], null=True, blank=True)
    salary_max = models.PositiveIntegerField(verbose_name=_("Maximum salary"), validators=[MinValueValidator(0)], null=True, blank=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, verbose_name=_("Experience (in years)"), validators=[MinValueValidator(0)], null=True, blank=True)
    skills_required = models.CharField(max_length=3000,verbose_name=_("Required Skills"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = "Job posting"
        verbose_name_plural = "Job postings"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

