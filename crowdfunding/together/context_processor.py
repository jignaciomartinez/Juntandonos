def is_logged_by_facebook(request):
    esta_logueado_por_facebook = request.session.get("is_logged_by_facebook")

    return {
        "logged_by_facebook" : True#esta_logueado_por_facebook
    }
