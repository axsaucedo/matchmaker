from django.conf.urls import patterns, include, url
from matchmaker import views
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'accounts/', include('social.apps.django_app.urls', namespace='social')),

    url(r'^$', TemplateView.as_view(template_name="home.html")),
    url(r'^matchup/$', views.matchUpRequest, name="matchup"),

    url(r'', TemplateView.as_view(template_name="404.html")),
)
