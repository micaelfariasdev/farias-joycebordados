const mediaQuery = window.matchMedia("(max-width: 768px)");

function Atualizar(e) {
    var NovoPedido = document.querySelector(".form-ped > .button-style");
    var tabela = document.querySelector("#tabela2")
    var buttonmenu = document.querySelector("button.nav-button-hidden")
    var menu = document.querySelector("div.menu-profile")
    var navmenu = document.querySelector("div.menu-profile > nav")
    var blur = document.querySelector("div.blur.hidden.fucionstart")

    buttonmenu.classList.remove('hidden')
     var lista = [buttonmenu, menu, navmenu]

    if (NovoPedido) {
        NovoPedido.innerHTML = e.matches ? '<i class="fa-solid fa-plus"></i>' : "Novo Pedido";
    }
    if (tabela) {
        if (mediaQuery.matches){ 
        tabela.style.transform = 'scale(0.8) translate(-35px, -50px)';
    } else {
        tabela.style.transform = ''; // Resetando o estilo
    }}
    
    if (buttonmenu) {
        buttonmenu.addEventListener("click", () => {
            blur.classList.toggle("hidden"); // Alterna a visibilidade do blur
            lista.forEach(item => item.classList.toggle("show"));
        });
    }

    if (blur) {
        blur.addEventListener("click", () => {
            blur.classList.add("hidden"); // Sempre oculta o blur ao clicar
            lista.forEach(item => item.classList.remove("show")); // Garante que todos somem
        });
    }

    
}

mediaQuery.addEventListener("change", Atualizar);
Atualizar(mediaQuery); // Executa ao carregar
