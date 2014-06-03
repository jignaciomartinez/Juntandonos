App.Controllers.Categoria = function(urlConsulta){
    this.categorias = $("#sel_categoria");
    this.urlConsulta = urlConsulta.replace("/99/", "/");
    this.init();
};

App.Controllers.Categoria.prototype = {
    constructor: App.Controllers.Categoria,
    init: function(){
        this.categorias.on("change", this.cambiarCategorias());
    },

    cambiarCategorias: function(evt){
        var _this = this;

        return function(evt){
            var nuevaUrl = _this.urlConsulta + $(this).val() + "/";

            $.get(nuevaUrl, function(data){
                var html = templateLoader.render("/templates/ajax/proyecto_list", data);
                $("#proyectos").empty().html(html);
            });
        };
    }
}
