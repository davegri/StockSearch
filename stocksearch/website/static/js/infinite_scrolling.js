// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


(function (){
    $('#preloader').hide()
    var Gallery = {
        page: 1,
        init: function(){
            this.cacheDOM();
            this.bindEvents();
        },
        cacheDOM: function(){
            this.$image_ul = $('ul.photos');
            this.$form = $('#search-form');
            this.$more_button = $('.load-more');
        },
        bindEvents: function(){
            $(document).on('scroll', function(){
                if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
                    this.getImages();
                }
            }.bind(this));

            this.$more_button.on('click', function(){
                this.$more_button.remove()
                this.getImages();
            }.bind(this));

            $(document).ajaxStart(function(){
                $('#preloader').show()
            });   
             $(document).ajaxStop(function(){
                $('#preloader').hide()
            });   
        },
        incrementPage: function(){
            this.page +=1;
        },
        appendImages: function(html){
            this.$image_ul.append(html);
            this.$image_ul.after('<button class="main-button load-more">Load more results</button>')
        },
        getImages: function(){
            this.incrementPage();
            data = this.$form.serializeArray();
            data.push({'name':'page', 'value':this.page});
            $.ajax({
                url : "/images/",
                type : "POST",
                data : data, 
                success : function(html) {
                    console.log("success");
                    this.appendImages(html);
                    this.cacheDOM();                    
                    this.bindEvents();
                }.bind(this),

                error : function(xhr,errmsg,err) {
                    console.log("error");
                }.bind(this)
            });
        }

    };
    Gallery.init();
})()



