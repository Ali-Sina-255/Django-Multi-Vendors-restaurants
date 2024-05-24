$(document).ready(function () {
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");
    // data = {
    //   food_id: food_id,
    // };
    $.ajax({
      type: "GET",
      url: url,
      // data: data,
      success: function (response) {
        console.log(response);
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location == "/login";
          });
          if (response.status == "Failed") {
            swal(response.message, "", "error");
          }
          console.log("raise error message");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_counter"]);
          $("#qty-" + food_id).html(response.qty);
        }
      },
    });
  });
  // place the cart item quantity on load
  $(".item_qty").each(function () {
    var the_id = $(this).attr("id");
    var qty = $(this).attr("data-qty");
    console.log(qty);
    $("#" + the_id).html(qty);
  });

  // Decrease the card quantity
  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    // if not data the url contain the id
    // data = {
    //   food_id: food_id,
    // };
    $.ajax({
      type: "GET",
      url: url,

      success: function (response) {
        console.log(response);
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location == "/login";
          });
        } else if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_counter"]);
          $("#qty-" + food_id).html(response.qty);
        }
      },
    });
  });
  // place the cart item quantity on load
  // DELETE CART_ITEM
  $(".delete_cart").on("click", function (e) {
    e.preventDefault();

    cart_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_counter"]);
          swal(response.status, response.message, "success");
        }
      },
    });
  });
  // DELETE CART ITEM WITHOUT RELOADING PAGE
  function removeCartItem(cartItemQty, cart_id) {
    if (cartItemQty <= 0) {
      console.log("this is not working in this time ");
    }
  }
});
