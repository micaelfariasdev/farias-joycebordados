const header = document.querySelector('header');

function onScroll() {
  // Calculando a porcentagem da rolagem
  let scrollY = window.scrollY;

  // Ajustando a altura do cabeçalho com base na rolagem
  let newHeight = Math.max(100, 200 - scrollY); // Garantindo que a altura não fique menor que 100px

  // Aplicando a nova altura com estilo inline
  
  // Adicionando ou removendo a classe 'scrolled'
  header.style.height = `${newHeight}px`;
  if (scrollY > 80 ) {
      header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
}

window.addEventListener('scroll', onScroll);
