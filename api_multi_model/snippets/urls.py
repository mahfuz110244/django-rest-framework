from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^contacts/$', views.ContactList.as_view()),
    url(r'^users/$', views.ContactUserList.as_view()),
    url(r'^attende/$', views.AttendeeView.as_view()),
    url(r'^attende/(?P<contact_id>[0-9]+)/$', views.AttendeeViewDetail.as_view()),
]