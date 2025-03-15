const excluirButtons = document.querySelectorAll('#excluir');

excluirButtons.forEach(excluir => {
    excluir.addEventListener('click', (e) => {
        e.preventDefault();  // Impede a ação padrão (navegação ou envio de formulário)

        const confirmAction = confirm("Tem certeza que deseja excluir?");  // Exibe um prompt de confirmação

        if (confirmAction) {
            // Se o usuário confirmar, você pode prosseguir com a navegação ou ação
            window.location.href = excluir.href;  // Redireciona para a URL do link
        }
    });
});