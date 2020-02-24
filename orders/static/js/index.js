window.addEventListener("load", () => {
  var product;
  document.querySelectorAll(".submit-order").forEach(element => {
    element.addEventListener("click", function() {
      $(".modal").modal("hide");
      let type = $(this).data().type;
      $.ajax({
        url: "/order/",
        type: "POST",
        data: JSON.stringify(typeOrder(type)),
        success: function(response) {
          console.log(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log(textStatus, errorThrown);
        }
      });
    });
  });

  document.querySelectorAll(".add-to-order").forEach(element => {
    element.addEventListener("click", function() {
      product = $(this).data().productName;
    });
  });

  document.querySelectorAll("#btn-confirm-order").forEach(element => {
    element.addEventListener("click", function() {
      $.ajax({
        url: "/confirm-order-final/",
        type: "POST",
        success: function(response) {
          console.log(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log(textStatus, errorThrown);
        }
      });
    });
  });

  document.querySelectorAll("#btn-cancel-order").forEach(element => {
    element.addEventListener("click", function() {
      $.ajax({
        url: "/cancel-order/",
        type: "POST",
        success: function(response) {
          console.log(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log(textStatus, errorThrown);
        }
      });
    });
  });

  document.querySelectorAll(".remove-item").forEach(element => {
    element.addEventListener("click", function() {
      let model = $(this).data().orderClass;
      let id = $(this).data().orderId;
      $.ajax({
        url: "/remove/",
        type: "POST",
        data: JSON.stringify({ model, id }),
        success: response => {
          console.log(this.parentNode.parentNode.remove());
        },
        error: (jqXHR, textStatus, errorThrown) => {}
      });
    });
  });

  function amountSelectedForm(selector) {
    let select = document.querySelector(selector);
    let size = select.options[select.selectedIndex].value;
    return size;
  }

  function typeOrder(dataType) {
    switch (dataType) {
      case "pizza":
        return {
          type: "pizza",
          product: product,
          size: amountSelectedForm("#modalProduct .modal-body #size"),
          amount: amountSelectedForm("#modalProduct .modal-body #amount"),
          topping: $("#modalProduct .modal-body #topping").val(),
          quantity: amountSelectedForm("#modalProduct .modal-body #quantity")
        };
        break;

      case "subs":
        return {
          type: "subs",
          product: product,
          size: amountSelectedForm("#modalSubs .modal-body #size"),
          quantity: amountSelectedForm("#modalSubs .modal-body #quantity")
        };
      case "pastas":
        return {
          type: "pastas",
          product: product,
          quantity: amountSelectedForm("#modalPastas .modal-body #quantity")
        };
      case "salads":
        return {
          type: "salads",
          product: product,
          quantity: amountSelectedForm("#modalSalads .modal-body #quantity")
        };
      case "dinnerPlatters":
        return {
          type: "dinnerPlatters",

          product: product,
          size: amountSelectedForm("#modalDinnerPlatters .modal-body #size"),
          quantity: amountSelectedForm(
            "#modalDinnerPlatters .modal-body #quantity"
          )
        };
        break;

      default:
    }
  }
});
