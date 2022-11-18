var updateBtns = document.getElementsByClassName('update-cart'); 

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function (){
        console.log("In func")
        var productId = this.dataset.product
        var action = this.dataset.action
        addCartToUser(productId,action)
    })

}

function addCartToUser(productId,action){ 

    var url = 'cart/add' 

    fetch(url,{
        method:'POST',  
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then ((data) => {
        console.log('data:',data)
    })
}


function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getToken('csrftoken');
