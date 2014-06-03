from django.conf.urls import patterns, url

urlpatterns = patterns('together.registro.views',
    url(r'^$', 'registro', name='registro'),
    url(r'^registro_fb/$', 'registro_fb', name='registro_fb'),
    url(r'^obtener_comunas/$','obtener_comunas', name="obtener_comunas"),
    url(r'^verificar_usuario/$',"verificar_usuario", name="verificar_usuario"),
    url(r'^recuperar_clave/$',"recuperar_clave", name="recuperar_clave"),
    url(r'^envio/$', "envio", name="envio"),
    url(r'^actualizar_clave/$',"actualizar_clave",name="actualizar_clave"),
)

