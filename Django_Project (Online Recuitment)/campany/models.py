from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ungettext_lazy as _

from .manager import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator



# Create your models here.


#Custom User Models
class MyUser(AbstractUser):
	username = None
	email =  models.EmailField(unique=True)
	
	profile = models.ImageField(upload_to='user_profile%y%m%d')
	is_seeker = models.BooleanField(default=False)
	is_hirer = models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email



class JobSeeker_profile(models.Model):
	user_type = models.OneToOneField("MyUser", on_delete=models.CASCADE)
	position = models.CharField(max_length=100,null=True)
	resume = models.FileField('Document', upload_to='mydocs_resume/')
	phone_regex = RegexValidator( regex = r'^\+?91?\d{10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
	phone= models.CharField('Phone',validators =[phone_regex], max_length=10, unique =True,null=True)
	bod = models.DateField()
	location = models.CharField(max_length=200)
	school_name = models.CharField(max_length=100,null=True)
	passing_year =  models.DateField(null=True)
	father_name = models.CharField(max_length=100,null=True)
	mother_name = models.CharField(max_length=100,null=True)
	web_site = models.URLField(null=True)




	def __str__(self):
		return self.user_type.email

class Add_Degree(models.Model):
	candidate = models.ForeignKey('MyUser', on_delete=models.CASCADE,null=True)
	degree = models.CharField(max_length=100)
	percentage = models.CharField(max_length=100)
	institute_name = models.CharField(max_length=100)
	start_date = models.CharField(max_length=100)
	passing_year = models.CharField(max_length=100)

	def __str__(self):
		return self.candidate.email






  # campany model 

class Campnay_profile(models.Model):
	user_type = models.OneToOneField("MyUser", on_delete=models.CASCADE)
	campany_logo = models.FileField(upload_to='mydocs_resume/')
	phone_regex = RegexValidator( regex = r'^\+?91?\d{10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
	phone= models.CharField('Phone',validators =[phone_regex], max_length=10, unique =True,null=True)
	location = models.CharField(max_length=300)
	company_name = models.CharField(max_length=100)
	company_site = models.URLField(max_length = 200)

	def __str__(self):
		return self.user_type.email




class Job_Type(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

Job_Category = [
("Graphic Designer","Graphic Designer"),
("Engineering Jobs ","Engineering Jobs "),
("Mainframe Jobs","Mainframe Jobs"),
("Legal Jobs","Legal Jobs"),
("IT Jobs","IT Jobs"),
("R&D Jobs","R&D Jobs"),
("Government Jobs","Government Jobs"),
("PSU Jobs","PSU Jobs"),
("Telecom","Telecom"),
("Pharma","Pharma"),
("Sales","Sales"),
("Analyticsr","Analytics"),
("Airline","Airline"),
("Teacher","Teacher"),
("HR","HR"),
("Hotel","Hotel"),
]

class Job_Category(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name


class Add_Job_Model(models.Model):
	campany = models.ForeignKey("Campnay_profile", on_delete=models.CASCADE)
	job_type = models.ForeignKey("Job_Type", on_delete=models.CASCADE)
	job_cat = models.ForeignKey('Job_Category',on_delete=models.CASCADE)
	job_title = models.CharField(max_length=100)
	sift = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	job_updates = models.DateTimeField(auto_now_add=True)
	salary_pack = models.FloatField(null=True)
	min_salary = models.FloatField(null=True)
	max_salary = models.FloatField(null=True)
	job_desc = models.TextField()
	job_skills = models.CharField(max_length=100)
	joining_facilites = models.CharField(max_length=300)
	notice_period = models.CharField(max_length=50)
	job_post_file = models.FileField('Document',upload_to='post_file%y%m%d',null=True)
	ex_p = models.CharField(max_length=20)
	def __str__(self):
		return self.campany.company_name



class Applied_job(models.Model):
	job = models.ForeignKey(Add_Job_Model, on_delete=models.DO_NOTHING)
	seeker = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
	fullname = models.CharField(max_length=100)
	experience = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	notic_p = models.CharField(max_length=100)
	skill = models.CharField(max_length=100)
	gander = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	dob = models.CharField(max_length=30)

	def __str__(self):
		return self.fullname


# News letters

class News_Letter(models.Model):
	email = models.EmailField(max_length=100,unique=True)


#Client Review

class ClientReview(models.Model):
	user =  models.OneToOneField("MyUser", on_delete=models.CASCADE)
	msg = models.CharField(max_length=100)



class Contact_Us(models.Model):
	name =  models.CharField(max_length=100)
	Email = models.EmailField(max_length=100)
	subject = models.CharField(max_length=100)
	msg = models.TextField()



