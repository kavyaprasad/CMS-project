from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)
from django.http import JsonResponse
from .models import Otp,Video,FacebookUser,Report,Views,Rating,CommentsVideo,FormsVideo,AddtoPlayList,PremiumMember,Subscribe,Dislikes
from .forms import UserLoginForm, UserRegisterForm,UploadFileForm,OtpForm
from django.contrib.auth.models import User
import string, random
from Crypto.Cipher import DES
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Count,Q
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from _thread import *
import _thread as thread
from django.http import Http404
from django.http import JsonResponse
from datetime import datetime, timedelta
today = datetime.now().date()
from django.core import serializers
import json
import operator
from slacker import Slacker
slack = Slacker("xoxb-174704496901-b9nHNmAqe88EAgEnJrgJXA42")




def display(request):
	logout(request)
	return render(request,"display.html")



def register_view(request):
	logout(request)
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		form = UserRegisterForm()
		messages.success(request,"Successfully Registerd Please Login To Continue",extra_tags='safe')
		slack.chat.post_message('#feedmeserver',"A New Registraion")
	context = {
		"form": form,
		"title": title
	}
	return render(request, "register.html", context)





def login_user(request):
	logout(request)
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		slack.chat.post_message('#feedmeserver',"A Userlogin")
		return HttpResponseRedirect("/otp/")          

	return render(request, "login.html", {"form":form, "title": title})



def facebook(request): # Method is a Fuctionality Does not Give a HTML 
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		get_email = request.POST.get('email') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_name = request.POST.get('name')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		get_auth_token = request.POST.get('authtoken')# Taking The DATA from front end in form of POST to Django FACE BOOK USER AUTH TOKEN
		queryset_list = User.objects.all().values_list("email",flat=True)# Performing a Django Query and getting all Django Users Email Address 
		letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcedfghijklmnopqrstuvwxyz1234567890!@#$%^&*()"
		random_string = ''.join(random.choice(letters) for x in range(8))        
		text = random_string
		des = DES.new('01234567', DES.MODE_ECB)
		encrypted = des.encrypt(text)
		abc = str(encrypted)
		slack.chat.post_message('#feedmeserver',"A FacebookUserLogin")
		if get_email in queryset_list:
			query = FacebookUser.objects.filter(user_email=get_email)
			username = query[0].user_name
			abc = query[0].user_password
			ijk =  (bytes(abc))
			efg = des.decrypt(ijk)
			gg =  (str(efg))
			password = gg[2:][:-1]
			user_new = authenticate(username=username, password=password)
			login(request, user_new)
		else:
			fbinstance = User.objects.create_user(username=get_name,email=get_email,password=text)
			fbinstance.save()
			fbuser = FacebookUser.objects.create(user_name=get_name,user_email=get_email,user_password=encrypted,auth_token=get_auth_token,encrypted_password=abc)
			query = FacebookUser.objects.filter(user_email=get_email)
			username = query[0].user_name
			abc = query[0].user_password
			ijk =  (bytes(abc))
			efg = des.decrypt(ijk)
			gg =  (str(efg))
			password = gg[2:][:-1]
			user = authenticate(username=username, password=password)
			login(request, user)
	return HttpResponse('')



@login_required
def otp(request):
	user = (request.user)
	email_id = (request.user.email)
	my_list = []
	for x in range(1):
		my_otp = random.randint(100,900)*126
		my_list.append(my_otp)
	otp = my_list[0]
	otp_instance = Otp.objects.create(otp_umber=otp,user_name=user,user_email=email_id)
	send_mail('HI your OTP to Login to 127.0.0.1:8000 is ', 'Your OTP     '+ str(otp), 'feedmeapp1@gmail.com', [email_id], fail_silently=False)
	return HttpResponseRedirect("/otp_confirm/")      



@login_required
def otp_confirm(request):
	title = "OTP LOGIN"
	form = OtpForm(request.POST or None)
	queryset_list = Otp.objects.all().order_by("-timestamp")
	form = OtpForm(request.POST or None)
	if form.is_valid():
		otp = form.cleaned_data.get("otp")
		otp_get = queryset_list.filter(Q(user_name=request.user)&Q(otp_umber=otp))
		try:
			otp_get_latest = otp_get.latest("timestamp")
			return HttpResponseRedirect("/landing/")      
		except:
			messages.success(request,"Invalid OTP",extra_tags='safe')
	context = {
	"form":form,
	"title":title
	}
	return render(request,"otp.html",context) 

@login_required
def logout_view(request):
	logout(request)
	slack.chat.post_message('#feedmeserver',"A User Logout")
	return redirect("/login/")


#########################################################################################################
########################################################################################################
############## AUTH ENDS ##############################################################################



