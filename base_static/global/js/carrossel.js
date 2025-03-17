const swiper = new Swiper('.swiper', {
    // Optional parameters
    direction: 'horizontal',
    autoplay: {
        delay: 5000, // Tempo entre slides (em ms)
        disableOnInteraction: false, // Continua rodando mesmo após interação
    },
    loop: true,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  
    // And if we need scrollbar
    scrollbar: {
      el: '.swiper-scrollbar',
    },
    effect: 'slide',
  });