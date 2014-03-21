from django.conf.urls import patterns, include, url
from matchmaker import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'accounts/', include('social.apps.django_app.urls', namespace='social')),

    url(r'^$', TemplateView.as_view(template_name="matchup/home.html")),
    url(r'^matchup/$', views.matchUpRequest, name="matchup"),
    url(r'^matchups/(?P<matchid>\d+)/$', views.viewMatchUpRequest, name="matchup"),


    url(r'^login/', TemplateView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^accounts/view/(?P<username>.+)/$', views.viewProfile, name='profile'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^signup/', TemplateView.as_view(template_name='accounts/signup.html'), {'next_page': '/'}),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns +=  {
    url(r'', TemplateView.as_view(template_name="matchup/404.html")),
}
