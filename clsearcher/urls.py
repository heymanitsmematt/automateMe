from django.conf.urls import patterns
from django.views.generic import TemplateView
from clsearcher.views import UpdateView, NewEntry, Main
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    (r'^', Main.as_view()),
    (r'^clUpdate/$', UpdateView.as_view()),
    (r'^NewEntry/$', csrf_exempt(NewEntry.as_view())),
)
