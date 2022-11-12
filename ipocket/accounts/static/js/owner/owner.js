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

function deleteBtn(){

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