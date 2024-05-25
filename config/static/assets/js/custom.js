$(document).ready(function () {
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
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
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty-" + food_id).html(response.qty);
          // adding subtotal tex  grand_total

          ApplyCartAmount(
            response.cart_amount["subtotal"],
            response.cart_amount["total"],
            response.cart_amount["grand_total"]
          );
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
    cart_id = $(this).attr("id");

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
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty-" + food_id).html(response.qty);
          if (window.location.pathname == "/cart/") {
            removeCartItem(response.qty, cart_id);
            CheckEmptyCart();
          }
          ApplyCartAmount(
            response.cart_amount["subtotal"],
            response.cart_amount["total"],
            response.cart_amount["grand_total"]
          );
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
          removeCartItem(0, cart_id);
          CheckEmptyCart();
        }
        ApplyCartAmount(
          response.cart_amount["subtotal"],
          response.cart_amount["total"],
          response.cart_amount["grand_total"]
        );
      },
    });
  });
  // DELETE CART ITEM WITHOUT RELOADING PAGE
  function removeCartItem(cartItemQty, cart_id) {
    if (cartItemQty <= 0) {
      document.getElementById("cart-item-" + cart_id).remove();
      console.log("this is not working in this time ");
    }
  }

  // CHECK IF CART EMPTY
  function CheckEmptyCart() {
    var cart_counter = document.getElementById("cart_counter").innerHTML;
    if (cart_counter == 0) {
      document.getElementById("empty_cart").style.display = "block";
    }
  }

  // Cart Amount
  function ApplyCartAmount(subtotal, total, grand_total) {
    if (window.location.pathname == "/cart/") {
      $("#subtotal").html(subtotal);
      $("#total").html(total);
      $("#grand_total").html(grand_total);
    }
  }
});
