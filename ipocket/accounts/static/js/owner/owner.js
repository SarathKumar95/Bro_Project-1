function blockUser() {
  let confirmAction = confirm("Are you sure you want to block this user? ");
  if (confirmAction) {
    console.log("Inside confirm");
    let url = $("#blockbtn").attr("data-url");
    window.location = url;
  } else {
    console.log("Do nothing!");
  }
}

function unblockUser() {
  let confirmAction = confirm("Are you sure you want to unblock this user? ");
  if (confirmAction) {
    console.log("Inside confirm");
    let url = $("#unblockbtn").attr("data-url");
    window.location = url;
  } else {
    console.log("Do nothing!");
  }
}

function deleteProduct(passID) {
  let row = document.getElementById("productrow" + passID);

  console.log("Row is", row);

  console.log("Product ID", passID);
  let confirmAction = confirm(
    "Are you sure you want to delete this product ? "
  );

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  if (confirmAction) {
    $.ajax({
      method: "POST",
      url: "product/delete",
      data: {
        passID: passID,
        csrfmiddlewaretoken: getCookie("csrftoken"),
      },

      success: function (response) {
        alert("Product Deleted!");
        row.remove();
      },
    });
  }
}

function deleteCategory() {
  let confirmAction = confirm(
    "Are you sure you want to delete this category ? "
  );
  if (confirmAction) {
    console.log("Inside confirm");
    let url = $("#deletecategory-btn").attr("data-url");
    window.location = url;
  } else {
    console.log("Do nothing!");
  }
}

function deleteOrder() {
  let confirmAction = confirm("Are you sure you want to delete this order ? ");
  if (confirmAction) {
    console.log("Inside confirm");
    let url = $("#deleteOrder-btn").attr("data-url");
    window.location = url;
  } else {
    console.log("Do nothing!");
  }
}

function deleteOrderItem() {
  var product = document.getElementById("deleteOrderItem-btn").value;
  console.log("Product id  is", product);

  let confirmAction = confirm(
    "Are you sure you want to remove this product from the order  ? "
  );
  if (confirmAction) {
    let url = $("#deleteOrderItem-btn").attr("data-url");
    window.location = url;
  } else {
    console.log("Do nothing!");
  }
}

function cancelOrderItem() {
  var product = document.getElementById("cancelOrderItem-btn").value;
  console.log("Product id  is", product);

  let confirmAction = confirm(
    "Are you sure you want to cancel this product from the order  ? "
  );
  if (confirmAction) {
    let url = $("#cancelOrderItem-btn").attr("data-url");
    window.location = url;
  } else {
    console.log("Do nothing!");
  }
}

const imageBox = document.getElementById("image-box");
const imageForm = document.getElementById("image-form");
const confirmBtn = document.getElementById("confirm-btn");
