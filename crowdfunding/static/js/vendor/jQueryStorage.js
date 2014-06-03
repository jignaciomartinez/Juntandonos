/**
 *  jQuery storage
 *  @author: Sebastian Real.
 *  @version: 0.2
 **/
;(function($){
    "use strict";

    /**
     *  Getting our storage method
     *
     **/
    function getStorageFactory(){
        var storageMethods = {
            local : localStorage,
            session : sessionStorage
        };

        if($.storage.options.method in storageMethods){
            return storageMethods[$.storage.options.method];
        }else{
            throw new TypeError("You have assigned an invalid choice as a storage method, please choose local or session");
        }
    }

    /**
     *  Out main method
     *  @param a :
     *      - if this is a object, it will persist all keys and values in our storage method
     *      - if this is a string, it returns storage value in key or null
     *      - if this is a null value, it returns all keys/values in an object
     *  @param b :
     *      - if this arg not is null it will set key/value in storage method
     *      - if this param is null it will delete value and key from storage
     **/
    $.storage = function(){
        var storage = getStorageFactory(),
            namespace = $.storage.options.namespace,
            args = arguments;

        if(namespace){
            namespace += "_";
        }

        switch(args.length){
            case 0:
                return (function(){
                    var json = {};

                    $.each(storage,function(key, value){
                        json[key] = JSON.parse(value);
                    });

                    return json;
                })();
            case 1:
                if(typeof args[0] === "string"){
                    return JSON.parse(storage.getItem(namespace + args[0]));
                }else if($.type(args[0]) === "object"){
                    $.each(args[0],function(key, value){
                        storage.setItem(namespace + key, JSON.stringify(value));
                    });
                }

                break;
            case 2:
                if(args[1] === null){
                    storage.removeItem(namespace + args[0]);
                }else{
                    storage.setItem(namespace + args[0], JSON.stringify(args[1]));
                }

                break;
            default:
                throw new TypeError("Los parametros de storage deben ser 0, 1 o 2 !!!!");
        }
    };

    /**
     *  Removes al storage data from object
     **/
    $.clearStorage = function(){
        getStorageFactory().clear();
    };

    /**
     *  Default storage options
     *
     **/
    $.storage.options = {
        method : "session",
        namespace : ""
    };
})(jQuery);