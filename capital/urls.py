
from django.conf.urls import patterns, include, url

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from app.views import *
from django.core.urlresolvers import reverse
from django.contrib import admin


admin.site.site_header = 'Perfecto Remore'

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', 'jwt_auth.views.obtain_jwt_token'),
    url(r'api-token-refresh/', refresh_jwt_token),
    url(r'^', admin.site.urls),

    url(r'^categoria/', 'app.views.categoria'),
    url(r'^detalle/(\d+)', 'app.views.detalle'),
    url(r'^menu/(\d+)', 'app.views.menu'),
    url(r'^distrito/', 'app.views.distrito'),
    url(r'^subcategoria/(\d+)', 'app.views.subcategoria'),
    url(r'^portadaphoto/', 'app.views.portadaphoto'),
    url(r'^buscasocia/(\d+)',  Buscasocia.as_view()),
    url(r'^guardanotificacion/', Guardanotificacion.as_view()),
    url(r'^aceptarservicio/', Aceptarservicio.as_view()),
    url(r'^miservicios/', Miservicios.as_view()),
    url(r'^miserviciossocias/(\d+)', Miserviciossocias.as_view()),
    url(r'^sacauser/', Sacauser.as_view()),
    url(r'^sacasocia/', Sacasocia.as_view()),
    url(r'^detalleservicio/(\d+)', Detalleservicio.as_view()),

    url(r'^miperfil/', Miperfil.as_view()),
    url(r'^detalledeservicio/(\d+)', 'app.views.detalledeservicio'),
    url(r'^smsrecibidos', 'app.views.smsrecibidos'),
    url(r'^smsrecibidos/', 'app.views.smsrecibidos'),
    url(r'^prueba/', 'app.views.prueba'),
    url(r'^registro/', 'app.views.registro'),
    url(r'^ultimoservicio/', Ultimoservicio.as_view()),
    url(r'^nuevasocia/', 'app.views.nuevasocia'),
    url(r'^envianotificacion/(\w+)/', 'app.views.envianotificacion'),
    url(r'^carganoti/(\w+)/(\d+)', 'app.views.carganoti'),
    url(r'^contacto/', 'app.views.contacto'),
    url(r'^help/', 'app.views.help'),


    
]
