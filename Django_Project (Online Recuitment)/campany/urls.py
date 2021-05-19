from django.urls import path,re_path,include
from .views import *
from django_email_verification  import urls as mail_urls
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import MySetPasswordForm,MyPasswordResetForm



urlpatterns = [
    path('',HomePage.as_view(),name='home'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('company_list/',CompanyView.as_view(),name='company_list'),
    path('single_company/',CompanyView_single.as_view(),name='conatct'),
    path("email/",include(mail_urls)),
    #register 
    path("send_email/",sendEmail),
    path('register/',UserRegiterView.as_view(),name='register'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name='activate'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),

    #LoginView
    path('login/',LoginView.as_view(),name='login'),
    #reset password 
   path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='commons/password_reset_form.html',
             form_class=MyPasswordResetForm,
         ),
         name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='commons/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='commons/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='commons/password_reset_complete.html'),name='password_reset_complete'),    #logout
    path('logout/',LogoutView.as_view(),name='logout'),
    #profile
    path('JobSeeker_Profile/',login_required(JobSeeker_Profile.as_view()),name='JobSeeker_Profile'),
    #add Job
    re_path(r'^job/$',Add_jobs.as_view(),name='job'),
    #company RegistrationView
    path('cregister/',CompanyRegiterView.as_view(),name='cregister'),
    path('apply/',login_required(Apply_For_Job.as_view()),name='apply'),
    path('candidate_listing/',login_required(Candidate_listing.as_view()),name='candidate_listing'),

    #subscriptions
    path('newsletter/',Subscriptions.as_view(),name='newsletter'),


    #add Degree

    path('add_degree/',Add_Qualification.as_view(),name='add_degree'),

    #page not found and

    path("page_not_found/",Page_Not_Found.as_view(),name='page_not_found'),

    #blocg
    path("blog/",Blog_Right.as_view(),name='blog'),

    #about UserRegiterView
    path("about/",About.as_view(),name='about'),

    #edit profile
    path('edit_profile/',EditProfile.as_view(),name='edit_profile'),



]