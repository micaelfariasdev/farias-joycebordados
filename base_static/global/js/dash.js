
  let chartInstance = null;  // Variável para armazenar a instância do gráfico

  fetch('/profile/pedidos/api/')
    .then(response => response.json())
    .then(data => {

      var init = document.getElementsByName('data_init')[0];
      var end = document.getElementsByName('data_end')[0];
      
      var PedidosData = document.querySelector('.vendas > p')
      var fatData = document.querySelector('.fat > p')
      var ticketData = document.querySelector('.ticket > p')
      var spaninit = document.querySelector('#init')
      var spanend = document.querySelector('#end')

      function filtrarDados() {

        const dataInicio = new Date(init.value);  // Pega o valor da data de início
        const dataFim = new Date(end.value);     // Pega o valor da data de fim
  
        // Ajusta a data final para incluir o último dia
        dataFim.setDate(dataFim.getDate() + 1);
  
        // Filtra os dados dentro do intervalo de datas
        const dadosFiltrados = data.filter(item => {
            const partes = item.data.split('-');  
            const dataPedido = new Date(partes[0], partes[1] - 1, partes[2]);  
            return dataPedido >= dataInicio && dataPedido <= dataFim;
        });
        spaninit.innerHTML = dataInicio
        spaninit.innerHTML = `${dataInicio.toLocaleString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })}`
        spanend.innerHTML = dataFim
        spanend.innerHTML = `${dataFim.toLocaleString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })}`
  
        // Se houver dados filtrados, mapeia para labels e valores
        const labels = dadosFiltrados.map(item => {
            const dataPedido = new Date(item.data);  
            return dataPedido.toISOString().split('T')[0]; 
        });
  
        const fat = dadosFiltrados.map(item => parseFloat(item.valor));
        const valores = dadosFiltrados.map(item => item.quantidade);
        const pedidosTOT = valores.reduce((acc, curr) => acc + curr, 0);
        const fatTOT = fat.reduce((acc, curr) => acc + curr, 0);
        PedidosData.innerHTML = pedidosTOT
        fatData.innerHTML = `${fatTOT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`;
        var tickmed = fatTOT / pedidosTOT
        ticketData.innerHTML = `${tickmed.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`;
        // Calcula o valor máximo para o eixo Y, com um valor de segurança de +10
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
                            color: 'black'  // Cor dos rótulos do eixo X
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

    })
    .catch(error => console.error('Erro ao carregar JSON:', error));

