let modalId = $('#image-gallery');

$(document)
 .ready(function() {

  loadGallery(true, 'a.thumbnail');

  //This function disables buttons when needed
  function disableButtons(counter_max, counter_current) {
   $('#show-previous-image, #show-next-image')
    .show();
   if (counter_max === counter_current) {
    $('#show-next-image')
     .hide();
   } else if (counter_current === 1) {
    $('#show-previous-image')
     .hide();
   }
  }

  /**
   *
   * @param setIDs        Sets IDs when DOM is loaded. If using a PHP counter, set to false.
   * @param setClickAttr  Sets the attribute for the click handler.
   */

  function loadGallery(setIDs, setClickAttr) {
   let current_image,
    selector,
    counter = 0;

   $('#show-next-image, #show-previous-image')
    .click(function() {
     if ($(this)
      .attr('id') === 'show-previous-image') {
      current_image--;
     } else {
      current_image++;
     }

     selector = $('[data-image-id="' + current_image + '"]');
     updateGallery(selector);
    });

   function updateGallery(selector) {
    let $sel = selector;
    current_image = $sel.data('image-id');
    $('#image-gallery-title')
     .text($sel.data('title'));
    $('#image-gallery-image')
     .attr('src', $sel.data('image'));
    disableButtons(counter, $sel.data('image-id'));
   }

   if (setIDs == true) {
    $('[data-image-id]')
     .each(function() {
      counter++;
      $(this)
       .attr('data-image-id', counter);
     });
   }
   $(setClickAttr)
    .on('click', function() {
     updateGallery($(this));
    });
  }

  var fewSeconds = 5;
  $('#subbtn').click(function() {
   // Ajax request
   alert("I have read all the instructions carefully");
   var btn = $(this);
   /*btn.prop('disabled', true);
   setTimeout(function(){
       btn.prop('disabled', false);
   }, fewSeconds*1000);*/
  });

  var value = $('input[name=attendee_type]:checked').val().split('-');
  $("#id_ticket_price").val(value[1]);
  $('input[type=radio]').change(function() {
   var value = $('input[name=attendee_type]:checked').val().split('-');
   $("#id_ticket_price").val(value[1]);
  });


  $(".tshirt-size").hide();
  $(".tshirt-price").hide();

  $('#id_want_tshirt').change(function() {
   if ($('#id_want_tshirt').val() == 'Yes') {
    $(".tshirt-size").show();
    $(".tshirt-price").hide();
    $("#id_tshirt_price").val(350);
   } else {
    $(".tshirt-size").hide();
    $(".tshirt-price").hide();
    $(".tshirt-price").val();
   }
  });


  $(".tshirt-size").change(function() {
   if ($("#id_tshirt option:selected").val() == "None") {
    $("#id_tshirt_price").val(0);
   } else {

    $(".tshirt-price").show();
    $("#id_tshirt_price").val(350);

   }
  });




  $("#want_tshirt option").filter(function() {
   return $(this).val() == $("#tshirt_price").val();
  }).attr('selected', true);

  $("#want_tshirt").on("change", function() {

   $("#tshirt_price").val($(this).find("option:selected").attr("value"));
  });

 });

// build key actions
$(document)
 .keydown(function(e) {
  switch (e.which) {
   case 37: // left
    if ((modalId.data('bs.modal') || {})._isShown && $('#show-previous-image').is(":visible")) {
     $('#show-previous-image')
      .click();
    }
    break;

   case 39: // right
    if ((modalId.data('bs.modal') || {})._isShown && $('#show-next-image').is(":visible")) {
     $('#show-next-image')
      .click();
    }
    break;

   default:
    return; // exit this handler for other keys
  }
  e.preventDefault(); // prevent the default action (scroll / move caret)
 });
