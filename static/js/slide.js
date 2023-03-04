var img = document.getElementById('img');

var slides=["{{url_for('static' , filename = '/images/products/camera1.jpg')}}","{{url_for('static' , filename = '/images/products/camera2.jpg')}}"];

var Start=0;

function slider(){
    if(Start<slides.length){
        Start=Start+1;
    }
    else{
        Start=1;
    }
    console.log(img);
    img.innerHTML = "<img src="+slides[Start-1]+">";
   
}
setInterval(slider,2000);
