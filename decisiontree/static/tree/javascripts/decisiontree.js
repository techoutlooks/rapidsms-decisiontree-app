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
     truncate: false
    });
  $('#id_max_length').change(function(event){
    $('.counterField textarea').maxlength('option', 'max', $('#id_max_length').val());
    // trigger a change event on the textarea
    $('.counterField textarea').change();
  });
  // On any change to the textarea, check the character count
  $('.counterField textarea').on('change keyup paste', function(event){
    submit = $('#submit-button')[0];
    if (this.value.length > $('#id_max_length').val()) {
      // update the notification, only if this is a change
      if (!submit.disabled) {
        clearNotifications();
        addNotification("error", "Message too long.");
        submit.disabled = true;
      }
    } else {
      // update the notification, only if this is a change
      if (submit.disabled) {
        clearNotifications();
        submit.disabled = false;
      }
    }
  });
});
