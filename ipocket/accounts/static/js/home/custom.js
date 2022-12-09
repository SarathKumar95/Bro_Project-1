

function changeQty(){
    var cart_id = document.getElementById('cart-prod-id').value;
    var cart_qty = document.getElementById('cart-prod-qty').value;
    // console.log("Product id", cart_id)
    // console.log("cart qty is",cart_qty)
  
    var token = $('input[name=csrfmiddlewaretoken]').val();
    console.log("Token: ",token)

    $.ajax({
        method:'POST',
        url: "list/update",
        data: {'cart_id':cart_id,
        'cart_qty':cart_qty,
        csrfmiddlewaretoken: token
    
        },
        success: function (response) {
            alertify.success(response.status)            
        }
    });
  }
  

function deleteCartItem(proId) {   
    
    let subTotal = $('#sub-total').text() 
    const qty = $('#cartprod-qty'+proId).val()
    const price = $('#cartprod-price'+proId).val()  
    let cartCount = $('#cartCount').text()
          
    console.log("Cart count is", cartCount);

    var token = $('input[name=csrfmiddlewaretoken]').val(); 
    
    $.ajax({
        method: "POST",
        url: "list/delete",
        data: {
            'product_id':proId,
            csrfmiddlewaretoken: token
        },
        success: function (response) {
            alertify.success(response.status)
            $('#single-item'+proId).remove()
            $('#sub-total').text((subTotal) - (price * qty))  
            // $('#cartCount').val()    
            // $('#sub-total').text()
            // location.reload()        
            $('#cartCount').text(cartCount - 1) 
            
            console.log("Cart count is", cartCount);
            
        }
    });
}


  

