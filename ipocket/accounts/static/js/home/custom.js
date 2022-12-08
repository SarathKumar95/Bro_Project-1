

$('.addtoCartBtn').click(function (){
    //console.log("Here in add!");
    var product_id = document.getElementById('prod_id').value;
    var product_qty = document.getElementById('var-value').innerHTML;
    var token = $('input[name=csrfmiddlewaretoken]').val();
    console.log("Product id is ", product_id)
    console.log("Product qty is ", product_qty)
    
    let navCount = Number($('#navcartCount').text()) 
    
    console.log("Cart in nav count is", navCount)

    $.ajax({
        method: "POST",
        url: "cart/add",
        data: {
            'product_id' : product_id,
            'product_qty' : product_qty,
            csrfmiddlewaretoken: token     
       },

        success: function (response) {
          console.log("its added!")  
          alertify.success(response.status)
          $('#navcartCount').text(navCount + 1)      
        }
    });

});


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




