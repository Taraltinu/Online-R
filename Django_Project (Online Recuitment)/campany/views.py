from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
#html mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.db.models import Q



# Create your views here.


class HomePage(View):
	def get(self, request):
		recent_job = Add_Job_Model.objects.all()
		top_company = Campnay_profile.objects.all()
		# aj = request.GET.get("post_id")

		#ajax Code 
		return render(request, "index_1.html",{"recent_job":recent_job,"top_company":top_company})






class CompanyView(View):
	template_name="company_listing.html"
	def get(self,request,*args,**kwargs):
		job_listing = Add_Job_Model.objects.all()
		return render(request,self.template_name,{"job_listing":job_listing})
	def post(self,request,*args,**kwargs):
		location = request.POST.get("location")
		category = request.POST.get("category")
		Experience = request.POST.get("Experience")
		salary = request.POST.get("salary")
		salary = int(salary[0:2])
		job_listing = Add_Job_Model.objects.filter(Q(location__icontains=location)| Q(min_salary__lt=salary)|Q(ex_p__icontains=Experience)|Q(job_cat__name__icontains=category))
		return render(request, self.template_name,{"job_listing":job_listing})


class CompanyView_single(DetailView):
	template_name = 'company_listing_single.html'


# account code start


class UserRegiterView(View):
	template_name = 'register.html'

	def get(self, request):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		current_loc = request.POST.get('current_loc')
		resume = request.FILES.get('resume')
		phone = request.POST.get('phone')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')

		context = {'fieldValues': request.POST}
		if not MyUser.objects.filter(email=email).exists():
			if password == password2:
				if len(password) < 6:
					messages.error(request, 'Password too short')
					return render(request, 'register.html', context)
				user = MyUser.objects.create_user(email=email,phone=phone,location=current_loc)
				user.set_password(password)
				user.is_active = False
				user.is_seeker = True
				user.first_name = fname
				user.last_name =lname
				user.save()
				current_site = get_current_site(request)
				email_body = {
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user), }
				link = reverse('activate', kwargs={
							   'uidb64': email_body['uid'], 'token': email_body['token']})
				email_subject = 'Activate your account'
				activate_url = 'http://'+current_site.domain+link
				email = EmailMessage(
					email_subject,
					'Hi '+', Please the link below to activate your account \n'+activate_url,
					'noreply@semycolon.com',
					[email],
				)
				email.send(fail_silently=False)
				messages.success(request, 'Account successfully created')
				return redirect("login")
			else:
				messages.error(request, 'Paaword does not match ! !') 
				return redirect("register")
		else:
			messages.error(request, 'Email Already Taken !') 
			return redirect("register")


class VerificationView(View):
	def get(self, request, uidb64, token):
		try:
			id = force_text(urlsafe_base64_decode(uidb64))
			user = MyUser.objects.get(pk=id)

			if not account_activation_token.check_token(user, token):
				return redirect('login'+'?message='+'User already activated')

			if user.is_active:
				return redirect('login')
			user.is_active = True
			user.save()

			messages.success(request, 'Account activated successfully')
			return redirect('login')

		except Exception as ex:
			pass

		return redirect('login')


class EmailValidationView(View):
	def post(self, request):
		data = json.loads(request.body)
		email = data['email']
		if not validate_email(email):
			return JsonResponse({'email_error': 'Email is invalid'}, status=400)
		if User.objects.filter(email=email).exists():
			return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
		return JsonResponse({'email_valid': True})







def sendEmail(request):
	
	email = 'tinu1316@gmail.com'
	password = "Taral@1234"
	phone = 92929291111 
	user = get_user_model().objects.create(email=email,password=password,phone=phone)
	send_email(user)
	return render(request, 'confim_template.html')


class LoginView(View):
	def get(self, request):
		return render(request, 'login.html')

	def post(self, request):
		email = request.POST['email']
		password = request.POST['password']
		print(email,password)

		if email and password:
			user = MyUser.objects.filter(email=email).exists()
			print(user)
			if user:
				user = MyUser.objects.get(email=email)
				if user.is_active:
					auth.login(request, user)
					if user.is_seeker:
						messages.success(request, 'Welcome, '+' you are now logged in')
						return redirect('edit_profile')
					elif user.is_hirer:
						messages.success(request, 'Welcome, '+' you are now logged in')
						return redirect('candidate_listing')
				messages.error(
					request, 'Account is not active,please check your email')
				return redirect('login')
			messages.error(
				request, 'Invalid credentials,try again')
			return redirect('login')

		messages.error(
			request, 'Please fill all fields')
		return render(request, 'login.html')


class LogoutView(View):
	def get(self, request):
		auth.logout(request)
		messages.success(request, 'You have been logged out')
		return redirect('login')

