$(function () {
  function addNotification(type, message) {
    var cls = type === null ? "alert" : "alert alert-" + type;
    var dismiss = $("<button>").attr("data-dismiss", "alert").addClass("close").html("&times;");
    var notif = $("<div>").addClass(cls).html(message).prepend(dismiss);
    $("#messages").append(notif);
  }
  function clearNotifications() {
    $("#messages").children().alert("close");
  }
  $('.counterField textarea').maxlength(
    {max: $('#id_max_length').val(),
     truncate: false,
     onFull: function(overflowing){
       if (!overflowing) {
         clearNotifications();
         // enable the submit button
         $(':button').removeAttr('disabled');
       } else {
         clearNotifications();
         addNotification("error", "Message too long.");
         // disable the submit button
         $(':button').attr('disabled', 'disabled');
       }
     }
    });
  $('#id_max_length').change(function(event){
    $('.counterField textarea').maxlength('option', 'max', $('#id_max_length').val());
  });
});
