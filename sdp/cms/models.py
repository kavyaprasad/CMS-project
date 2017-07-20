import uuid
from django.db import models
from django.contrib.auth.models import User

    # Create your models here.

class Video(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=500)
	video = models.FileField(upload_to='videos')
	type_choices = (('Indian','Indian'), 
		('Japnese','Japnese'),
		('Chinese','Chinese'),
		('Mexican','Mexican'),
		('American','American'),
		('Italian','Italian'),
		('French','French'),
		('Asian','Asian'),
		('Others','Others'))
	cusine_type = models.CharField(max_length=1000,choices=type_choices)
	recipe = models.CharField(max_length=1000)
	uploaded_by = models.ForeignKey(User)
	time = models.TimeField()
	markers = models.CharField(max_length=1000)
	hits = models.IntegerField(default=0)
	subtitle = models.FileField(upload_to='subtitles')

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


	def __str__(self):
		return '%s,%s,%s' % (self.title,self.cusine_type,self.uploaded_by)

	def get_absloute_url(self):
		return reverse("video_search:search", kwargs={"id": self.id})



class Otp(models.Model):
	otp_umber = models.IntegerField(default=0)
	user_name = models.CharField(max_length=1000)
	user_email = models.CharField(max_length=1000)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	def __str__(self):
		return '%d,%s,%s,' % (self.otp_umber,self.user_name,self.user_email)



class FacebookUser(models.Model):
	user_name = models.CharField(max_length=10000)
	user_password = models.BinaryField()
	encrypted_password = models.CharField(max_length=1000)
	user_email = models.CharField(max_length=1000)
	auth_token = models.CharField(max_length=1000)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	
	def __str__(self):
		return '%s,%s,' % (self.user_name,self.user_email)


class Ads(models.Model):
	ad = models.FileField(upload_to='videos/ads')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)



class CommentsVideo(models.Model):
	video = models.ForeignKey(Video,on_delete=models.CASCADE)
	comment = models.CharField(max_length=10000)
	comment_by= models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return '%s,%s,%s,' % (self.video,self.comment,self.comment_by)



class FormsVideo(models.Model):
	video = models.ForeignKey(Video,on_delete=models.CASCADE)
	value = models.CharField(max_length=10000)
	comment_by= models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return '%s,%s,%s,' % (self.video,self.value,self.comment_by)



class Report(models.Model):
	video = models.ForeignKey(Video,on_delete=models.CASCADE)
	report_by = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		unique_together = (('video', 'report_by'))


	def __str__(self):
		return '%s,%s,' % (self.video,self.report_by)

class Views(models.Model):
	video = models.ForeignKey(Video,on_delete=models.CASCADE)
	hits = models.IntegerField(default=0)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return '%s,%s,' % (self.video,self.hits)



class Rating(models.Model):
	rating = models.IntegerField(default=0)
	video = models.ForeignKey(Video,on_delete=models.CASCADE)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		unique_together = (('video', 'user'))

	def __str__(self):
		return '%s,%s,' % (self.video,self.rating)

class Dislikes(models.Model):
	rating = models.IntegerField(default=0)
	video = models.ForeignKey(Video,on_delete=models.CASCADE)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		unique_together = (('video', 'user'))

	def __str__(self):
		return '%s,%s,' % (self.video,self.rating)









class AddtoPlayList(models.Model):
	# rating = models.IntegerField(default=0)
	video = models.ForeignKey(Video,on_delete=models.CASCADE)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		unique_together = (('video', 'user'))

	def __str__(self):
		return '%s,%s,' % (self.video,self.user)


class Subscribe(models.Model):
	user_subscribed = models.ForeignKey(User,related_name="subscribeduser")
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		unique_together = (('user_subscribed', 'user'))

	def __str__(self):
		return '%s' % (self.user)





class PremiumMember(models.Model):
	rating = models.CharField(max_length=1000)
	# video = models.ForeignKey(Video,on_delete=models.CASCADE)
	user = models.ForeignKey(User,unique=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return '%s,%s,' % (self.rating,self.user)

