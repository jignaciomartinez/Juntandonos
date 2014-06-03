window.fbAsyncInit = function() {
    FB.init({
        appId : '1420749211490800',
        status : false, // check login status
        cookie : true, // enable cookies to allow the server to access the session
        xfbml : true  // parse XFBML
    });

    FB.Event.subscribe('auth.authResponseChange', function(response) {
        if (response.status === 'connected') {
            console.log("paso 1");
        } else if (response.status === 'not_authorized') {
            console.log("paso 2");
        }else{
            console.log("paso 3");
        }
    });
};

(function(d){
    var js,
        id = 'facebook-jssdk',
        ref = d.getElementsByTagName('script')[0];

    if (d.getElementById(id)) {
        return;
    }

    js = d.createElement('script');
    js.id = id;
    js.src = "//connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
})(document);

$("#btn_login_facebook").on("click",function(){
    FB.login(function(response){
        FB.api('/me', function(resp) {
            $.post("/fb_login/", {'fb_id' : resp.id}, function(data){
                if(data.status == "ok"){
                    window.location.href = data.url
                }
            });

            $.get("http://graph.facebook.com/" + resp.id, {fields:"picture",type:"large"}, function(data){
                var usr = {
                    fb_id : resp.id,
                    user_name : resp.username,
                    first_name : resp.first_name,
                    last_name : resp.last_name,
                    sexo : resp.gender,
                    img_url : data.picture.data.url
                };
                
                $.post("/registro/registro_fb/", usr, function(data){
                    window.location.href = data.url
                })

                console.log(usr);
            });

        });
    });
});

//Temporalmente.
function testAPI(){
    console.log('alive');
}
