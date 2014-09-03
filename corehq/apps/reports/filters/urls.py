from django.conf.urls.defaults import *

from . import api

urlpatterns = patterns('',
    url(r'^emwf_options/$', api.EmwfOptionsView.as_view(), name='emwf_options'),
    url(r'^emwf_options/all-data/$', api.EmwfOptionsView.as_view(), {'all_data':True}, name='emwf_options_with_all_data'),
    url(r'^emwf_options/share-groups/$', api.EmwfOptionsView.as_view(), {'share_groups':True}, name='emwf_options_with_share_groups'),
)
