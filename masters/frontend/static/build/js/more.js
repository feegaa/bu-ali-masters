$(document).ready(function(){
    setTimeout(function() {
        $('#alert').fadeOut('fast');
    }, 2000); 

    $('.gender').click(function() {
        $(this).find('.btn').toggleClass('active');  
        if ($(this).find('.btn-primary').length>0) {
            $(this).find('.btn').toggleClass('btn-primary');
        }
        $(this).find('.btn').toggleClass('btn-default');
    });
})
