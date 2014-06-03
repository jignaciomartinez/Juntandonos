from django import template
import re

register = template.Library()

@register.filter
def separador_miles(value, arg="."):
    nuevos_numeros = []
    numeros = list(str(value))[::-1]
    indice = 1

    for numero in numeros:
        nuevos_numeros.append(numero)

        if indice % 3 == 0:
            nuevos_numeros.append(arg)

        indice += 1

    nuevos_numeros = nuevos_numeros[::-1]
    return re.sub("^(\.|,)", "", "".join(nuevos_numeros))
