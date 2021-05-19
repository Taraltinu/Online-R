from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreation_Form,UserChange_form
from .models import *



class MyUserAdmin(UserAdmin):
	add_form = UserCreation_Form
	form  =  UserChange_form
	list_display = ("email","is_active","is_staff")
	list_filter = ("is_active","last_login")

	fieldsets = ( 
			(None ,{"fields":('email','password',"profile")}),
			("permissions",{"fields":("is_active","is_staff")}),
		)
	add_fieldsets =( 
		(None,{
			"classes":("wide"),
			"fields":("email","password","password2",'first_name', 'last_name',)
			})
	
		)
	# add_fieldsets = (
 #        (None, {
 #            'classes': ('wide',),
 #            'fields': ('email',"first_name","last_name", 'password1', 'password2')}
 #        ),
 #    )
	search_fields = ("email",)
	ordering = ("email",)
	filter_horizontal  = []

# admin.site.unregister(User)
admin.site.register(MyUser,MyUserAdmin)


#company account

admin.site.register(Campnay_profile)
admin.site.register(Job_Type)

admin.site.register(Add_Job_Model)

admin.site.register(Job_Category)
admin.site.register(Applied_job)
admin.site.register(JobSeeker_profile )
admin.site.register(Add_Degree)