#-*- coding: utf-8 -*-
import re, os
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives

def is_text_valid(texto, largo=140):
    if texto is None or texto.strip() == "":
        return False

    if len(texto) > largo:
        return False

    return True

def is_number_valid(texto):
    if texto is None or not(texto.isdigit()):
        return False

    if texto < 1 :
        return False

    return True

class Http500(Exception):
    pass

def is_email_valid(email):
    return re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',email.lower())

def is_rut_valid(rut):
    if '-' in rut :
        rut = rut.split('-')
    else:
        tmp = str(rut)
        rut = []
        rut.append(str(tmp)[0:-1])
        rut.append(str(tmp)[-1])

    if '.' in rut[0] :
        rut[0] = rut[0].replace('.','')
    
    if 'K' in rut[1] :
        rut[1] = str(rut[1]).upper()

    value = 11 - sum([ int(a)*int(b) for a,b in zip(str(rut[0]).zfill(8), '32765432')]) % 11
    dv = { 10 : 'K', 11 : '0'}.get(value, str(value))

    return str(dv) == str(rut[1])

def mail_sender_new_account(correo, clave, usuario):
    asunto = "Bienvenido a Juntándonos"

    plantilla = open(os.path.dirname(__file__) + "/email_templates/registro.html","rb").read()
    plantilla = plantilla.replace("{{ nombre }}", usuario)
    destinatarios = (correo, )
    msg = EmailMultiAlternatives(asunto, plantilla, "Equipo juntandonos", destinatarios)
    msg.content_subtype = "html"
    msg.send()

def mail_aporte(nombre, aportador, aportes, proyecto, correo):
    asunto = "Has recibido un aporte"
    
    plantilla = open(os.path.dirname(__file__) + "/email_templates/aporte.html","rb").read()
    plantilla = plantilla.replace("{{ nombre }}", nombre)
    plantilla = plantilla.replace("{{ aportador }}", aportador)
    plantilla = plantilla.replace("{{ aportes }}", aportes)
    plantilla = plantilla.replace("{{ proyecto }}", proyecto)
    destinatarios = (correo, )
    msg = EmailMultiAlternatives(asunto, plantilla, "Equipo juntandonos", destinatarios)
    msg.content_subtype = "html"
    msg.send()