# Company Registration View
class CompanyRegiterView(View):
	template_name = 'register.html'

	def get(self, request):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		current_loc = request.POST.get('current_loc')
		phone = request.POST.get('phone')
		company_name = request.POST.get('c_name')
		campany_logo = request.FILES.get('campany_logo')
		site_url = request.POST.get("site_url")


		context = {'fieldValues': request.POST}
		if not MyUser.objects.filter(email=email).exists():
			user = MyUser.objects.filter(email=email)
			if not Campnay_profile.objects.filter(company_name=company_name).exists():
				if len(password) < 6:
					messages.error(request, 'Password too short')
					return render(request, 'register.html', context)
				user = MyUser.objects.create_user(email=email,phone=phone,location=current_loc)
				company = Campnay_profile.objects.create(user_type=user,campany_logo=campany_logo,phone=phone,location=current_loc,company_name=company_name,company_site=site_url)
				company.save()
				user.set_password(password)
				user.is_active = False
				user.is_hirer = True
				user.is_staff = True

				user.save()
				current_site = get_current_site(request)
				email_body = {
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user), }
				link = reverse('activate', kwargs={
							   'uidb64': email_body['uid'], 'token': email_body['token']})
				email_subject = 'Activate your account'
				activate_url = 'http://'+current_site.domain+link
				email = EmailMessage(
					email_subject,
					'Hi '+', Please the link below to activate your account \n'+activate_url,
					'noreply@semycolon.com',
					[email],
				)
				email.send(fail_silently=False)
				messages.success(request, 'Account successfully created')
				return redirect("login")
			else:
				messages.error(request, 'Your Company Already Registed !') 
				return redirect("register")
		else:
			messages.error(request, 'Email Already Taken !')  
			return redirect("register")




# add Job

class Add_jobs(View):
	def get(self,request):
		job_t=  Job_Type.objects.all()
		job_c=  Job_Category.objects.all()

		return render(request,'add_postin.html',{"data":job_t,"job_c":job_c})

	def post(self,request):
		user =  MyUser.objects.get(email=request.user)
		campany = Campnay_profile.objects.get(user_type=request.user)
		job_title = request.POST.get('job_title')
		job_cat = request.POST.get('job_cat')
		job_loc = request.POST.get('')
		job_type = request.POST.get('job_type')
		salary_min = request.POST.get('min_salary')
		salary_max = request.POST.get('max_salary')
		r_skill = request.POST.get('job_skills')
		n_period = request.POST.get('notice_period')
		joining_facilities = request.POST.get('joining_facilites')
		sift = request.POST.get("sift")
		job_loc = request.POST.get("location")
		sal_pack = request.POST.get("salary_pack")
		job_desc = request.POST.get("job_desc")
		# print(job_type,r_skill,sift,job_desc,job_post_file)

		if job_type and r_skill:
			if True and  user.is_hirer:
				print(user.is_hirer)

				job_obj = Add_Job_Model(campany=campany,job_type_id=int(job_type),job_cat_id=int(job_cat),job_title=job_title,sift=sift,location=job_loc,salary_pack=sal_pack,min_salary=salary_min,max_salary=salary_max,job_desc=job_desc,job_skills=r_skill,joining_facilites=joining_facilities,notice_period=n_period)
				if 'resume' in request.FILES :
					res = request.FILES['resume']
					job_obj.job_post_file=res
					job_obj.save()
				job_obj.save()

			else:
				messages.error(request, 'You are not able Here')
				return redirect('job')

		else:
			messages.error(request, 'all field are mandotory')
			return redirect('job')


		return render(request,'add_postin.html')




#Apply Job

class Apply_For_Job(View):
	def get(self,request):
		job_id = request.GET.get("job_id")
		print(job_id)
		return render(request,'apply.html',{"job_id":job_id})
	
	def post(self, request,*args,**kwargs):
		user =   MyUser.objects.get(pk=request.user.id)
		job_id = request.POST.get('job_id')
		print(job_id,'ffffffffffffffffffffffffffff')
		job = Add_Job_Model.objects.get(pk=int(job_id))
		fullname = request.POST.get('name')
		location = request.POST.get('location')
		notice_period = request.POST.get('notice_period')
		email = request.POST.get('email')
		experience = request.POST.get('experience')
		job_skills = request.POST.get('job_skills')
		dob = request.POST.get('dob')
		gander = request.POST.get('gander')


		if user is not None:
			job_obj = Applied_job(job_id =job.id,seeker_id=user.id,fullname=fullname,city=location,experience=experience,notic_p=notice_period,skill=job_skills,gander=gander,email=email,dob=dob)
			if 'resume' in request.FILES:
				user.resume = request.FILES['resume']
				user.save()
			job_obj.save()
		return render(request,'apply.html')


