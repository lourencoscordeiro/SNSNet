from django.conf.urls import url
from . import views

app_name = 'net'

urlpatterns = [

    # redirects to the login page
    # ex: /
    url(r'^$', views.login_redirect, name='login_redirect'),

    # ex: /login/
    url(r'^login/$', views.login_account, name='login_account'),

    # ex: /signup/
    url(r'^health_professional_signup/$', views.health_professional_signup,
        name='health_professional_signup'),

    # ex: /signup/
    url(r'^health_institution_signup/$', views.health_institution_signup,
        name='health_institution_signup'),

    # ex: /resend_email/
    url(r'^resend_email/$', views.resend_email, name='resend_email'),

    # ex: /feed/
    url(r'^feed/$', views.feed, name='feed'),

    # ex: /account/username
    url(r'^account/(?P<username>[\w\-]+)/$', views.account, name='account'),

    # ex: /logout/
    url(r'^logout/$', views.logout_account, name='logout_account'),

    # ex: /upload_image/
    url(r'^upload_image/$', views.upload_image, name='upload_image'),

    # ex: /update_personal_info/
    url(r'^update_personal_info/$', views.update_personal_info,
        name='update_personal_info'),

    # ex: /follow/username
    url(r'^follow/(?P<username>[\w\-]+)/$', views.follow, name='follow'),

    # ex: /unfollow/username
    url(r'^unfollow/(?P<username>[\w\-]+)/$', views.unfollow, name='unfollow'),

    # ex: /not_found/
    url(r'^not_found/$', views.not_found, name='not_found'),

    # ex: /search/
    url(r'^search/$', views.search, name='search'),

    # ex: /like/
    url(r'^like/$', views.like, name='like'),

    # ex: /delete_post/
    url(r'^delete_post/(?P<post_id>[0-9]+)/$',
        views.delete_post, name='delete_post'),

    # ex: /update_password/
    url(r'^update_password/$', views.update_password, name='update_password'),

]