@login_required
def landing(request):
	instance = get_object_or_404(Video, id="e6c36609-abb5-46cd-9390-292aa386af92")
	queryset = Video.objects.all().order_by("-timestamp")
	rel_instance = instance.commentsvideo_set.all()
	try:
		ijk = PremiumMember.objects.get(user=request.user)
	except PremiumMember.DoesNotExist:
		ijk = None
	hits = Views.objects.create(video_id="e6c36609-abb5-46cd-9390-292aa386af92",hits="1",user=request.user)
	query = Views.objects.filter(video_id="e6c36609-abb5-46cd-9390-292aa386af92")
	count = query.count()
	likes = Rating.objects.filter(video_id="e6c36609-abb5-46cd-9390-292aa386af92")
	dislikes = Dislikes.objects.filter(video_id="e6c36609-abb5-46cd-9390-292aa386af92")
	dislik = dislikes.count()
	likes_count = likes.count()	
	marker = instance.markers
	myList = [item for item in marker.split('\n')]
	abc = str(myList)	
	markers = abc[2:][:-2]
	qury = Subscribe.objects.filter(user=request.user).order_by("-timestamp")
	lis = []
	for qu in qury:
		if request.user == qu.user:
			third = Video.objects.filter(uploaded_by_id=qu.user_subscribed)
			lis.append(third)
		else:
			lis.append("No Notification")
	secondlis = []
	for l in lis:
		for video in l:
			# abc = video.timestamp.sort()
			secondlis.append(video)
	print(secondlis)
	# index, value = max(enumerate(secondlis), key=operator.itemgetter(1))
	if secondlis == []:
		notification = "No Notification"
		li = [notification]
	else:
		notification = secondlis[-1]
		li = [notification]

	print(li)
	context = {
		"rel_instance":rel_instance,
		"instance": instance,
		"title": instance.id,
		"queryset":queryset,
		"markers":markers,
		"count":count,
		"likes_count":likes_count,
		"tom":ijk,
		"notification":li,
		"dislikes_count":dislik
	}
	return render(request, "searchdetail.html",context)




@login_required
def upload(request):
	form = UploadFileForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.uploaded_by = request.user
		print(instance.video)
		instance.save()
		form = UploadFileForm()
		slack.chat.post_message('#feedmeserver',"A New VideoUpload")
		messages.success(request,'Successfully Uploaded',extra_tags='safe')

	context = {
		"title": "Upload A New Video",
		"form": form,
		}
	return render(request, "upload.html",context)



@login_required
def search(request):

	queryset_list = Video.objects.all().order_by("-timestamp")
	hits = Views.objects.all()
	query = request.GET.get("q")
	query2 = request.GET.get("browser") 
	try:
		if query2 == "Title":
			title = query2.lower()
			if query:
				queryset_list = queryset_list.filter(Q(title__icontains=query)).distinct()
			if queryset_list.exists():
				messages.success(request,str(queryset_list.count())+' Videos Found For The Title',extra_tags='safe')
			else:
				messages.success(request,'Videos Not Found For The Title',extra_tags='safe')

		if query2 == "Cuisine":
			title = query2
			if query:
				queryset_list = queryset_list.filter(Q(cusine_type__iexact=query)).distinct()
			if queryset_list.exists():
				messages.success(request,str(queryset_list.count())+' Videos Found For The Cuisine',extra_tags='safe')
			else:
				messages.success(request,'Videos Not Found For The Cuisine',extra_tags='safe')

		if query2 == "User":
			title = query2
			if query:
				queryset_list = queryset_list.filter(Q(uploaded_by__username__icontains=query)).distinct()
			if queryset_list.exists():
				messages.success(request,str(queryset_list.count())+' Videos Found For The User',extra_tags='safe')
			else:
				messages.success(request,'Videos Not Found For The User',extra_tags='safe')

		if query2 == "Tag":
			title = query2
			if query:
				queryset_list = queryset_list.filter(Q(markers__icontains=query)).distinct()
			if queryset_list.exists():
				messages.success(request,str(queryset_list.count())+' Videos Found For The Tag',extra_tags='safe')
			else:
				messages.success(request,'Videos Not Found For The Tag',extra_tags='safe')
	except:
		messages.success(request,'BAD REQUEST',extra_tags='safe')


	element_list = queryset_list
	paginator = Paginator(queryset_list, 20) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {

		"object_list": queryset,
		"element_list": element_list,
		"lastWeek":datetime.now()- timedelta(days=7),
		"lastMonth":datetime.now()- timedelta(days=30),
		"title": " Search ",
		"hits":hits

	}
	return render(request, "searchpage.html",context)



