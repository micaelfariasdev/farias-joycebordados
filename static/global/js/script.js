let currentIndex = 0;
const slides = document.querySelectorAll('.carrossel img');
const dots = document.querySelectorAll('.dot');

function updateSlide(index) {
    document.querySelector('.carrossel').style.transform = `translateX(-${index * 100}%)`;
    dots.forEach(dot => dot.classList.remove('active'));
    dots[index].classList.add('active');
}

function changeSlide(index) {
    currentIndex = index;
    updateSlide(currentIndex);
}

function autoSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    updateSlide(currentIndex);
}

setInterval(autoSlide, 5000);


const show = document.querySelector('.blur-back');
const log = document.querySelector('.conteiner-buscar');

function showLog() {
    show.classList.add('show');
    log.classList.add('show');
}

function hiddenLog() {
    show.classList.remove('show');
    log.classList.remove('show');
}