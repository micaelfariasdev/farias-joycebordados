const mediaQueryped = window.matchMedia("(max-width: 768px)");
fetch('/profile/pedidos/api/')
.then(response => response.json())
.then(data => {
    
    const list3 = data.reduce((acc, item) => {
        
        if (item.cliente && item.cliente.nome) {
                const clienteId = item.cliente.nome;  
                
                if (!acc[clienteId]) {
                    acc[clienteId] = {
                        pk: item.cliente.id,
                        nome: item.cliente.nome,
                        numero: item.cliente.numero || 'none',  
                        pedidos: 0
                    };
                }
                
                
                acc[clienteId].pedidos += 1;
            }
        
            return acc;
        }, {});
        
        
        // Convertendo o objeto de volta para um array, caso você precise de uma lista de objetos
        const clientesUnicos = Object.values(list3);
        
        var grid = new gridjs.Grid({
            columns: [
                "Nome",
                "Numero",
                "Pedidos",
                "Ação"
            ],
            data: clientesUnicos.map(cliente => [
                cliente.nome,
                formatarnum(cliente.numero),
                cliente.pedidos,
                gridjs.html(`<a class="button-style color-black sc-70" onclick="popup(${cliente.pk})"><i class="fa-solid fa-pen"></i></a> 
                    `)
                ]),
                search: true,
                sort: true,
                pagination: {
                    limit: 20
                }
            }).render(document.getElementById("tabela2"))
        })
            
    function popup(pk, event) {
    var url = `${window.location.origin}${window.location.pathname}`
    var pknum = pk
    popup2 = window.open(url + pknum, "popup2", "width=600,height=600");
    
    var intervalo = setInterval(function() {
        if (popup2.closed) {
            clearInterval(intervalo);
            window.location.reload();
        }
    }, 1000);

    popup2.onload = function () {
        var form = popup2.document.querySelector('form');
    
        if (!form) {
            console.error("Formulário não encontrado dentro do popup.");
            return;
        }
    
        form.addEventListener('submit', function (event) {
            event.preventDefault();
    
            Swal.fire({
                title: "Tem certeza?",
                text: "Deseja editar o cliente?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Sim",
                cancelButtonText: "Não"
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire({
                        title: "Cliente editado",
                        icon: "success",
                        showCancelButton: false,
                        confirmButtonText: "OK"
                    }).then(() => {
                        form.submit(); // Corrigido: Agora envia corretamente o formulário
                    });
                }
            });
        });

        var fecharpopup = popup2.document.querySelector("button.red")
        fecharpopup.addEventListener('click', function (event) {
            event.preventDefault();
            popup2.close()
        })
    };
    
} 


function formatarnum(valor) {
    let num = valor;
  
    if (num.length > 0) {
      if (num.length <= 2) {
        num = `(${num}`;
      } else if (num.length <= 6) {
        num = `(${num.slice(0, 2)}) ${num.slice(2)}`;
      } else {
        num = `(${num.slice(0, 2)}) ${num.slice(2, 3)} ${num.slice(3, 7)}-${num.slice(7, 11)}`;
      }
    }
    return num;
  }


var add = document.querySelector('.add-related');
var cancel = document.querySelector("body > main > div.pop-new-cliente > div > form > a > button");
var popcliente = document.querySelector('.pop-new-cliente');

add.addEventListener('click', function (event) {
    event.preventDefault();
    popcliente.style.top = '100px'
    //popcliente.classList.add('show')
});
cancel.addEventListener('click', function (event) {
    event.preventDefault();
    popcliente.style.top = '-500px'

});

var formcliente = document.querySelector(".formcliente");
    if (formcliente) {
        formcliente.addEventListener("submit", function (event) {
        event.preventDefault();
        Swal.fire({
          title: "Tem certeza?",
          text: "Deseja Criar um cliente novo?.",
          icon: "question",
          showCancelButton: true,
          confirmButtonText: "Sim",
          cancelButtonText: "Não",
        }).then((result) => {
          if (result.isConfirmed) {
            Swal.fire({
              title: "Cliente criado",
              icon: "success",
              showCancelButton: false,
              confirmButtonText: "ok",
            }).then((result) => {
              this.submit();
            });
          }
        });
      });
    }