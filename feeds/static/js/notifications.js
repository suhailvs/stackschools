var setTimeoutDuration = 120000; // 2 minutes = 2 * 60 * 1000
$(function () {
  // $("#notifications").click(function () {
  //   if ($(".popover").is(":visible")) {
  //     $("#notifications").popover('hide');
  //   }
  //   else {
  //     $("#notifications").popover('show');
  //     $.ajax({
  //       url: '/notifications/last/',
  //       beforeSend: function () {
  //         $(".popover-body").html("<div style='text-align:center'><img src='/static/img/loading.gif'></div>");
  //         $("#notifications").removeClass("btn-secondary");
          
  //       },
  //       success: function (data) {
  //         $(".popover-body").html(data);
  //       }
  //     });
  //   }
  //   return false;
  // });


  $('#notifications').on('show.bs.dropdown', function () {
    $.ajax({
      url: '/notifications/last/',
      beforeSend: function () {
        $("#notifications_body").html(`
          <div class="dropdown-menu-header">
            <div style='text-align:center'><img src='/static/img/loading.gif'></div>
          </div>`);
        $("#notifications i").removeClass("text-info");
        $("#notifications .indicator").hide();
      },
      success: function (data) {
        $("#notifications_body").html(data);
      }
    });
  });

  function check_notifications() {
    $.ajax({
      url: '/notifications/check/',
      cache: false,
      success: function (data) {
        if (data != "0") {
          $("#notifications i").addClass("text-info");
          $("#notifications .indicator").show();
        }
        else {
          $("#notifications i").removeClass("text-info");
          $("#notifications .indicator").hide();
        }
      },
      complete: function () {
        window.setTimeout(check_notifications, setTimeoutDuration);
      }
    });
  };
  check_notifications();
});