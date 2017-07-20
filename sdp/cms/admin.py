from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Video,FacebookUser,Otp,Ads,Report,Views,Rating,FormsVideo,AddtoPlayList,Subscribe,PremiumMember,FormsVideo


class FacebookUserAdmin(admin.ModelAdmin):
	
	list_display = ["user_name","user_password","user_email"]

	class Meta:
		model = FacebookUser


class OtpAdmin(admin.ModelAdmin):
	
	list_display = ["user_name","otp_umber","user_email",]

	class Meta:
		model = Otp
class VideoAdmin(admin.ModelAdmin):
	list_display = ["id","title","cusine_type","recipe","uploaded_by"]

	class Meta:
		model = Video



class AddAdmin(admin.ModelAdmin):
	

	class Meta:
		model = Ads

admin.site.register(Video,VideoAdmin)
admin.site.register(FacebookUser, FacebookUserAdmin)
admin.site.register(Otp, OtpAdmin)
admin.site.register(Report)
admin.site.register(AddtoPlayList)
admin.site.register(Subscribe)
admin.site.register(PremiumMember)




admin.site.register(FormsVideo)
admin.site.register(Views)
admin.site.register(Rating)
admin.site.register(Ads, AddAdmin)
