"""authi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import ( password_reset,password_reset_done,password_reset_confirm,password_reset_complete)
from module.views import (quiz,dislikes,commentdelete,login_user, register_view, logout_view,display,upload,display,otp,otp_confirm,landing,videodetail,search,facebook,report,admin_report,rating,comments,ajax_test,home,videodelete,delete,formdata,form_report,test,addtoplaylist,viewsadmin,premiummember,subscribe,notification,myfav,analytics,useranalytics)

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    url(r'^facebook/$', facebook, name='facebook'),
    url(r'^addtoplaylist/$', addtoplaylist, name='addtoplaylist'),
    url(r'^text/$', test, name='text'),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_user, name='login'),
    url(r'^otp/', otp, name='otp'),
    url(r'^quiz/', quiz, name='quiz'),
    url(r'^rating/', rating, name='rating'),
    url(r'^otp_confirm/', otp_confirm, name='otp_login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^$', login_user, name='login'),
    url(r'^insert/', upload, name='upload'),
    url(r'^landing/$',  landing,name="landing page"),    
    url(r'^search/', search, name='search'),
    url(r'^report/', report, name='report'),
    url(r'^comments/', comments, name='comments'),
    url(r'^formdata/', formdata, name='formdata'),
    url(r'^ajax_test/$', ajax_test, name='ajax_test'),
    url(r'^home/', home, name='home'),
    url(r'^formreport/', form_report, name='form_report'),
    url(r'^mostviewed/', viewsadmin, name='viewsadmin'),
    url(r'^premiummember/', premiummember, name='premiummember'),
    url(r'^subscribe/', subscribe, name='subscribe'),
    url(r'^notification/', notification, name='notification'),
    url(r'^fav/', myfav, name='myfav'),
    url(r'^dislikes/', dislikes, name='dislikes'),
    url(r'^commentdelete/(?P<id>[0-9A-Za-z_\-]+)/$', commentdelete, name='commentdelete'),
    url(r'^useranalytics/', useranalytics, name='myfav'),
    url(r'^analytics/', analytics, name='analytics'),
    url(r'^deletevideo/(?P<id>[0-9A-Za-z_\-]+)/$', videodelete, name='deletevideo'),
    url(r'^delete/(?P<id>[0-9A-Za-z_\-]+)/$', delete, name='delete'),
    url(r'^adminreport/', admin_report, name='adminreport'),
    url(r'^videodetail/(?P<id>[0-9A-Za-z_\-]+)/$',  videodetail),
    url(r'^password-reset/$',password_reset,name='reset_password'),
    url(r'^password-reset/done/$',password_reset_done,name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','django.contrib.auth.views.password_reset_confirm',name='password_reset_confirm'),
    url(r'^reset-password/complete/$',password_reset_complete,name='password_reset_complete')
         # url(r'^password-reset/done/$',password_reset_done,name='password_reset_done'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
