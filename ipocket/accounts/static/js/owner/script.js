function showBlocked(){
    alert("User Blocked.")
}

function showUnblocked(){
    alert("User authorized.")
}


function imageZoom(imgID){

    //alert("Working!");//

    let img = document.getElementById(imgID)

    let lens = document.getElementById('lens')

    lens.style.backgroundImage = `url(${img.src} )`

    let ratio = 1

    lens.style.backgroundSize = (img.width * ratio) + 'px' + (img.height * ratio) + 'px' ;
    
    img.addEventListener("mousemove", moveLens)
    lens.addEventListener("mousemove", moveLens)
    img.addEventListener("touchmove", moveLens)

    function moveLens(){
        let pos = getCursor()
        //console.log('pos:', pos )

        let positionLeft = pos.x - (lens.offsetWidth / 2)
        let positionTop = pos.y - (lens.offsetHeight / 2)


        if(positionLeft < 0){
            positionLeft = 0
        }

        if(positionTop < 0){
            positionTop = 0
        }

        if(positionLeft > img.width - lens.offsetWidth / 3){
            positionLeft = img.width - lens.offsetWidth / 3
        }

        if(positionTop > img.height - lens.offsetHeight / 3){
            positionTop = img.height - lens.offsetHeight / 3
        }

        
        
        lens.style.left = positionLeft + 'px';
        lens.style.top = positionTop + 'px';
        
        
        lens.style.backgroundPosition = "-" + (pos.x * ratio) + 'px -' + (pos.y * ratio) + 'px' 
    
    }

    document.getElementById('img-container').addEventListener('mouseover',function(){
        imageZoom('featured')
    })

    function getCursor(){

        let e = window.event
        let bounds = img.getBoundingClientRect()
        
        //console.log("e:",e)
        //console.log("bounds:",bounds)

        let x = e.pageX - bounds.left
        let y = e.pageY - bounds.top
        
        x = x - window.pageXOffset;
        y = y - window.pageYOffset;
        
        return {'x':x, 'y':y}
    }

}

imageZoom('featured')