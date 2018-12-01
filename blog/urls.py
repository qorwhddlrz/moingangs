from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^subject/([가-힣]\w+)/$', views.post_list_search, name='post_list_grade'),
    url(r'^subject/([가-힣]\w+)/([가-힣]\w+)$', views.post_list_search, name='post_list_subject'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^accounts/register/$', views.register, name='register'),#
    url(r'^post/search/$',views.post_searchpage,name='post_searchpage'),
    url(r'^post/(?P<pk>\d+)/search/$',views.post_search,name='post_search'),
    url(r'^grade/$', views.add_grade_info, name='add_grade_info'),
    url(r'^grade/(?P<pk>\d+)$', views.grade_detail, name='grade_detail'),
    url(r'^grade/statistics/$', views.grade_list, name='grade_list'),
]
