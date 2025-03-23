
let chartInstance = null;  // Variável para armazenar a instância do gráfico
let chartInstance2 = null;  // Variável para armazenar a instância do gráfico
function ToRealBrasil(valor){
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

fetch('/profile/grafico/api/')
    .then(response => response.json())
    .then(data => {
        var init = document.getElementsByName('data_init')[0];
        var end = document.getElementsByName('data_end')[0];
        var compinit = document.getElementsByName('data_init')[1];
        var compend = document.getElementsByName('data_end')[1];

        var PedidosData = document.querySelector('.vendas > p')
        var fatData = document.querySelector('.fat > p')
        var ticketData = document.querySelector('.ticket > p')

        var CardPedido = document.querySelector('.vendas')
        var CardFat = document.querySelector('.fat')
        var CardTicket = document.querySelector('.ticket')

        var spaninit = document.querySelector('#init')
        var spanend = document.querySelector('#end')

        function filtrarDados() {
            const dataInicio = new Date(init.value);  
            const dataFim = new Date(end.value);    
            const compdataInicio = new Date(compinit.value);  
            const compdataFim = new Date(compend.value);     

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
            const ctx1 = document.getElementById('graficoPedidos').getContext('2d');
            chartInstance = new Chart(ctx1, {
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
    const divi = card.querySelector('.info')
    divc.addEventListener('mouseenter', infomouse)
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

fetch('/profile/pedidos/api/')
    .then(response => response.json())
    .then(data => {
        var init = document.getElementsByName('data_init')[0];
        var end = document.getElementsByName('data_end')[0];
        var compinit = document.getElementsByName('data_init')[1];
        var compend = document.getElementsByName('data_end')[1];
        const clientepedidos = document.getElementById('client-pedido-plus')
        const clientegasto = document.getElementById('client-pedido-valor')

        function filtrarPedidos(){

        const dataInicio = new Date(init.value);  
        const dataFim = new Date(end.value);  
        
        dataFim.setDate(dataFim.getDate() + 1);

        const dadosFiltrados = data.filter(item => {
            const partes = item.data.split('-');
            const dataPedido = new Date(partes[0], partes[1] - 1, partes[2]);
            return dataPedido >= dataInicio && dataPedido <= dataFim;
        });

        var lista = {}
        dadosFiltrados.forEach(item => {
            if(item.cliente){
                const nome = item.cliente.nome
                const valor = +item.valor_total
                if (lista[nome]) {
                    lista[nome]['quantidade'] += 1
                }else{
                    lista[nome] = {'quantidade':1}
                }
                if (lista[nome]['valorTOT']) {
                    lista[nome]['valorTOT'] += valor
                }else{
                    lista[nome]['valorTOT'] = valor
                }
                if (lista[nome]['MaiorPedido']) {
                    if(lista[nome]['MaiorPedido']['valor'] < item.valor_total)
                    lista[nome]['MaiorPedido'] = {'pedido': item.codigo, 'valor': +item.valor_total}
                }else{
                    lista[nome]['MaiorPedido'] = {'pedido': item.codigo, 'valor': +item.valor_total}
                }
            }
            return lista;
        });
        const ordenado = Object.entries(lista)
        .sort((a, b) => b[1]['quantidade'] - a[1]['quantidade']); 
        const maiorgasto = Object.entries(lista)
        .sort((a, b) => b[1]['valorTOT'] - a[1]['valorTOT']); 

        const labels = ordenado.map((person) => person[0]);
        const valores = ordenado.map((person) => person[1]['quantidade']);

        clientepedidos.innerHTML = `<strong>${ordenado[0][0]}:</strong> ${ordenado[0][1]['quantidade']} Pedidos 
                                    <span>Ao todo ${ordenado[0][0]} gastou ${ToRealBrasil(ordenado[0][1]['valorTOT'])}
                                     com os ${ordenado[0][1]['quantidade']} Pedidos`
        clientegasto.innerHTML = `<strong>${maiorgasto[0][0]}:</strong> ${ToRealBrasil(maiorgasto[0][1]['valorTOT'])}
                                   <span>O seu maior pedido foi "#${maiorgasto[0][1]['MaiorPedido']['pedido']}" valendo  ${ToRealBrasil(maiorgasto[0][1]['MaiorPedido']['valor'])}</span> `

        if (chartInstance2) {
            chartInstance2.destroy();
        }

        const ctx2 = document.getElementById('graficoclientes').getContext('2d');
            chartInstance2 = new Chart(ctx2, {
                type: 'bar',  
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
                            max: 2, 
                            ticks: {
                                color: 'black',
                            }
                        },
                        y: {
                            min: 0,  // Valor mínimo do eixo Y
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
        window.onload = filtrarPedidos()
        // Adiciona os event listeners
        init.addEventListener('change', filtrarPedidos);
        end.addEventListener('change', filtrarPedidos);
        compinit.addEventListener('change', filtrarPedidos);
        compend.addEventListener('change', filtrarPedidos);
    })