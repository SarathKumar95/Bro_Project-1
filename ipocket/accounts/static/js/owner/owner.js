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