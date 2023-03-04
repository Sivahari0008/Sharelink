var img = document.getElementById('img');

var slides=["https://rukminim1.flixcart.com/image/416/416/xif0q/mobile/k/t/k/-original-imaghxemdgq5j8ww.jpeg?q=70",'https://rukminim1.flixcart.com/image/416/416/xif0q/mobile/y/l/p/-original-imaghxemc3wtcuhb.jpeg?q=70'];

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
