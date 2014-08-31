//------------------------------------------------------------------------
//								PRELOADER SCRIPT
//------------------------------------------------------------------------
$(window).load(function() { // makes sure the whole site is loaded

    "use strict";

    $('#preloader').delay(400).fadeOut('slow'); // will fade out the white DIV that covers the website.
    $('.clock').fadeOut(); // will first fade out the loading animation

    new WOW().init();

    $.stellar();

})




$(document).ready(function() {

    "use strict";

    //------------------------------------------------------------------------
    //						TESTIMONIALS SLIDER SETTINGS
    //------------------------------------------------------------------------
    var owl = $("#testimonials-slider");
    owl.owlCarousel({
        items: 5,
        itemsDesktop: [1400, 4],
        itemsDesktopSmall: [1200, 3],
        itemsTablet: [900, 2],
        itemsMobile: [600, 1],
        autoPlay: 4000,
        stopOnHover: true
    });




    //------------------------------------------------------------------------
    //						INTRO SUPERSLIDER SETTINGS
    //------------------------------------------------------------------------
    $("#slides").superslides({
        play: 8000,
        animation: "fade",
        pagination: false,
        inherit_height_from: "#intro"
    });




    //------------------------------------------------------------------------
    //					SUBSCRIBE FORM VALIDATION'S SETTINGS
    //------------------------------------------------------------------------          
    $('#subscribe_form').validate({
        onfocusout: false,
        onkeyup: false,
        rules: {
            email: {
                required: true,
                email: true
            }
        },
        errorPlacement: function(error, element) {
            error.appendTo(element.closest("form"));
        },
        messages: {
            email: {
                required: "We need your email address to contact you",
                email: "Please, enter a valid email"
            }
        },

        highlight: function(element) {
            $(element)
        },

        success: function(element) {
            element
                .text('').addClass('valid')
        }
    });




    //------------------------------------------------------------------------------------
    //						SUBSCRIBE FORM MAILCHIMP INTEGRATIONS SCRIPT
    //------------------------------------------------------------------------------------		
    $('#subscribe_form').submit(function() {
        $('.error').hide();
        $('.error').fadeIn();
        // submit the form
        if ($(this).valid()) {
            $('#subscribe_submit').button('loading');
            var action = $(this).attr('action');
            ajaxPost('/subscribe/', {
                'email': $('#subscribe_email').val()
            }, function(data) {
                if (data.success == true) {
                    $('.error').html('Well done, you are subscribed');
                } else {
                    $('.error').html('Oops! Something went wrong!');
                }
                $('#subscribe_submit').button('reset');
            });
            // return false to prevent normal browser submit and page navigation 
        }
        return false;
    });




    //------------------------------------------------------------------------------------
    //						REGISTRATION FORM VALIDATION'S SETTINGS
    //------------------------------------------------------------------------------------		  
    $('#register_form').validate({
        onfocusout: false,
        onkeyup: false,
        rules: {
            name: "required",
            email: {
                required: true,
                email: true
            },
            username: "required",
            password: {
                required: true,
                minlength: 4
            },
            betakey: "required",
        },
        errorPlacement: function(error, element) {
            error.insertAfter(element);
        },
        messages: {
            name: "What's your name?",
            email: {
                required: "What's your email?",
                email: "Please, enter a valid email"
            },
            username: "What's your username?",
            password: {
                required: "What's your password?",
                minlength: jQuery.format("At least {0} characters")
            },
            betakey: {
                required: "Put in a betakey",
            },
        },

        highlight: function(element) {
            $(element)
                .text('').addClass('error')
        },

        success: function(element) {
            element
                .text('').addClass('valid')
        }
    });

});