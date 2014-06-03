from django.conf.urls import patterns, url

urlpatterns = patterns("together.mis_proyectos.views",
    url(r'^tipo\-de\-proyecto/$','tipo_proyecto',name="tipo_proyecto"),
    url(r'^paso1/(\d+)/$',"nuevo_proyecto_paso1", name="nuevo_proyecto_paso1"),
    url(r'^guardar\-paso1/$',"guardar_paso1",name="guardar_paso1"),
    url(r'^paso2/$',"nuevo_proyecto_paso2", name="nuevo_proyecto_paso2"),
    url(r'^guardar\-paso2/$',"guardar_paso2",name="guardar_paso2"),
    url(r'^paso3/(?P<id_proyecto>\d+)/$', "nuevo_proyecto_paso3", name="nuevo_proyecto_paso3"),
)
