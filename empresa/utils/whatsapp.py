
def mensagem(pedido):
    stt = pedido.status[0]
    if stt == '0':
        msg = f'''
Olá, *{pedido.cliente.nome}!* Seu pedido foi confirmado.
Código do pedido: \`\`\`#{pedido.codigo}\`\`\`
_• Produto: {pedido.produto}._
_• Detalhes do pedido: {pedido.observacao}._

Em breve, você receberá mais informações sobre o status do seu pedido.
Caso precise de algo, estamos à disposição!
'''
        return msg

def enviar_msg(num, pedido):
    num_format = f"+55{num}"
    dados = {
        'numero': num_format,
        'mensagem': f'{mensagem(pedido)}',
    }
    return dados