@login_required
def videodetail(request,id):
	instance = get_object_or_404(Video, id=id)
	queryset = Video.objects.all().order_by("-timestamp")
	rel_instance = instance.commentsvideo_set.all()
	try:
	        ijk = PremiumMember.objects.get(user=request.user)
	except PremiumMember.DoesNotExist:
		ijk = None
	hits = Views.objects.create(video_id=id,hits="1",user=request.user)
	query = Views.objects.filter(video_id=id)
	count = query.count()
	likes = Rating.objects.filter(video_id=id)
	dislikes = Dislikes.objects.filter(video_id=id)
	dislik = dislikes.count()
	likes_count = likes.count()	
	marker = instance.markers
	myList = [item for item in marker.split('\n')]
	abc = str(myList)	
	markers = abc[2:][:-2]
	qury = Subscribe.objects.filter(user=request.user).order_by("-timestamp")
	lis = []
	for qu in qury:
		if request.user == qu.user:
			third = Video.objects.filter(uploaded_by_id=qu.user_subscribed)
			lis.append(third)
		else:
			lis.append("No Notification")
	secondlis = []
	for l in lis:
		for video in l:
			# abc = video.timestamp.sort()
			secondlis.append(video)
	print(secondlis)
	# index, value = max(enumerate(secondlis), key=operator.itemgetter(1))
	if secondlis == []:
		notification = "No Notification"
		li = [notification]
	else:
		notification = secondlis[-1]
		li = [notification]

	print(li)
	context = {
		"rel_instance":rel_instance,
		"instance": instance,
		"title": instance.id,
		"queryset":queryset,
		"markers":markers,
		"count":count,
		"likes_count":likes_count,
		"tom":ijk,
		"notification":li,
		"dislikes_count":dislik
	}
	return render(request, "searchdetail.html",context)


@login_required
def report(request):
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		get_id = request.POST.get('id') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_user = request.POST.get('user')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		query = Video.objects.filter(id=get_id)
		new_report = Report.objects.create(video_id=get_id,report_by=request.user)
		# messages.success(request,'Successfully Reported',extra_tags='safe')
	return HttpResponse('')

@login_required
def rating(request):
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		get_id = request.POST.get('id') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_user = request.POST.get('user')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		query = Video.objects.filter(id=get_id)
		new_report = Rating.objects.create(video_id=get_id,rating="1",user=request.user)

	return HttpResponse('')



@login_required
def addtoplaylist(request):
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		get_id = request.POST.get('id') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_user = request.POST.get('user')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		query = Video.objects.filter(id=get_id)
		new_report = AddtoPlayList.objects.create(video_id=get_id,user=request.user)

	return HttpResponse('')






@login_required
def comments(request):
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		get_id = request.POST.get('id') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_user = request.POST.get('user')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		get_comments = request.POST.get('comment')
		new_report = CommentsVideo.objects.create(video_id=get_id,comment=get_comments,comment_by=request.user)

	return HttpResponse('')


@login_required
def formdata(request):
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		get_id = request.POST.get('id') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_user = request.POST.get('user')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		get_form = request.POST.get('form')
		new_report = FormsVideo.objects.create(video_id=get_id,value=get_form,comment_by=request.user)
	return HttpResponse('')


@login_required
def premiummember(request):
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		get_id = request.POST.get('id') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_user = request.POST.get('user')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		# get_form = request.POST.get('form')
		new_report = PremiumMember.objects.create(rating="True",user=request.user)
	return HttpResponse('')


@login_required
def subscribe(request):
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		# get_id = request.POST.get('id') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_user = request.POST.get('user')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		# get_form = request.POST.get('form')
		print(get_user)
		new_report = Subscribe.objects.create(user_subscribed_id=get_user,user=request.user)
	return HttpResponse('')


@login_required
def dislikes(request):
	if request.method == 'POST': # From Frontend we are getting the data in a POST method and we are checking if front end is giving POST Method or not 
		get_id = request.POST.get('id') # Taking The DATA from front end in form of POST to Django FACE BOOK USER EMAIL ADDRESS
		get_user = request.POST.get('user')# Taking The DATA from front end in form of POST to Django FACE BOOK USER NAME
		query = Video.objects.filter(id=get_id)
		new_report = Dislikes.objects.create(video_id=get_id,rating="1",user=request.user)
		#messages.success(request,'Successfully Disliked ',extra_tags='safe')
	return HttpResponse('')





@login_required
def notification(request):
	query = Subscribe.objects.filter(user=request.user).order_by("-timestamp")
	lis = []
	for qu in query:
		third = Video.objects.filter(uploaded_by_id=qu.user_subscribed)
		lis.append(third)
	# print(lis)
	secondlis = []
	for l in lis:
		for video in l:
			# abc = video.timestamp.sort()
			secondlis.append(video)
	# index, value = max(enumerate(secondlis), key=operator.itemgetter(1))
	# notification = secondlis[-1]
	# li = [notification]
	# print(type(li))
	context = {	"object_list": secondlis}

	return render(request, "subscribe.html",context)



