#-*- coding: utf-8 -*-
import math

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.generic import TemplateView,ListView,View
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User

from ..models import Proyecto, TipoProyecto, Producto, Moneda
from ..models import Categoria, CuentaBancaria, TipoCuenta
from ..models import Banco, DetalleUsuario, ImagenProyecto, ImagenProducto
from ..common import is_text_valid, Http500, is_rut_valid

class NuevoProyecto1View(TemplateView):
    def get(self, req, categoria_id):
        template = "nuevo_proyecto/nuevo_proyecto_paso_1.html"

        req.session["tipo_proyecto_id"] = 2
        req.session["categoria_id"] = categoria_id
        tipo_proyecto = TipoProyecto.objects.get(pk = 2)

        data = {
            "monedas" : Moneda.objects.all(),
            "cantidad_impuesto" : tipo_proyecto.impuesto
        }

        return render_to_response(template, data, context_instance=RequestContext(req))

class NuevoProyecto2View(TemplateView):
    template_name = "nuevo_proyecto/nuevo_proyecto_paso_2.html"

    def get_context_data(self, **kw):
        data = super(NuevoProyecto2View, self).get_context_data(**kw)
        data['bancos'] = Banco.objects.all()
        data['tipos_cuentas'] = TipoCuenta.objects.all()
        data["tipo_proyecto_id"] = self.request.session.get("tipo_proyecto_id")

        return data


class GuardarPasoUno(View):

    def post(self, request):
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        thumbnail = request.FILES.get("thumbnail")
        video = request.POST.get('video')
        categoria = self.request.session.get("categoria_id")
        duracion = request.POST.get('duracion')

        valido = True
        valido = valido and is_text_valid(titulo)
        valido = valido and is_text_valid(descripcion, 140)
        valido = valido and is_text_valid(video, 500)

        productos = self.obtener_productos()

        creador_id = self.request.user.id
        tipo_proyecto_id = self.request.session.get("tipo_proyecto_id")

        imagen_proyecto = ImagenProyecto()
        imagen_proyecto.imagen = thumbnail
        imagen_proyecto.save()

        proyecto_data = {
            "titulo": titulo,
            "descripcion": descripcion,
            "video": video,
            "categoria": categoria,
            "duracion": duracion,
            "creador_id":creador_id,
            "tipo_proyecto": tipo_proyecto_id,
            "productos": productos,
            "thumbnail" : imagen_proyecto.id
        }

        request.session['f_nuevo_proyecto'] = proyecto_data

        return redirect("nuevo_proyecto_paso2")

    def obtener_productos(self):
        productos = []
        valido = True
        i = 0

        while True:

            url_producto = self.request.POST.get("url_%d"%i)
            desc_producto = self.request.POST.get("descripcion_producto")
            tipo_moneda_producto = self.request.POST.get("tipo_moneda_%d"%i)
            precio = self.request.POST.get("valor_%d"%i)
            imagen_producto = self.request.FILES.get("imagen_producto_%d"%i)

            print

            img_producto = ImagenProducto()
            img_producto.imagen = imagen_producto
            img_producto.save()

            valido = valido and is_text_valid(desc_producto, 500)
            valido = valido and is_text_valid(precio)

            if not valido:
                break

            moneda = Moneda.objects.get(pk=1)
            prod = {
                "nombre": " ",
                "url": " ",
                "descripcion": desc_producto,
                "tipo_moneda_producto": moneda.id,
                "precio": precio,
                "imagen_producto_id" : img_producto.id
            }
            productos.append(prod)
            i += 1

        return productos

