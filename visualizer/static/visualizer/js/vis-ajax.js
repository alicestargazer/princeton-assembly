// function gameOver() {
//   var probnum = $('#prob').attr('data-prob-id');
//   $.ajax({
//       type: "POST",
//       url: $('#prob').attr('data-done-ref'),
//       data: {
//           csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
//           probnum: probnum,
//       },
//       success: function(data) {
//           alert("Congratulations! You scored: "+data);
//       },
//       error: function(xhr, textStatus, errorThrown) {
//           alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
//       }
//   });
// }

$(document).ready(function() {

    $("#test").submit(function(event){
    event.preventDefault();
        $.ajax({
            async: true,
            type: "POST",
            url: $('#test').attr('data-done-ref'),
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                probnum: $('#test').attr('data-id'),
            },
            success: function(data) {
                $("#all").html(data);
            },
            error: function(xhr, textStatus, errorThrown) {
                alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
            }
        });
        return false;
    });

    $("#next").submit(function(event){
    event.preventDefault();
    var position = $("#myscroll").scrollTop();
    var reg_position = $("#regscroll").scrollTop();
        $.ajax({
            async: true,
            type: "POST",
            url: $('#next').attr('data-done-ref'),
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                probnum: $('#next').attr('data-id-a'),
                currline: $('#next').attr('data-id-b'),
            },
            success: function(data) {
              if (position >= 466) {
                  $("#allV").html(data);
                  $("#myscroll").scrollTop( position );
                  $("#regscroll").scrollTop( reg_position );
              } else {
                  $("#allV").html(data);
                  $("#myscroll").scrollTop( position );
                  $("#regscroll").scrollTop( reg_position );
              }
            },
            error: function(xhr, textStatus, errorThrown) {
                alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
            }
        });
        return false;
    });



});
