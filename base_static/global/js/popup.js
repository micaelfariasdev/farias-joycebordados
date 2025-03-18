var popup1;
var detail = document.querySelector('.popup-adm');


function admin_area(event) {
    event.preventDefault();


    popup1 = window.open(detail.href, "popup", "width=1440,height=650");


}


detail.addEventListener('click', admin_area);



