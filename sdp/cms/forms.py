from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

from .models import Video


User = get_user_model()


class OtpForm(forms.Form):
	otp = forms.CharField(widget=forms.PasswordInput)
	



class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
	   
		# user_qs = User.objects.filter(username=username)
		# if user_qs.count() == 1:
		#     user = user_qs.first()
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect passsword")
			if not user.is_active:
				raise forms.ValidationError("This user is not longer active.")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email address')
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password'
		]



class Comments(forms.ModelForm):
	comment = forms.TextInput(attrs={'size': 10, 'title': 'Add Comments Please'})



def validate_file_extension(value):
	if not value.name.endswith('.pdf'):
		raise ValidationError(u'Error message')

class UploadFileForm(forms.ModelForm):
	recipe = forms.CharField(required = False,widget=forms.Textarea)
	time = forms.TimeField(widget=forms.TimeInput(attrs={'readonly':'readonly'},format='%H:%M:%S'))
	markers = forms.CharField(required = False,widget=forms.Textarea)



	class Meta:
		model = Video
		fields = ['title','cusine_type','recipe','video','time','markers','subtitle']




