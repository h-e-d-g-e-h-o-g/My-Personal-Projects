const heartButton = document.getElementById('heartButton');
let isLiked = false;

heartButton.addEventListener('click', function () {
    if (isLiked) {
        heartButton.classList.remove('fa-heart-crack');
        heartButton.classList.add('fa-heart');
    } else {
        heartButton.classList.remove('fa-heart');
        heartButton.classList.add('fa-heart-crack');
    }
    
    isLiked = !isLiked;
});
