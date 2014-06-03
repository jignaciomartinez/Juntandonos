function TemplateLoader(engine, options){
    options = options || {};

    this.cache = {};
    this.prefix = options.prefix ? options.prefix + "_" : "";
    this.engine = engine;
    this.template = null;
    this.withCache = "withCache" in options ? options.withCache : true;
}

TemplateLoader.prototype = {
    constructor: TemplateLoader,

    load: function(templateName){
        var key, skey, template;

        key = this.prefix + "_memory_" + templateName;

        if(this.cache[key]){
            return this.cache[key];
        }

        skey = this.prefix + templateName;

        if(this.withCache && sessionStorage.getItem(skey)){
            this.cache[key] = sessionStorage.getItem(skey);
            return this.cache[key];
        }

        template = this._getAjaxTemplate(templateName);
        sessionStorage.setItem(skey, template);
        this.cache[key] = template;

        return this.cache[key];
    },

    _getAjaxTemplate: function(templateUrl){
        var xhr;

        xhr = new XMLHttpRequest();
        xhr.open("GET", templateUrl, false);
        xhr.onreadystatechange = this._callBack.bind(this, xhr, templateUrl);
        xhr.send(null);

        return this.template;
    },

    _callBack: function(xhr, templateUrl){
        if(xhr.readyState === 4){
            if(xhr.status !== 200){
                throw new URIError("The URL " + templateUrl + " was not found");
            }

            this.template = xhr.responseText.replace(/^[\s\t\n\r]+|[\s\t\n\r]+$/, '');
        }
    },

    compile: function(templateName){
        var template = this.load(templateName);
        this.cache[templateName] = this.engine.compile(template);

        return this.cache[templateName];
    },

    render: function(templateName, data){
        return this.compile(templateName)(data);
    }
};
