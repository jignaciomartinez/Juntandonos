# -*- coding: utf8 -*-
import os, json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.views.generic import View, TemplateView

from ..models import ComprobantePago, Mensaje, Proyecto, TipoPago
from ..common import is_text_valid, is_email_valid, is_number_valid, Http500, mail_aporte

class PagoView(TemplateView):
    def get(self, req):
        return render_to_response("pagos/pago.html",context_instance=RequestContext(req))

    @transaction.commit_on_success
    def post(self, req):
    	nombre = req.POST.get("nombre")
    	mensaje = req.POST.get("mensaje")
    	email = req.POST.get("email")
    	monto = req.POST.get("monto")
    	forma_pago = req.POST.get("tipo_pago")

        id_proyecto = self.request.session['id_this_proyect']

        valido = True
        valido = valido and is_text_valid(nombre, 140)
        valido = valido and is_email_valid(email)
        valido = valido and is_text_valid(mensaje, 500)
        valido = valido and is_number_valid(monto)

        if not valido:
            raise Http500()

        proyecto = Proyecto.objects.get(pk = id_proyecto)
        tp = TipoPago.objects.get(pk = forma_pago)
        usuario = User.objects.get(pk = self.request.user.id)

    	cp = ComprobantePago()
    	cp.usuario = usuario
    	cp.monto = monto
    	cp.tipo_pago = tp
    	cp.proyecto = proyecto
    	cp.save()

    	m = Mensaje()
    	m.comprobante_pago = cp
    	m.mensaje = mensaje
        m.save()
        creador = User.objects.get(username = proyecto.creador)
        nombre = creador.username
        correo = creador.email
        aportador = nombre
        aportes = monto
        nombre_proyecto = proyecto.titulo

        mail_aporte(nombre, aportador, aportes, nombre_proyecto, correo)

        return redirect("ver_proyecto", id_proyecto = id_proyecto)

class PagoPrimerPasoView(TemplateView):
    template_name = "pagos/pago_primer_paso.html"

pago = login_required(PagoView.as_view())
pago_primer_paso = PagoPrimerPasoView.as_view()
