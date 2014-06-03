from django.conf.urls import include, patterns, url

urlpatterns = patterns('together.dashboard.views',
    url(r'^$', "dashboard", name="dashboard"),
    url(r'^mi\-perfil/$', "mi_perfil", name="mi_perfil"),
    url(r'^proyecto_detalle/(?P<id_proyecto>\d+)/$', "ver_proyecto", name="ver_proyecto"),
    url(r'^actualizar_usuario/$', 'actualizar_usuario', name="actualizar_usuario"),
)

urlpatterns += patterns("together.mis_proyectos.views",
    url(r'^nuevo\-proyecto/',include("together.mis_proyectos.urls")),
)