class GuardarPasoDos(View):

    @transaction.commit_on_success
    def post(self,req):
        valido = True
        creador_id = self.request.user.id

        titular_cuenta = req.POST.get('titular_cuenta')
        num_cuenta = req.POST.get('num_cuenta')
        banco = req.POST.get('banco')
        rut = req.POST.get('rut')
        tipo_cuenta = req.POST.get('tipo_cuenta')

        valido = valido and is_text_valid(titular_cuenta)
        valido = valido and is_text_valid(num_cuenta)
        valido = valido and is_text_valid(banco)
        valido = valido and is_text_valid(tipo_cuenta)

        data_cuenta = {
            "titular": titular_cuenta,
            "cuenta": num_cuenta,
            "banco": banco,
            "rut": rut,
            "tipo": tipo_cuenta,
            "creador": creador_id
        }

        self.__crear_cuenta(data_cuenta)
        id_proyecto = self.__crear_proyecto(req.session['f_nuevo_proyecto'])


        return redirect("nuevo_proyecto_paso3", id_proyecto = id_proyecto)

    def __crear_cuenta(self, data):
        try:
            cuenta = CuentaBancaria.objects.get(numero_cuenta = data['cuenta']\
                , banco = data['banco'], tipo_cuenta = data['tipo'])
        except CuentaBancaria.DoesNotExist as dne:
            banco = Banco.objects.get(pk=data['banco'])
            tipo_cuenta = TipoCuenta.objects.get(pk=data['tipo'])

            cuenta = CuentaBancaria()
            cuenta.numero_cuenta = data['cuenta']
            cuenta.tipo_cuenta = tipo_cuenta
            cuenta.banco = banco
            cuenta.save()

        try:
            detalle_usuario = DetalleUsuario.objects.get(usuario = data['creador'])
            detalle_usuario.rut = data['rut']
            detalle_usuario.cuenta_bancaria = cuenta
            detalle_usuario.save()

        except DetalleUsuario.DoesNotExist as dne:
            creador = User.objects.get(pk=data['creador'])

            detalle_usuario = DetalleUsuario()
            detalle_usuario.usuario = creador
            detalle_usuario.rut = data['rut']
            detalle_usuario.cuenta_bancaria = cuenta
            detalle_usuario.save()

    def __crear_proyecto(self, data):
        creador = User.objects.get(pk = data["creador_id"])
        tipo_proyecto = TipoProyecto.objects.get(pk = data["tipo_proyecto"])
        categoria = Categoria.objects.get(pk = data["categoria"])
        imagen_proyecto = ImagenProyecto.objects.get(pk = data["thumbnail"])

        proyecto = Proyecto()
        proyecto.titulo = data["titulo"]
        proyecto.descripcion = data["descripcion"]
        proyecto.imagen = imagen_proyecto
        proyecto.creador = creador
        proyecto.video_url = data["video"]
        proyecto.duracion = data["duracion"]
        proyecto.tipo_proyecto = tipo_proyecto
        proyecto.categoria = categoria
        proyecto.save()

        imagen_proyecto.proyecto = proyecto
        imagen_proyecto.save()

        self.__crear_producto(data['productos'], proyecto)

        return proyecto.id

    def __crear_producto(self, data, proyecto):
        print data
        for item in data:
            moneda = Moneda.objects.get(pk=item['tipo_moneda_producto'])
            producto = Producto()
            producto.nombre = item['nombre']
            producto.url = item['url']
            producto.precio = item['precio']
            producto.proyecto = proyecto
            producto.descripcion = item['descripcion']
            producto.moneda = moneda
            producto.save()

            imagen_producto = ImagenProducto.objects.get(pk=item["imagen_producto_id"])
            imagen_producto.producto = producto
            imagen_producto.save()


class NuevoProyecto3View(TemplateView):
    template_name = "nuevo_proyecto/nuevo_proyecto_paso_3.html"

    def get_context_data(self, **kwargs):
        context = super(NuevoProyecto3View, self).get_context_data(**kwargs)

        id_proyecto = kwargs["id_proyecto"]
        proyecto = Proyecto.objects.get(id = id_proyecto)

        context["proyecto"] = proyecto
        context["recaudado"] = 0
        context["total"] = math.trunc(proyecto.get_total_proyecto())
        context["dias_restantes"] = 0
        context["numero_colaboradores"] = 0
        context["productos"] = Producto.objects.filter(proyecto = id_proyecto)

        return context

terminos_condiciones = login_required(TemplateView.as_view(template_name="nuevo_proyecto/terminos_y_condiciones.html"))
tipo_proyecto = login_required(TemplateView.as_view(template_name="nuevo_proyecto/tipo_de_proyecto.html"))

nuevo_proyecto_paso1 = login_required(NuevoProyecto1View.as_view())
guardar_paso1 = login_required(GuardarPasoUno.as_view())
nuevo_proyecto_paso2 = login_required(NuevoProyecto2View.as_view())
guardar_paso2 = login_required(GuardarPasoDos.as_view())
nuevo_proyecto_paso3 = login_required(NuevoProyecto3View.as_view())
