$(document).ready(function () {
  var is_desktop = false;

  cekDesktop();

  $(window).resize(function () {
    cekDesktop();
    cekNavbar();
  });

  $("#navbar").addClass("no-transition");
  cekNavbar();
  $("#navbar").removeClass("no-transition");

  $(document).scroll(function () {
    cekNavbar();
  });

  if ($(".datepicker").length) {
    $(".datepicker").datepicker({
      format: "d MM yyyy",
      maxViewMode: 1,
      todayBtn: "linked",
      language: "id",
      todayHighlight: true,
    });
  }

  //Smooth scrolling
  $('a[href*="#"]')
    // Remove links that don't actually link to anything
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function (event) {
      // On-page links
      if (
        location.pathname.replace(/^\//, "") ==
          this.pathname.replace(/^\//, "") &&
        location.hostname == this.hostname
      ) {
        // Figure out element to scroll to
        var target = $(this.hash);
        target = target.length
          ? target
          : $("[name=" + this.hash.slice(1) + "]");
        // Does a scroll target exist?
        if (target.length) {
          // Only prevent default if animation is actually gonna happen
          event.preventDefault();
          // Scroll tambahan jika navbar masih kondisi awal
          var tambahan = 0;
          if ($(window).scrollTop() == 0) {
            tambahan = 45;
          }
          $("html, body").animate(
            {
              scrollTop:
                target.offset().top -
                $("#navbar").outerHeight(false) +
                tambahan,
            },
            1000,
            function () {}
          );
        }
      }
    });
});

function cekNavbar() {
  var batas = 20;

  if (is_desktop) {
    if ($(document).scrollTop() > batas) {
      $("#navbar").addClass("small-navbar");
    } else {
      $("#navbar").removeClass("small-navbar");
    }
  }
}

function cekDesktop() {
  is_desktop = $("#desktopTest").is(":visible");

  if (is_desktop) {
    $(".navbar-white").toggleClass("navbar-white navbar-transparan");
  } else {
    $(".navbar-transparan").toggleClass("navbar-transparan navbar-white");
    $("#navbar").addClass("small-navbar");
  }
}
