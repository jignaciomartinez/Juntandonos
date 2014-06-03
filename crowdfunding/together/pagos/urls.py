from django.conf.urls import patterns, url

urlpatterns = patterns('together.pagos.views',
	url(r'^$', 'pago', name='pago'),
    url(r"^pago\-primer\-paso/$","pago_primer_paso",name="pago_primer_paso"),
)
