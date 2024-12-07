from django.urls import *
from .views import *

app_name = "Provider"

urlpatterns = [
    path('',Provider_Reg, name = "provider_reg"),
    path('provider_verify/',Provider_Verify_Email, name = "provider_verify_mail"),
    path('provider_verify_mail/',Provider_Sent_Mail, name = "provider_verify_email_sent"),
    path('provider_login/',Provider_Login, name = "provider_login"),
    path('provider_profile/',Provider_Profile, name = "provider_profile"),
    path('provider_forgotpassword',Provider_ForgotPassword,name="provider_forgotpw"),
    path('provider_otpverify/',Provider_OtpVerify,name="provider_otpverify"),
    path('provider_resetpw',Provider_ResetPassword,name="provider_resetpw"),
    path('provider_logout/',Provider_Logout, name = 'provider_logout'),
    path('provider_set_password/',Provider_set_password,name="provider_set_password"),
    path('post_job/',post_job,name="post_job"),
    path('managejobs/',managejobs,name="managejobs"),
    path('viewjob/<int:job_id>/',viewjob,name="viewjob"),
    path('edit_job/<int:job_id>/', edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', delete_job, name='delete_job'),
    path('all_applicants_list/',all_applicants_list,name="all_applicants_list"),
    path('view_employee/<int:applicant_id>/',view_employee,name="view_employee"),
    path('update_service_decision/',update_service_decision,name="update_service_decision"),
    path('schedule_meeting/<int:applicant_id>/<int:job_id>/',schedule_meeting,name="schedule_meeting"),
    path('manage_job_report/',manage_job_report,name="manage_job_report"),
    path('all_applicants_list_report/',all_applicants_list_report,name="all_applicants_list_report")
]
