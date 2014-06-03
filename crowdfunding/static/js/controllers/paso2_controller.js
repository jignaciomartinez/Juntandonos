App.Controllers.Paso2 = function(){
    this.$titularCuenta = $("#titular_cuenta");
    this.$numCuenta = $("#num_cuenta");
    this.$rut = $("#rut");
    this.$banco = $("#banco");
    this.$tipoCuenta = $("#tipo_cuenta");
    this.$btnContinuar = $("#btn_continuar");
    this.$form = $("#f_paso_2");

    this.mensajeObligatorio = "campo obligatorio";
    this.mensajeRut = "Rut inválido";
    this.addEvents();
}

App.Controllers.Paso2.mixin({
    addEvents: function(){
        this.$btnContinuar.on("click", this.validarEnvio.bind(this));
    },

    validarEnvio: function(){
        var valido = true;

        $(".error_message").removeClass("error_message").empty();

        if(this.isEmpty(this.$titularCuenta)){
            valido = false;
            this.$titularCuenta.siblings("span").addClass("error_message").text(this.mensajeObligatorio);
        }

        if(this.isEmpty(this.$numCuenta)){
            valido = false;
            this.$numCuenta.siblings("span").addClass("error_message").text(this.mensajeObligatorio);
        }else if(isNaN(this.$numCuenta.val())){
            valido = false;
            this.$numCuenta.siblings("span").addClass("error_message").text("Deben ser sólo números");
        }

        if(this.isEmpty(this.$rut)){
            valido = false;
            this.$rut.siblings("span").addClass("error_message").text(this.mensajeObligatorio);
        }else if(!$.Rut.validar(this.$rut.val())){
            valido = false;
            this.$rut.siblings("span").addClass("error_message").text(this.mensajeRut);
        }

        if(this.$banco.val() === "0"){
            valido = false;
           this.$banco.siblings("span").addClass("error_message").text(this.mensajeObligatorio);
        }

        if(this.$tipoCuenta.val() === "0"){
            valido = false;
            this.$tipoCuenta.siblings("span").addClass("error_message").text(this.mensajeObligatorio);
        }

        if(!valido){
            return;
        }
        
        this.$form.trigger("submit");
    },

    isEmpty: function($el){
        return $el.val().trim() === "";
    }
});
