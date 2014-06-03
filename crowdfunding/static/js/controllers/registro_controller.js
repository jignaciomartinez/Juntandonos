App.Controllers.Registro = function(){
    this.$nombreUsuario = $("#nombre_usuario");
    this.$email = $("#email");
    this.$region = $("#region");
    this.$comuna = $("#comuna");
    this.$password = $("#password");
    this.$repeat = $("#repeat");
    this.$dia = $("#dia");
    this.$mes = $("#mes");
    this.$anio = $("#anio");

    this.addEventos();
};

App.Controllers.Registro.mixin({
    addEventos: function(){
        $("#region").on("change", this.redibujarComunas);
        $("#f_registro").on("submit", this.validarEnvio());
    },

    validarEnvio: function(){
        var _this = this;

        return function(evt){
            evt.preventDefault();
            $(".error_message").removeClass("error_message").text("");

            var valido, $span, me, json;

            me = this;
            valido = _this.validacionCampo(_this.$nombreUsuario, "nombre_usuario");
            valido = valido && _this.validacionCampo(_this.$email, "email");
            valido = valido && _this.validacionCampo(_this.$password, "contraseña");
            valido = valido && _this.validacionCampo(_this.$repeat,"repetir contraseña");

            if(!/^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$/.test(_this.$email.val())){
                valido = false;
                _this.$email.parent().find("span").addClass("error_message").text("El email es inválido");
            }

            if(_this.$password.val() !== _this.$repeat.val()){
                valido = false;
                _this.$password.parent().find("span").addClass("error_message").text("Las contraseñas deben ser iguales");
                _this.$repeat.parent().find("span").addClass("error_message").text("Las contraseñas deben ser iguales");
            }else if(_this.$password.val().length < 6 || _this.$password.val().length > 50){
                valido = false;
                _this.$password.parent().find("span").addClass("error_message").text("La contraseña debe tener entre 6 y 50 caracteres");
            }

            if(!$("input[type=radio]:checked").length){
                valido = false;
                $("input[type=radio]:first").parent().find("span").addClass("error_message").text("Debe indicar si es hombre o mujer");
            }

            if(!_this.$dia.val() || !_this.$mes.val() || !_this.$anio.val()){
                valido = false;
                _this.$dia.parent().find("span").addClass("error_message").text("Debe seleccionar una fecha válida");
            }else if(!_this.isFechaValida(_this.$dia.val(), _this.$mes.val(), _this.$anio.val())){
                valido = false;
                _this.$dia.parent().find("span").addClass("error_message").text("Debe seleccionar una fecha válida");
            }

            if(valido){
                json = {
                    username : _this.$nombreUsuario.val(),
                    email : _this.$email.val()
                };

                $.get("/registro/verificar_usuario/", json, function(res){
                    res = JSON.parse(res);
                    if(!res.existe){
                        me.submit();
                    }else{
                        valido = false;

                        if(res.mensajeUser){
                            _this.$nombreUsuario.parent().find("span").addClass("error_message").text(res.mensajeUser);
                        }

                        if(res.mensajeEmail){
                            _this.$email.parent().find("span").addClass("error_message").text(res.mensajeEmail);
                        }
                    }
                });
            }
        };
    },

    validacionCampo: function(campo, tipo){
        var valido = true, $span;

        if(campo.val().trim() === ""){
            valido = false;
            $span = campo.parent().find("span");
            $span.addClass("error_message").text("Debe agregar " + tipo);
        }else if(campo.val().trim().length > 140){
            valido = false;
            $span = campo.parent().find("span");
            $span.addClass("error_message").text("El " + tipo + " debe poseer menos de 140 caracteres");
        }

        return valido;
    },

    isFechaValida: function(dia, mes, anio){
        function getDiaMaximo(m){
            var days = 31;

            if(m == 4 || m == 6 || m == 9 || m == 11){
                days = 30;
            }else if(m == 2){
                days = ((anio % 4 == 0) && (!(anio % 100 === 0) || anio % 400 === 0 )) ? 29 : 28;
            }

            return days;
        }

        return  parseInt(dia, 10) <= getDiaMaximo(mes);
    }
});
