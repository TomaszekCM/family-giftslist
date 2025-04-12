import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import $ from "jquery";

// Test jQuery — tylko do sprawdzenia działania
$(document).ready(function () {
  console.log("jQuery działa!");
});


$(document).ready(function () {
  $("#show-alert").click(function () {
    $("#alert-box").removeClass("d-none").addClass("show");
  });
});