# -*- coding: utf8 -*-
import os, json

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.contrib.auth.models import User
from django.views.generic import ListView, TemplateView, View
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.core.urlresolvers import reverse

from .models import Proyecto, DetalleUsuario, Categoria

def get_js_template(req):
    my_path = os.path.dirname(__file__) + req.path
    my_path = my_path.replace("\\","/").rstrip("/") + ".html"

    js_template = open(my_path,"rb").read()

    return HttpResponse(js_template)


class IngresoView(View):
    def get(self, req):
        if req.user.is_authenticated():
            return redirect("dashboard")

        return render_to_response("ingreso/index.html",context_instance=RequestContext(req))


class LoginView(View):
    def post(self, req):
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        data = { "status" : "ok", "message" : "" }

        try:
            usuario_db = User.objects.get(username=username)
            user = authenticate(username=usuario_db.username, password=password)

            if user is None:
                data["status"] = "fail"
                data["message"] = "El usuario y/o contraseña son inválidos"
            else:
                log_in(self.request, user)
                req.session["is_logged_by_facebook"] = False
                data["url"] = reverse("dashboard")

        except User.DoesNotExist:
            data["status"] = "fail"
            data["message"] = "El usuario y/o contraseña son inválidos"

        return HttpResponse(json.dumps(data))


class FBLoginView(View):
    def get(self,request):
        self.client.login(self.user, backend="facebook")
        self.request.session["is_logged_by_facebook"] = True

        return redirect(reverse("dashboard"))


class LogoutView(View):
    def get(self, req):
        log_out(req)
        return redirect(reverse("index"))


class ProyectosList(ListView):
    model = Proyecto
    template_name = "index.html"

    def get_context_data(self,**kwargs):
        context = super(ProyectosList, self).get_context_data(**kwargs)
        context["proyectos"] = self.model.objects.all().order_by("-id")
        context["categorias"] = Categoria.objects.all().order_by("id")

        return context


class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self,**kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class MisProyectosList(ListView):
    model = Proyecto
    template_name = "dashboard/mis_proyectos.html"

    def get_comtext_data(self, **kwargs):
        context = super(MisProyectos, self).get_context_data(**kwargs)
        tmp = self.model.objects.filter()

class ProyectosFilterView(View):
    def get(self, req, categoria_id):
        data = []
        if categoria_id == "0":
            categoria_id = None
        
        if categoria_id is None:
            proyectos = Proyecto.objects.all().order_by("-id")[0:6]
        else:
            proyectos = Proyecto.objects.filter(categoria_id=categoria_id).order_by("-id")[0:6]

        for proyecto in proyectos:
            data.append({
                "id" : proyecto.id,
                "imagenProyecto" : proyecto.imagenproyecto_set.all()[0].imagen.url,
                "avatarUsername" : proyecto.creador.username,
                "nombreCreador" : proyecto.get_nombre_creador(),
                "tipoProyecto" : proyecto.tipo_proyecto.nombre,
                "proyecto" : {
                    "titulo" : proyecto.titulo.upper(),
                    "descripcion" : proyecto.descripcion,
                    "montoActual" : proyecto.get_monto_actual(),
                    "porcentajeActual" : proyecto.get_porcentaje_actual(),
                    "diasRestantes" : proyecto.get_dias_restantes().days
                }
            })

        return HttpResponse(json.dumps({ "proyectos" : data }), content_type="application/json")

index = ProyectosList.as_view()
dashboard = DashboardView.as_view()
misproyectos = MisProyectosList.as_view()
login = LoginView.as_view()
fb_login = FBLoginView.as_view()
logout = LogoutView.as_view()
ingresar = IngresoView.as_view()
obtener_proyectos = ProyectosFilterView.as_view()
