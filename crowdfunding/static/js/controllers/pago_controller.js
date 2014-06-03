App.Controllers.Pago = function(){
    this.form = $("#f_pago");
    this.nombre = $("#nombre");
    this.email = $("#email");
    this.monto = $("#monto");
    this.mensaje = $("#mensaje");
    this.tipoPagoCredito = $("#tipo_pago_credito");
    this.tipoPagoPaypal = $("#tipo_pago_paypal");
    this.mensajeObligatorio = "Debes completar el campo";
    this.mensajeEmailNoValido = "Formato de email inválido";
    this.mensajeNumeroErroneo = "Formato de número inválido";

    this.init();
};

App.Controllers.Pago.prototype = {
    constructor: App.Controllers.Pago,
    init: function(){
        this.form.on("submit", this.validarForm());
        console.log('some');
    },

    validarForm: function(){
        var _this = this;

        function isEmpty($el){
            return $el.val().trim() === "";
        }

        return function(evt){
            evt.preventDefault();
            var valido = true,
                regexEmail = /^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$/;

            $(".error_message").removeClass("error_message").empty();

            if(isEmpty(_this.nombre)){
                valido = false;
                _this.nombre.siblings("span").addClass("error_message").text(_this.mensajeObligatorio);
            }

            if(isEmpty(_this.email)){
                valido = false;
                _this.email.siblings("span").addClass("error_message").text(_this.mensajeObligatorio);
            }else if(!regexEmail.test(_this.email.val())){
                valido = false;
                _this.email.siblings("span").addClass("error_message").text(_this.mensajeEmailNoValido);
            }


            if(isEmpty(_this.monto)){
                valido = false;
                _this.monto.siblings("span").addClass("error_message").text(_this.mensajeObligatorio);
            }else if(isNaN(_this.monto.val())){
                valido = false;
                _this.monto.siblings("span").addClass("error_message").text(_this.mensajeNumeroErroneo);
            }

            if(isEmpty(_this.mensaje)){
                valido = false;
                _this.mensaje.siblings("span").addClass("error_message").text(_this.mensajeObligatorio);
            }

            if(!$("input[type=radio]:checked").length){
                valido = false;
                $("input[type=radio]").siblings("span").addClass("error_message").text(_this.mensajeObligatorio);
            }

            if(!valido){
                return;
            }
            _this.form.get(0).submit();
        };
    }
};
