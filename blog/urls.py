from django.conf.urls import url


from . import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^blog/(?P<slug>[-\w]+)/$', views.ArticleDetailView.as_view(), name='article-detail'),
    url(r'^blog/comments/(?P<article>[0-9]+)/$', views.add_comment, name='add_comment'),

]
