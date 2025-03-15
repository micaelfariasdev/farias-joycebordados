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

const showlog = document.querySelector('.back-log');
const showpix = document.querySelector('.back-pix');
const pix = document.querySelector('.conteiner-pix');
const log = document.querySelector('.conteiner-buscar');

function showLog() {
    showlog.classList.add('show');
    log.classList.add('show');
}

function hiddenLog() {
    showlog.classList.remove('show');
    log.classList.remove('show');
}


function showPix() {
    showpix.classList.add('show');
    pix.classList.add('show');
}

function hiddenPix() {
    showpix.classList.remove('show');
    pix.classList.remove('show');
}

showpix.addEventListener('click', (e) => {

    hiddenPix(),
        hiddenLog()
}
)
showlog.addEventListener('click', (e) => {

    hiddenPix(),
        hiddenLog()
}
)

function copiarTexto() {
    // Seleciona o conteúdo do textarea
    var codigo = document.getElementById("pix");

    // Seleciona o texto dentro do textarea
    codigo.select();
    codigo.setSelectionRange(0, 99999); // Para dispositivos móveis

    // Copia o texto para a área de transferência
    document.execCommand("copy");

    // Opcional: Alerta o usuário que o conteúdo foi copiado
    alert("Código copiado para a área de transferência!");
}