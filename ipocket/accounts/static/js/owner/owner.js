console.log("In owner.js");


function blockUser(){
    let confirmAction = confirm("Are you sure you want to block this user? ");
    if(confirmAction){
        console.log("Inside confirm");
        let url = $("#blockbtn").attr("data-url");
        window.location = url;
    }
    else{
        console.log("Do nothing!");
    }


}

function unblockUser(){
    let confirmAction = confirm("Are you sure you want to unblock this user? ");
    if(confirmAction){
        console.log("Inside confirm");
        let url = $("#unblockbtn").attr("data-url");
        window.location = url;
    }
    else{
        console.log("Do nothing!");
    }


}

function deleteProduct(){

    let confirmAction = confirm("Are you sure you want to delete this product? ");
    if(confirmAction){
        console.log("Inside confirm");
        let url = $("#deleteproduct-btn").attr("data-url");
        window.location = url;
    }
    else{
        console.log("Do nothing!");
    }

}


function deleteCategory(){

    let confirmAction = confirm("Are you sure you want to delete this category ? ");
    if(confirmAction){
        console.log("Inside confirm");
        let url = $("#deletecategory-btn").attr("data-url");
        window.location = url;
    }
    else{
        console.log("Do nothing!");
    }

}


function deleteOrder(){
    let confirmAction = confirm("Are you sure you want to delete this order ? ");
    if(confirmAction){
        console.log("Inside confirm");
        let url = $("#deleteOrder-btn").attr("data-url");
        window.location = url;
    }
    else{
        console.log("Do nothing!");
    }

}


function deleteOrderItem(){
    var product = document.getElementById('deleteOrderItem-btn').value 
    console.log("Product id  is", product);
    
    let confirmAction = confirm("Are you sure you want to remove this product from the order  ? ");
    if(confirmAction){
        let url = $("#deleteOrderItem-btn").attr("data-url");
        window.location = url;
    }
    else{
        console.log("Do nothing!");
    }

}

function cancelOrderItem(){
    var product = document.getElementById('cancelOrderItem-btn').value 
    console.log("Product id  is", product);
    
    let confirmAction = confirm("Are you sure you want to cancel this product from the order  ? ");
    if(confirmAction){
        let url = $("#cancelOrderItem-btn").attr("data-url");
        window.location = url;
    }
    else{
        console.log("Do nothing!");
    }

    }












const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirm-btn')
