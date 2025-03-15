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