$(document).ready(function () {
  var is_desktop = false;

  var parallax_faktor = 0.5;
  $(".parallax").css(
    "height",
    $(document).height() * (1 / parallax_faktor) + 500
  );

  cekDesktop();
  // geserParallax(parallax_faktor);

  $(window).resize(function () {
    cekDesktop();
    cekNavbar(parallax_faktor);
  });

  $("#navbar").addClass("no-transition");
  cekNavbar();
  $("#navbar").removeClass("no-transition");

  $(document).scroll(function () {
    cekNavbar();
    // geserParallax();
  });

  $("form").each(function () {
    $(this)
      .find("input")
      .keypress(function (e) {
        // Enter pressed?
        if (e.which == 10 || e.which == 13) {
          this.form.submit();
        }
      });
  });

  // $("#searchbox").keypress(function (event) {
  //   var keycode = event.keyCode ? event.keyCode : event.which;
  //   if (keycode == "13") {
  //     history.pushState("", document.title, window.location.pathname);
  //     window.location.href =
  //       window.location.href +
  //       "?s=" +
  //       encodeURIComponent($(this).val()) +
  //       "&p=1";
  //   }
  // });

  $(".replace-koma").each(function (i, obj) {
    var text = obj.innerHTML;
    console.log(obj);
    console.log(text.trim());
    obj.innerHTML = replaceLast(",", ".", text);
  });

  // if ($("input[type=date]").length) {
  //   $("input[type=date]").datepicker({
  //     format: "d MM yyyy",
  //     maxViewMode: 1,
  //     todayBtn: "linked",
  //     language: "id",
  //     todayHighlight: true,
  //   });
  // }

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

function geserParallax(parallax_faktor) {
  if (true) {
    console.log("wow");
    var scroll = $(document).scrollTop();
    var ypos = parallax_faktor * scroll;

    $(".parallax").css("transform", "translatey(" + ypos + "px)");
  }
}

function replaceLast(find, replace, string) {
  var lastIndex = string.lastIndexOf(find);

  if (lastIndex === -1) {
    return string;
  }

  var beginString = string.substring(0, lastIndex);
  var endString = string.substring(lastIndex + find.length);

  return beginString + replace + endString;
}
