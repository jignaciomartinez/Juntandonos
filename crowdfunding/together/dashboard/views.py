import math
import re
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.generic import TemplateView,ListView
from ..models import Proyecto, Producto, Categoria
from ..common import is_text_valid, is_email_valid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"
    model = Proyecto

    def get_context_data(self,**kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        mi_usuario = self.request.user

        context["mis_proyectos"] = self.model.objects.filter(creador_id = mi_usuario.id)


        if (self.request.user.email is None) or self.request.user.email == "":
            context["es_facebook"] =  True
        else:
            context["es_facebook"] = False

        return context


class MiPerfilView(TemplateView):
    template_name = "dashboard/mi_perfil.html"

    def get_context_data(self, **kwargs):
        context = super(MiPerfilView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class UpdateUserView(TemplateView):
    def post(self, req):
        template = "dashboard/actualizar_usuario.html"
        user_name = req.POST.get("nombre_usuario")
        fisrt_name = req.POST.get("first_name")
        last_name = req.POST.get("last_name")
        email = req.POST.get("email")
        old_password = req.POST.get("password_old")
        new_password = req.POST.get("password")

        data = {"status_form" : "ok", "status_pass" : "fail"}
        valido = True
        valido = valido and is_text_valid(user_name)
        valido = valido and is_email_valid(email)

        if valido:
            this_user = User.objects.get(username__exact=user_name)
            this_user.email = email
            this_user.first_name = fisrt_name
            this_user.last_name = last_name
            this_user.save()
            data['status_form'] = "ok"
        else:
            data['status_form'] = "fail"

        user = authenticate(username=user_name, password=old_password)

        if user is not None:
            this_user.set_password(new_password)
            this_user.save()
            data['status_pass'] = "ok"

        return render_to_response(template, data, context_instance='')


class VerProyectoView(TemplateView):
    template_name = 'dashboard/ver_proyecto.html'

    def get_context_data(self, **kwargs):
        context = super(VerProyectoView, self).get_context_data(**kwargs)
        id_proyecto = kwargs.get('id_proyecto')
        proyecto = Proyecto.objects.get(id = id_proyecto)

        context["proyecto"] = proyecto
        context["recaudado"] = proyecto.get_monto_actual
        context["total"] = math.trunc(proyecto.get_total_proyecto())
        context["dias_restantes"] = proyecto.get_dias_restantes
        context["numero_colaboradores"] = proyecto.get_colaboradores
        context["productos"] = Producto.objects.filter(proyecto = id_proyecto)
        self.request.session['id_this_proyect'] = id_proyecto

        return context


def comprobar_password(req):
    username = self.request.POST.get("nombre_usuario")
    password = self.request.POST.get("password_old")

    data = {"status" : "ok"}
    user = user = authenticate(username=username, password=password)

    if user is None:
        data["status"] = "fail"

    return HttpResponse(json.dumps(data))


dashboard = login_required(DashboardView.as_view())
mi_perfil = login_required(MiPerfilView.as_view())
ver_proyecto = VerProyectoView.as_view()
actualizar_usuario = UpdateUserView.as_view()