@login_required
def analytics(request):
	queryset_list = Video.objects.all().order_by("-timestamp")
	mylis = []
	for obj in queryset_list:
		abc = obj.views_set.count()
		efg = obj.title
		listto = [efg,abc]
		mylis.append(listto)
		context = {	"object_list": mylis}

	return render(request, "analyticsviews.html",context)



@login_required
def useranalytics(request):
	queryset_list = Video.objects.all().order_by("-timestamp")
	mylis = []
	for obj in queryset_list:
		# abc = obj.uploaded_by.count()
		efg = obj.uploaded_by.username
		listto = [efg]
		mylis.append(efg)
	my_dict = {i:mylis.count(i) for i in mylis}
	lis = []
	for key,value in my_dict.items():
		# print(key,value)
		tolis = [key,value]
		lis.append(tolis)
	print(lis)
	context = {	"object_list": lis}

	return render(request, "useranalytics.html",context)

@login_required
def quiz(request):
	queryset_list = FormsVideo.objects.all().order_by("-timestamp")
	mylis = []
	for obj in queryset_list:
		# abc = obj.uploaded_by.count()
		efg = obj.value
		listto = [efg]
		mylis.append(efg)
	# print(mylis)
	my_dict = {i:mylis.count(i) for i in mylis}
	lis = []
	for key,value in my_dict.items():
		# print(key,value)
		tolis = [key,value]
		lis.append(tolis)
	print(lis)
	context = {	"object_list": lis}

	return render(request, "quizanalytics.html",context)





@login_required
def myfav(request):
	queryset_list = AddtoPlayList.objects.filter(user=request.user)
	paginator = Paginator(queryset_list, 30) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	context = {
	"object_list": queryset_list,
	}
	return render(request, "myfav.html",context)


@login_required
def form_report(request):
	if request.user.is_active and request.user.is_staff:
		queryset_list = FormsVideo.objects.all().order_by("-timestamp")
		paginator = Paginator(queryset_list, 30) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			queryset = paginator.page(1)
		except EmptyPage:
			queryset = paginator.page(paginator.num_pages)
		context = {
		"object_list": queryset_list,
		}
		return render(request, "formdata.html",context)


	else:
		raise Http404("Wrong Page")

@login_required
def admin_report(request):
	if request.user.is_active and request.user.is_staff:
		queryset_list = Report.objects.all().order_by("-timestamp")
		paginator = Paginator(queryset_list, 30) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			queryset = paginator.page(1)
		except EmptyPage:
			queryset = paginator.page(paginator.num_pages)
		context = {
		"object_list": queryset_list,
		}
		return render(request, "admin.html",context)


	else:
		raise Http404("Wrong Page")


@login_required
def viewsadmin(request):
	if request.user.is_active and request.user.is_staff:
		queryset_list = Video.objects.all().order_by("-timestamp")
		paginator = Paginator(queryset_list, 30) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			queryset = paginator.page(1)
		except EmptyPage:
			queryset = paginator.page(paginator.num_pages)
		context = {
		"object_list": queryset_list,
		}
		return render(request, "views.html",context)


	else:
		raise Http404("Wrong Page")



@login_required
def commentdelete(request,id):
	if request.user.is_active and request.user.is_staff:
		u = CommentsVideo.objects.get(pk=id).delete()
		messages.success(request,'Successfully Deleted ',extra_tags='safe')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		raise Http404("Wrong Page")






@login_required
def delete(request,id):
	if request.user.is_active and request.user.is_staff:
		u = Video.objects.get(pk=id).delete()
		messages.success(request,'Successfully Deleted ',extra_tags='safe')
		return HttpResponseRedirect("/adminreport/")
	else:
		raise Http404("Wrong Page")



@login_required
def videodelete(request,id):
	if request.user.is_active and request.user.is_staff:
		instance = get_object_or_404(Video, id=id)
		rel_instance = instance.report_set.all()
		rel_instance1 = instance.commentsvideo_set.all()
		context = {
		"rel_instance":rel_instance,
		"instance": instance,
		"rel_instance1":rel_instance1
		}
		return render(request, "deletedetail.html",context)
	else:
		raise Http404("Wrong Page")


def home(request):
	return render_to_response('home.html', {},
						  context_instance=RequestContext(request))


def Populate_Config_Resources():
	queryset_list = CommentsVideo.objects.all().order_by("-timestamp")
	data = queryset_list
	return data

def ajax_test(request):
	if request.is_ajax():
		config_data = Populate_Config_Resources()
	else:
		message = "Not ajax"
	return HttpResponse(config_data)

def test(request):
	return render_to_response('text.html', {},
						  context_instance=RequestContext(request))

