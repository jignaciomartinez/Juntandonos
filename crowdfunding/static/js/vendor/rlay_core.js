(function(context){
"use strict";
    var paramTypes = [
        "Null", "Undefined", "Array",
        "Object", "Number", "Boolean",
        "RegExp", "Function", "Element",
        "NaN", "Infinity", "Date"
    ];

    function type(obj){
        var str = {}.toString.call(obj),
            argType = str.match(/\[object (\w*?)\]/)[1].toLowerCase();

        if(obj && (obj.nodeType === 1 || obj.nodeType === 9)){
            return "element";
        }

        if(argType === "number"){
            if(isNaN(obj)){
                return "nan";
            }else if(!isFinite(obj)){
                return "infinity";
            }
        }

        return argType;
    }

    for(var i = 0; i < paramTypes.length; i++){
        type["is" + paramTypes[i]] = (function(i){
            return function(obj){
                return type(obj) === paramTypes[i].toLowerCase();
            };
        })(i);
    }

    if(!type.isFunction(Object.is)){
        Object.is = function(v1, v2) {
            if (v1 === 0 && v2 === 0) {
                return 1 / v1 === 1 / v2;
            }

            if (v1 !== v1) {
                return v2 !== v2;
            }

            return v1 === v2;
        };
    }

    if(!type.isFunction(Object.create)){
        Object.create = function(o){
            var F = function(){};
            F.prototype = o;
            return new F();
        };
    }

    function extend(A, B){
        for(var attr in B){
            if(B.hasOwnProperty(attr) && type.isUndefined(A[attr])){
                A[attr] = B[attr];
            }
        }

        return A;
    }

    extend(Array.prototype,{
        forEach: function(callback, context){
            if(!type.isFunction(callback)){
                throw new TypeError(callback + " is not a function");
            }

            var i, l;

            for(i = 0, l = this.length; i < l; i++){
                if(i in this){
                    callback.call(context, this[i], i, this);
                }
            }
        },

        clear: function(){
            this.length = 0;
        },

        remove: function(index){
            return this.splice(index, 1)[0];
        },

        inArray: function(value){
            var i = 0,
                length = this.length;

            for(;i < length; i++){
                if(this[i] === value){
                    return true;
                }
            }

            return false;
        },

        indexOf: function(value){
            var index = -1,
                i = 0,
                length = this.length;

            for(; i < length; i++){
                if(this[i] === value){
                    index = i;
                    break;
                }
            }

            return index;
        },

        lastIndexOf: function(value){
            var index = -1,
                i = this.length;

            for(; i > 0; i--){
                if(this[i] === value){
                    index = i;
                    break;
                }
            }

            return index;
        },

        map: function(fn){
            var i = 0,
                length = this.length,
                arr = [];

            for(;i < length; i++){
                arr.push( fn(this[i]) );
            }

            return arr;
        },

        filter: function(fn){
            var i = 0,
                length = this.length,
                arr = [];

            for(;i < length; i++){
                if( fn(this[i]) ){
                    arr.push(this[i]);
                }
            }

            return arr;
        },

        last: function(){
            return this[ this.length - 1 ];
        },

        unique: function(){
            var arr = [];

            this.forEach(function(value){
                if(!arr.inArray(value)){
                    arr.push(value);
                }
            });

            return arr;
        }
    });

    extend(String.prototype,{
        format: function(){
            var regex = null,
                str = this,
                each = Array.prototype.forEach;

            each.call(arguments, function(value, i){
                regex = new RegExp("\\{" + i + "\\}","g");
                str = str.replace(regex, value);
            });

            return str;
        },

        trim: function(){
            return this.replace(/^\s+|\s+$/g,'');
        },

        trimLeft: function(){
            return this.replace(/^\s+/g,'');
        },

        trimRight: function(){
            return this.replace(/\s+$/g,'');
        },

        template: function(json){
            var text, keys, replaceFn;

            replaceFn = function(text, token, replace, filter){
                var filters = {
                    uppercase : String.prototype.toUpperCase,
                    lowercase : String.prototype.toLowerCase
                };

                if(filter in filters){
                    replace = filters[filter].call(replace);
                }

                text = text.replace(token, replace);
                return text;
            };

            text = this;
            keys = text.match(/\{\{\s*[0-9A-z\._\|]+\s*\}\}/g);

            keys.forEach(function(value){
                var matches, tmp, expression, filter;

                matches = /([0-9A-z\._]+)((?:\|)(\w+))?/.exec(value);
                expression = matches[1];
                filter = matches[3];

                expression = expression.split(".");
                tmp = json[expression.shift()];

                while(expression.length){
                    tmp = tmp[expression.shift()];
                }

                if(typeof tmp !== "function"){
                    text = replaceFn(text, value, tmp, filter);
                }
            });

            return text;
        },

        replaceAll: function(matchableText, replacement){
            return this.replace(new RegExp(matchableText,"g"), replacement);
        },

        toArray: function(){
            return this.split("");
        }
    });

    extend(Function.prototype,{
        bind: function(context){
            var args, fn;
            args = [].slice.call(arguments, 1);
            fn = this;

            function f(){
                return fn.apply(context, args);
            }

            f.prototype = context.prototype;
            return f;
        },

        mixin: function(klass, newProperties){
            var args, proto;

            args = [].slice.call(arguments);
            newProperties = args.pop();
            klass = args[0] || null;
            proto = klass && Object.create(klass.prototype) || {};

            for(var property in newProperties){
                if(!newProperties.hasOwnProperty(property)){
                    continue;
                }

                if(typeof proto[property] === "function"){
                    proto[property] = (function(oldFn, fn){
                        return function(){
                            this._super = oldFn;
                            var ret = fn.apply(this, arguments);
                            return ret;
                        };
                    })(proto[property], newProperties[property]);
                }else{
                    proto[property] = newProperties[property];
                }
            }

            proto.constructor = this;
            this.prototype = proto;
        }
    });

    context.type = type;
})(window || this);
