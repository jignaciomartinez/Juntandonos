#-*- coding: utf-8 -*-
import json
import calendar
from datetime import datetime, date

from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View, TemplateView

from ..models import DetalleUsuario
from ..common import is_text_valid, is_email_valid, mail_sender_new_account

class RegistroView(TemplateView):
    template_name = "registro/registro.html"

    def get(self, req):
        if req.user.is_authenticated():
            return redirect("dashboard")

        data = {
            "dias" : [i + 1 for i in range(31)],
            "meses" : [],
            "anios" : [i for i in range(1975, datetime.now().year - 15)]
        }

        data["anios"] = sorted(data["anios"],reverse=True)

        for monthnumber in range(1,13):
            data["meses"].append({
                "valor" : monthnumber,
                "nombre" : calendar.month_name[monthnumber]
            })

        return render_to_response("registro/registro.html",data,context_instance=RequestContext(req))

def obtener_comunas(req):
    region_id = req.GET.get("region")
    comunas = Comuna.objects.filter(region_id=region_id)
    data = []

    for comuna in comunas:
        data.append({
            "id" : comuna.id,
            "nombre" : comuna.nombre
        })

    return HttpResponse(json.dumps(data))


def verificar_usuario(req):
    email = req.GET.get("email")
    username = req.GET.get("username")
    mensaje_usuario = None
    mensaje_email = None

    try:
        username_exist = User.objects.get(username = username)

        if username_exist:
            mensaje_usuario = "El nombre de usuario ya existe"

    except User.DoesNotExist as e:
        pass

    try:
        email_exist = User.objects.get(email = email.lower())

        if email_exist:
            mensaje_email = "El correo ya existe"

    except User.MultipleObjectsReturned as mor:
        mensaje_email = "El correo ya existe"
    except User.DoesNotExist as dne:
        pass

    data = {
        "existe" : mensaje_usuario or mensaje_email or False,
        "mensajeUser" : mensaje_usuario,
        "mensajeEmail" : mensaje_email
    }

    return HttpResponse(json.dumps(data))


class EnvioView(View):
    @transaction.commit_on_success
    def post(self, req):
        self.nombre_usuario = req.POST.get("nombre_usuario")
        self.email = req.POST.get("email")
        self.clave = req.POST.get("password")
        self.sexo = req.POST.get("sexo")
        self.dia = req.POST.get("dia")
        self.mes = req.POST.get("mes")
        self.anio = req.POST.get("anio")

        valido = True
        valido = valido and is_text_valid(self.nombre_usuario)
        valido = valido and is_email_valid(self.email)
        valido = valido and is_text_valid(self.clave)
        valido = valido and is_text_valid(self.sexo)
        valido = valido and is_text_valid(self.dia)
        valido = valido and is_text_valid(self.mes)
        valido = valido and is_text_valid(self.anio)

        if valido:
            self.__guardar_usuario()

        return render_to_response("registro/registro_exitoso.html")

    def __guardar_usuario(self):
        user = User()
        user.username = self.nombre_usuario
        user.email = self.email.lower()
        user.is_staff = False
        user.is_active = True
        user.set_password(self.clave)
        user.save()

        fecha_nacimiento = date(int(self.anio), int(self.mes), int(self.dia))

        detalle = DetalleUsuario()
        detalle.fecha_nacimiento = fecha_nacimiento
        detalle.usuario = user
        detalle.sexo = self.sexo
        detalle.save()
        mail_sender_new_account(self.email.lower(), self.clave, self.nombre_usuario)


class RegistroFbUserView(View):
    def post(self, req):
        password = "juntandonos.com"
        email = req.POST.get("user_name")+"@facebook.com"
        username = req.POST.get("user_name")

        try:
            username_exist = User.objects.get(username = username)

            if username_exist:
                user = username_exist

        except User.DoesNotExist as e:
            user = User()
            user.username = username
            user.email = email.lower()
            user.is_staff = False
            user.is_active = True
            user.set_password(password)
            user.save()

        sexo = req.POST.get("sexo") == "male" and 1 or 0

        detalle = DetalleUsuario()
        detalle.fb_id = req.POST.get("fb_id")
        detalle.usuario = user
        detalle.sexo = sexo
        detalle.avatar = req.POST.get("img_url")
        detalle.save()

        #autentificacion del usuario
        log = authenticate(username = user.username)
        log_in(self.request, log)
        data['url'] = reverse("dashboard")

        return HttpResponse(json.dumps(data))

def actualizar_clave(req):
    email = req.POST.get("email")

    data = {
        "status" : "ok",
        "message" : "Solicitud realizada exitosamente, revise su bandeja de entrada para ver su nueva clave"
    }

    return HttpResponse(json.dumps(data),content_type = "application/json")


registro = RegistroView.as_view()
registro_fb = RegistroFbUserView.as_view()
envio = EnvioView.as_view()
recuperar_clave = TemplateView.as_view(template_name = "registro/recuperar_clave.html")
