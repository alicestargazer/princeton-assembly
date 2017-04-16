from django.conf.urls import url

from . import views

app_name = 'visualizer'
#
# # visualizer/[whatever is matched by the regex]
# # url(regex, view, kwargs=None, name=None)
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'), # /visualizer/
    url(r'^(?P<pk>[-\w]+)/$', views.VisualizerView.as_view(), name='visualizer'),
    url(r'^(?P<problem_id>[0-9]+)/animate/(?P<instruction_id>[0-9]+)/$', views.animate, name='animate'),
    url(r'^(?P<problem_id>[0-9]+)/reset/$', views.reset, name='reset'),
    url(r'^(?P<pk>[0-9]+)/hello/$', views.HelloView.as_view(), name='hello'),
    url(r'^(?P<problem_id>[0-9]+)/hello/$', views.absvalform, name='helloform'),
    url(r'^(?P<pk>[0-9]+)/absval/$', views.AbsvalView.as_view(), name='absval'),
    url(r'^(?P<problem_id>[0-9]+)/absvalform/$', views.absvalform, name='absvalform'),
    url(r'^(?P<pk>[0-9]+)/uppercase/$', views.UppercaseView.as_view(), name='uppercase'),
    url(r'^(?P<problem_id>[0-9]+)/uppercaseform/$', views.uppercaseform, name='uppercaseform'),
    url(r'^(?P<pk>[0-9]+)/rect/$', views.RectView.as_view(), name='rect'),
    url(r'^(?P<problem_id>[0-9]+)/rectform/$', views.rectform, name='rectform'),
    url(r'^(?P<pk>[0-9]+)/power/$', views.PowerView.as_view(), name='power'),
    url(r'^(?P<problem_id>[0-9]+)/powerform/$', views.powerform, name='powerform'),
]
