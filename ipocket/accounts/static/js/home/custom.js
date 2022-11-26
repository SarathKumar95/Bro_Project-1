console.log("In custom.js ");

document.getElementById('img-container').addEventListener('mouseover', function(){
    imageZoom('product-detail')
})

function imageZoom(imgID){
    let img = document.getElementById(imgID)
    let lens = document.getElementById('lens')  

    lens.style.backgroundImage = `url( ${img.src})`

    let ratio = 1

    lens.style.backgroundSize = (img.width * ratio) + 'px ' + (img.height * ratio) + 'px';
    
    img.addEventListener("mousemove", moveLens)
    lens.addEventListener("mousemove", moveLens)
    img.addEventListener("touchmove", moveLens)
    function moveLens(){
        let pos =   getCursor();
        console.log('pos',pos)

        let posLeft = pos.x - (lens.offsetWidth / 2) 
        let posTop = pos.y - (lens.offsetHeight / 2)

        if (posLeft < 0){
             posLeft = 0   
        } 

        if (posTop < 0){
            posTop = 0
        }

         
        if (posLeft > img.width - lens.offsetWidth /3 ){
            posLeft = img.width - lens.offsetWidth /3 
       } 

       
         
       if (posTop > img.width - lens.offsetHeight /3 ){
        posLeft = img.width - lens.offsetHeight /3 
   } 


        lens.style.left = posLeft + 'px';
        lens.style.top = posTop + 'px';

        lens.style.backgroundPosition = "-" + (pos.x * ratio) + 'px -' + (pos.y * ratio) + 'px ' 

    }

    function getCursor(){

        let e = window.event
        let bounds = img.getBoundingClientRect()
        
        //console.log('e:',e)
        //console.log('bounds:',bounds)
        let x = e.pageX - bounds.left
        let y = e.pageY - bounds.top
        x = x  - window.pageXOffset;
        y = y - window.pageYOffset;
        return {'x': x, 'y' : y}
    }

}

imageZoom('product-detail')


$('.addtoCartBtn').click(function (){
    var product_id = document.getElementById('prod_id').value;
    var product_qty = document.getElementById('var-value').innerHTML;
    var token = $('input[name=csrfmiddlewaretoken]').val();
    console.log("Product id is ", product_id)
    console.log("Product qty is ", product_qty)
    
    $.ajax({
        method: "POST",
        url: "cart/add",
        data: {
            'product_id' : product_id,
            'product_qty' : product_qty,
            csrfmiddlewaretoken: token     
       },

        success: function (response) {
          console.log(response) 
          alertify.success(response.status) 
        }
    });

});


function deleteCartItem() {   
    var product_id = document.getElementById('cart-prod-id').value;
    console.log("Product id is",product_id);

    var token = $('input[name=csrfmiddlewaretoken]').val(); 
    
    $.ajax({
        method: "POST",
        url: "list/delete",
        data: {
            'product_id':product_id,
            csrfmiddlewaretoken: token
        },
        success: function (response) {
            alertify.success(response.status)            
        }
    });
}



