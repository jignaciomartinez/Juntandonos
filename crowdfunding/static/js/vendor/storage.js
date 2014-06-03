function Storage(options){
    options = options || {};

    var defaults = {
        method : "local",
        namespace : ""
    };

    Object.keys(options).forEach(function(key, value){
        defaults[key] = value;
    });

    if(defaults.method === "local" || defaults.method === "session"){
        this.storage = window[defaults.method + "Storage"];
    }else{
        this.storage = localStorage;
    }

    this.namespace = defaults.namespace;
    this.to_s = Object.prototype.toString;
}

Storage.prototype.set = function(key, value){
    var _this = this;

    if(this.to_s.call(key) === "[object Object]"){
        Object.keys(key).forEach(function(key, val){
            _this.storage.setItem(_this.namespace + key, JSON.stringify(val));
        });
    }else if(key && typeof key === "string"){
        this.storage.setItem(this.namespace + key, JSON.stringify(value));
    }else{
        throw new TypeError("The key must be a string or a hash");
    }
};

Storage.prototype.get = function(key){
    var skey = this.namespace + key;

    if(skey in this.storage){
        return JSON.parse(this.storage.getItem(key));
    }else{
        return null;
    }
};

Storage.prototype.rm = function(key){

};

Storage.prototype.clear = function(){
    this.storage.clear();
};
