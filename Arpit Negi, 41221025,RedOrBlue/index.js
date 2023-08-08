var pills = $(".pill").length;

$('.pill')[0].addEventListener("click",function(){
    var file = window.open("source.html","_target");
    var enter = new Audio("MatrixSound.mp3");
    enter.play();
    setTimeout(function(){
        file.close();
        enter.pause();
    },5500);
});

$('.pill')[1].addEventListener("click",function(){
    $(".top-container").addClass('myClass'); 
    $("h1").addClass('myColor'); 
    $("h2").addClass('myColor'); 
    $(".top-cloud").addClass('top-cloud-motion');
    $(".bottom-cloud").addClass('bottom-cloud-motion');
    $("#1").addClass("firework firework1");
    $("#2").addClass("firework firework2");
    $("#3").addClass("firework firework3");
    var crackers = new Audio("crackers.mp3");
    crackers.play();
    var list =  $("div div div").length;
    for(var i=0;i<list;i++){
        $("div div div")[i].classList.add("explosion");
    }
    
    setTimeout(function(){
        $(".top-container").removeClass('myClass'); 
        $("h1").removeClass('myColor'); 
        $("h2").removeClass('myColor'); 
        $("#1").removeClass("firework firework1");
        $("#2").removeClass("firework firework2");
        $("#3").removeClass("firework firework3");
        for(var i=0;i<list;i++){
            $("div div div")[i].classList.remove("explosion");
        }
        crackers.pause();
    },6000)
});