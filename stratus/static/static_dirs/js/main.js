
var main = function() {
    //Enable the dropdown menu on nouseenter and leave
    $('#menuhead').on('mouseenter', function() {
        $('#head2').addClass('hovered');
        $('#menu').show();
    });$("#head2").on('mouseleave', function() {
        $('#head2').removeClass('hovered');
        $('#menu').hide();
    });

    //create interactivity for plus button
    //submits form located off screen, triggering file picker
    $('#plus2').click(function() {
        $('#files').trigger('click');
    });

    //if a file is double clicked, send information to Django download port
    $('.file').dblclick(function () {
        $.post('/accounts/download/', {file_name: $(this).attr('id')});
    });
}

$(document).ready(main);