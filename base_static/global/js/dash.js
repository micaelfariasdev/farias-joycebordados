
let chartInstance = null;  // Variável para armazenar a instância do gráfico

fetch('/profile/pedidos/api/')
    .then(response => response.json())
    .then(data => {

        var init = document.getElementsByName('data_init')[0];
        var end = document.getElementsByName('data_end')[0];
        var compinit = document.getElementsByName('data_init')[1];
        var compend = document.getElementsByName('data_end')[1];

        var PedidosData = document.querySelector('.vendas > p')
        var fatData = document.querySelector('.fat > p')
        var ticketData = document.querySelector('.ticket > p')

        var compPedidosData = document.querySelector('.vendas > span')
        var compfatData = document.querySelector('.fat > span')
        var compticketData = document.querySelector('.ticket > span')


        var CardPedido = document.querySelector('.vendas')
        var CardFat = document.querySelector('.fat')
        var CardTicket = document.querySelector('.ticket')

        var spaninit = document.querySelector('#init')
        var spanend = document.querySelector('#end')

        function filtrarDados() {

            const dataInicio = new Date(init.value);  // Pega o valor da data de início
            const dataFim = new Date(end.value);     // Pega o valor da data de fim
            const compdataInicio = new Date(compinit.value);  // Pega o valor da data de início
            const compdataFim = new Date(compend.value);     // Pega o valor da data de fim

            // Ajusta a data final para incluir o último dia
            dataFim.setDate(dataFim.getDate() + 1);
            compdataFim.setDate(compdataFim.getDate() + 1);

            // Filtra os dados dentro do intervalo de datas
            const dadosFiltrados = data.filter(item => {
                const partes = item.data.split('-');
                const dataPedido = new Date(partes[0], partes[1] - 1, partes[2]);
                return dataPedido >= dataInicio && dataPedido <= dataFim;
            });

            const dadosFiltradosCompre = data.filter(item => {
                const partes = item.data.split('-');
                const compdataPedido = new Date(partes[0], partes[1] - 1, partes[2]);
                return compdataPedido >= compdataInicio && compdataPedido <= compdataFim;
            });


            var inciodata = new Date(init.value)
            inciodata.setDate(dataInicio.getDate() + 1);
            spaninit.innerHTML = `${inciodata.toLocaleString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })}`
            spanend.innerHTML = `${dataFim.toLocaleString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })}`

            // Se houver dados filtrados, mapeia para labels e valores
            const labels = dadosFiltrados.map(item => {
                const dataPedido = new Date(item.data);
                return dataPedido.toISOString().split('T')[0];
            });

            const complabels = dadosFiltradosCompre.map(item => {
                const compdataPedido = new Date(item.data);
                return compdataPedido.toISOString().split('T')[0];
            });

            const fat = dadosFiltrados.map(item => parseFloat(item.valor));
            const valores = dadosFiltrados.map(item => item.quantidade);
            const pedidosTOT = valores.reduce((acc, curr) => acc + curr, 0);
            const fatTOT = fat.reduce((acc, curr) => acc + curr, 0);

            const compfat = dadosFiltradosCompre.map(item => parseFloat(item.valor));
            const compvalores = dadosFiltradosCompre.map(item => item.quantidade);
            const comppedidosTOT = compvalores.reduce((acc, curr) => acc + curr, 0);
            const compfatTOT = compfat.reduce((acc, curr) => acc + curr, 0);


            PedidosData.innerHTML = pedidosTOT
            fatData.innerHTML = `${fatTOT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`;
            var tickmed = fatTOT / pedidosTOT
            ticketData.innerHTML = `${tickmed.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`;





            var comptickmed = compfatTOT / comppedidosTOT

            style_comp(CardPedido, pedidosTOT, comppedidosTOT)
            style_comp(CardFat, fatTOT, compfatTOT, true)
            style_comp(CardTicket, tickmed, comptickmed, true)

            const maxY = valores.length > 0 ? Math.max(...valores) + 5 : 10;

            // Se já existe um gráfico, destrói-o
            if (chartInstance) {
                chartInstance.destroy();
            }

            // Cria o gráfico novamente
            const ctx = document.getElementById('graficoPedidos').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'line',  // Tipo de gráfico (linha)
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Quantidade de Pedidos',
                            data: valores,
                            borderColor: 'blue',
                            backgroundColor: 'rgb(194, 237, 141)',
                            borderWidth: 1,
                            yAxisID: 'y'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    devicePixelRatio: window.devicePixelRatio || 4,  // Melhora a renderização em telas de alta resolução
                    scales: {
                        x: {
                            ticks: {
                                color: 'black',
                            }
                        },
                        y: {
                            min: 0,  // Valor mínimo do eixo Y
                            max: maxY,  // Valor máximo do eixo Y
                            ticks: {
                                color: 'blue',
                                stepSize: 1  // Passo entre os ticks
                            },
                            position: 'left'  // Posição do eixo Y à esquerda
                        },
                    }
                }
            });
        }
        window.onload = filtrarDados()
        // Adiciona os event listeners
        init.addEventListener('change', filtrarDados);
        end.addEventListener('change', filtrarDados);
        compinit.addEventListener('change', filtrarDados);
        compend.addEventListener('change', filtrarDados);

    })
    .catch(error => console.error('Erro ao carregar JSON:', error));

function compare(valor, comparativo) {

    if (comparativo === 0) {
        return "N/A";
    }

    const dif = valor - comparativo;
    const resp = (dif / comparativo) * 100;
    return `${resp.toFixed(2)}%`;
}

function dif(valor, comparativo, real=false) {
    const dif = valor - comparativo
    if (real){
        return dif.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
    }
    return dif
}

function style_comp(card, valor, comparativo, real=false) {
    const divc = card.querySelector('.comparation')
    divc.addEventListener('mouseenter', infomouse)
    const divi = card.querySelector('.info')
    const comp = divc.querySelector('span')
    const info = divi.querySelector('span')
    const text = compare(valor, comparativo)
    if(real){
        var infotext = `Você teve ${dif(valor, comparativo, real)} em comparaçao com a data comparada`
    }else{
        var infotext = `Você teve ${dif(valor, comparativo)} em comparaçao com a data comparada`
    }
    if (text == 'N/A' || text == 'NaN%' ){
        comp.id = 'igual'
    }else if (text[0] == '-'){
        comp.id = 'baixa'
    }else{
        comp.id = 'cresce'
    }

    comp.innerHTML = text
    info.innerHTML = infotext   
}
var comp = document.querySelector(".comparation")

function infomouse() {
    const info = document.querySelectorAll('.info');
    
    if (info) {
        info.forEach(function(info) {
        document.addEventListener('mousemove', function(event) {
            // Pega a posição do mouse
            const mouseX = event.clientX;
            const mouseY = event.clientY;

            // Atualiza a posição da div
            info.style.left = mouseX - info.offsetWidth / 2 + 'px';
            info.style.bottom = window.innerHeight - mouseY + info.offsetHeight / 2 + 'px';
        })
    })
    } else {
        console.error('Elemento com a classe "info" não encontrado!');
    }
};
