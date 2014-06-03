import re

from datetime import timedelta, date
from django.db import models
from django.contrib.auth.models import User

class TipoProyecto(models.Model):
    nombre = models.CharField(max_length=140)
    impuesto = models.IntegerField(null=True)

    def __unicode__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=140)

    def __unicode__(self):
        return self.nombre


class Proyecto(models.Model):
    titulo = models.CharField(max_length=250)
    descripcion = models.TextField()
    creador = models.ForeignKey(User, related_name="creador")
    contribuyentes = models.ManyToManyField(User, related_name="contribuyentes", blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_modificacion = models.DateField(auto_now=True, auto_now_add=True)
    terminado = models.BooleanField(default=False)
    video_url = models.URLField(max_length=500)
    duracion = models.IntegerField()
    tipo_proyecto = models.ForeignKey(TipoProyecto)
    categoria = models.ForeignKey(Categoria)

    def __unicode__(self):
        return self.titulo + " " + str(self.terminado)

    def get_short_description(self):
        nombre_creador = self.creador.first_name + " " + self.creador.last_name
        return self.titulo + ", por " + nombre_creador

    def get_proyecto(self):
        nombre_creador = self.creador.username

        obj = {
            'id': self.id,
            'titulo': self.titulo,
            'creador': nombre_creador,
            'fecha_creacion': self.fecha_creacion,
            'duracion': self.duracion
        }

        return obj

    def get_nombre_creador(self):
        nombre_creador = self.creador.username
        return nombre_creador

    def get_dias_restantes(self):
        fecha_final = self.fecha_creacion + timedelta(days = self.duracion)
        dias_restantes = fecha_final - date.today()

        return dias_restantes

    def get_total_proyecto(self):
        impuesto = self.tipo_proyecto.impuesto
        total = 0

        for producto in self.producto_set.all():
            total += producto.precio

        total += total * (impuesto/100.0)

        return total

    def get_monto_actual(self):
        monto_actual = 0

        for comprobante_pago in self.comprobantepago_set.all():
            monto_actual += comprobante_pago.monto

        return monto_actual

    def get_porcentaje_actual(self):
        if self.get_monto_actual() == 0:
            porcentaje_actual = 0
        elif self.get_total_proyecto() == 0:
            porcentaje_actual = 0
        else :
            porcentaje_actual = ( self.get_monto_actual() * 100 )/self.get_total_proyecto()

        return round(porcentaje_actual,1)

    def get_colaboradores(self):
        colaboradores = 0
        id_array = []

        for comprobante_pago in self.comprobantepago_set.all():
            if comprobante_pago.usuario not in id_array:
                id_array.append(comprobante_pago.usuario)
                colaboradores += 1

        return colaboradores

    def obtener_lista_colaboradores(self):
        colaboradores = []

        for comprobante_pago in self.comprobantepago_set.all():
            colaboradores.append(comprobante_pago.usuario)

        return colaboradores

    def if_youtube(self):
        if re.search('youtube|youtu', self.video_url):
            return True
        else:
            return False

    def id_youtube_video(self):
        if re.search('youtube', self.video_url):
            _str = self.video_url.split("=")
            return _str[1]

        if re.search('youtu', self.video_url):
            _str = self.video_url.split(".be/")
            return _str[1]

class ImagenProyecto(models.Model):
    imagen = models.FileField(upload_to="proyectos/thumbnails")
    proyecto = models.ForeignKey(Proyecto,null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.proyecto is None:
            return " Sin proyecto " + str(self.fecha_creacion)

        return self.proyecto.titulo + " " + str(self.fecha_creacion)


class Moneda(models.Model):
    nombre = models.CharField(max_length=140)

    def __unicode__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=140, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    precio = models.IntegerField(default=0)
    moneda = models.ForeignKey(Moneda)
    es_recomendado = models.BooleanField(default=False)
    descripcion = models.TextField()
    proyecto = models.ForeignKey(Proyecto)

    def __unicode__(self):
        return self.nombre + " " + self.url

    def get_producto(self):
        obj = {
            'id': self.id,
            'nombre': self.nombre,
            'url': self.url,
            'precio': self.precio,
            'es_recomendado': self.es_recomendado
        }

        return obj


class ImagenProducto(models.Model):
    imagen = models.FileField(upload_to="productos/thumbnails")
    producto = models.ForeignKey(Producto,null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.imagen + " " + self.fecha_creacion


class Region(models.Model):
    nombre = models.CharField(max_length=140)

    def __unicode__(self):
        return self.nombre


class Comuna(models.Model):
    nombre = models.CharField(max_length=140)
    codigo = models.IntegerField()
    region = models.ForeignKey(Region)

    def __unicode__(self):
        return self.nombre + ", " + self.region.nombre


class TipoCuenta(models.Model):
    nombre = models.CharField(max_length=140)

    def __unicode__(self):
        return self.nombre


class Banco(models.Model):
    nombre = models.CharField(max_length=140)

    def __unicode__(self):
        return self.nombre


class CuentaBancaria(models.Model):
    numero_cuenta = models.IntegerField()
    tipo_cuenta = models.ForeignKey(TipoCuenta)
    banco = models.ForeignKey(Banco)

    def __unicode__(self):
        return self.numero_cuenta + " " + self.tipo_cuenta.nombre


class DetalleUsuario(models.Model):
    usuario = models.OneToOneField(User, related_name="usuario")
    fb_id = models.IntegerField(null=True, blank=True)
    rut = models.CharField(max_length=40, unique=True, null=True, blank=True)
    comuna = models.ForeignKey(Comuna, null=True, blank=True)
    sexo = models.NullBooleanField()
    cuenta_bancaria = models.ForeignKey(CuentaBancaria, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    avatar = models.URLField(max_length=1000,null=True)

    def __unicode__(self):
        return self.usuario.username


class TipoPago(models.Model):
    nombre = models.CharField(max_length=140)

    def __unicode__(self):
        return self.nombre


class ComprobantePago(models.Model):
    monto = models.IntegerField()
    tipo_pago = models.ForeignKey(TipoPago)
    proyecto = models.ForeignKey(Proyecto)
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.usuario.first_name


class Mensaje(models.Model):
    comprobante_pago = models.ForeignKey(ComprobantePago)
    mensaje = models.TextField()

    def __unicode__(self):
        return self.mensaje
