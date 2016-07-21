from django.conf.urls import url
from django.contrib import admin


from . views import (
     principal,
     post,
     detalle_post,
     login_view,
     register_view,
     logout_view,

)

urlpatterns = [
    url(r'^$', principal,name="inicio"),
    url(r'^casos/$',post, name="casos"),
    url(r'^(?P<caso_id>[0-9]+)/$', detalle_post, name='detail'),
    url(r'^login/$',login_view,name='vista_login'),
    url(r'^registro/$',register_view,name='vista_registro'),
     url(r'^logout/$',logout_view,name='vista_logout'),

    
]

    