class Candidate_listing(View):
	def get(self, request):
		apply_jobs = Applied_job.objects.all()
		return render(request,'candidate_listing.html',{"apply_jobs":apply_jobs})




# News Letter

def sendmail_html(request,email):
	ctx = {'user': "Aditya"}
	message = get_template('news_letter_email.html').render(ctx)
	msg = EmailMessage(
		'Subject',
		message,
		'tinu1316@gmail.com',
		[email],
	)
	msg.content_subtype = "html" 
	msg.send()
	print("Mail successfully sent")

class Subscriptions(View):
	def post(self,request, *args, **kwargs):
		ctx = {'user': "Aditya"}
		email = request.POST.get("email")

		news_obj = News_Letter.objects.get(email=email)
		if news_obj:
			messages.error(request, 'Your Are Already Subscribed !!')
		else:
			obj = News_Letter(email=email)
			obj.save()
			messages.success(request, 'Thanks for Subscribe !!')

		
		message = get_template('news_letter_email.html').render(ctx)
		msg = EmailMessage(
			'Subject',
			message,
			'tinu1316@gmail.com',
			[email],)
		msg.content_subtype = "html" 
		msg.send()
		return redirect('/')


class Add_Qualification(View):
	def get(self, request):
		return render(request,'add_degree.html')

	def post(self, request):
		candidate = MyUser.objects.get(email=request.user)
		degree = request.POST.get("degree")
		percentage = request.POST.get("percentage")
		institute_name = request.POST.get("institute_name")
		start_date = request.POST.get("start_date")
		passing_year = request.POST.get("passing_year")
		if True == candidate.is_seeker:
			if degree and percentage and institute_name:
				d_obj = Add_Degree(candidate=candidate,degree=degree,percentage=percentage,institute_name=institute_name,start_date=start_date,passing_year=passing_year)
				d_obj.save()
				messages.success(request, 'degree add Successfully!!')
				return redirect("JobSeeker_Profile")

			else:
				messages.error(request, 'The Field IS Required!!')
				return render(request,'add_degree.html')
		else:
			messages.error(request, 'You are not Job Seeker!!')
			return redirect('add_degree')

		messages.error(request, 'Something Went Wrong!!')
		return redirect("JobSeeker_Profile")






class JobSeeker_Profile(View):
	def get(self,request):
		degree = Add_Degree.objects.filter(candidate=request.user)
		data = MyUser.objects.get(email=request.user)
		profile_data = JobSeeker_profile.objects.get(user_type__id=request.user.id)


		return render(request,'candidate_profile.html',{"degree":degree,"data":data,"profile_data":profile_data})



class Page_Not_Found(View):
	def get(self,request):
		return  render(request,'404_error.html')



class Blog_Right(View):
	def get(self, request):
		jobs = Add_Job_Model.objects.all()[:3]
		return render(request,"blog_right.html",{"jobs":jobs})


class About(View):
	def get(self, request):
		return render(request,"about.html")





class ContactView(View):
	def get(self, request):
		return render(request, "contact.html")

	def post(self,request, *args, **kwargs):
		name = request.POST.get("name")
		Email = request.POST.get("Email")
		Subject = request.POST.get("Subject")
		Message = request.POST.get("Message")
		if name  and Email and Subject:
			Contact_Us(name=name,Email=Email,subject=Subject,msg=Message).save()
			messages.success(request, 'Your Request added Successfully!!')
			return redirect('contact')
			
		else:
			messages.error(request, 'Please Fill the All Field !!')
			return redirect('contact')


		return render(request,'contact.html')


class EditProfile(View):
	def get(self, request):

		print("edit profile")
		return render(request,'edit_profile.html')
	def post(self, request):
		phone = request.POST.get("phone")
		bod = request.POST.get("bod")
		location = request.POST.get("location")
		father_name = request.POST.get("father_name")
		mother_name = request.POST.get("mother_name")
		web_site = request.POST.get("web_site")

		if 'resume' in request.FILES or 'resume' in request.FILES:
			resume= request.FILES['resume']
			profile= request.FILES['profile']

			JobSeeker_profile(
				user_type=request.user,
				bod=bod,location=location,
				father_name=father_name,
				mother_name=mother_name,
				web_site=web_site,
				resume=resume,
				).save()
			return redirect("JobSeeker_Profile")
		JobSeeker_profile(
				user_type=request.user,
				bod=bod,location=location,
				father_name=father_name,
				mother_name=mother_name,
				web_site=web_site
				).save()
		return redirect("JobSeeker_Profile")

