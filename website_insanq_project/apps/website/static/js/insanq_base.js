$(document).ready(function(){

  var is_desktop = false;

  cekDesktop();

  $(window).resize(function() {
    cekDesktop();
    cekNavbar();
  });


  $('#navbar').addClass("no-transition");
  cekNavbar();
  $('#navbar').removeClass("no-transition");

  $(document).scroll(function() {
    cekNavbar();
  });
});

function cekNavbar() {
  var batas = 20;

  if (is_desktop) {
    if ($(document).scrollTop() > batas) {
      $('#navbar').addClass("small-navbar");
    } else {
      $('#navbar').removeClass("small-navbar");
    }
  }
}

function cekDesktop() {
  is_desktop = $('#desktopTest').is(":visible");

  if (is_desktop) {
    $(".navbar-white").toggleClass("navbar-white navbar-transparan");
  } else {
    $(".navbar-transparan").toggleClass("navbar-transparan navbar-white");
    $('#navbar').addClass("small-navbar");
  }
}
