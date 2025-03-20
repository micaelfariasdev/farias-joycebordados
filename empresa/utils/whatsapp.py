import locale

# Define o locale para o Brasil (moeda em reais)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
def mensagem(pedido):
    stt = pedido.status[0]
    pg = pedido.pago
    qr_pix = pedido.gerar_qr_pix()
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
    if stt == '1':
        msg = f'''
Olá, *{pedido.cliente.nome}!* Seu pedido está em produção.
Código do pedido: \`\`\`#{pedido.codigo}\`\`\`
_• Produto: {pedido.produto}._
_• Detalhes do pedido: {pedido.observacao}._
_• Valor: {locale.currency(pedido.valor_total, grouping=True)}._

Em breve, você receberá mais informações sobre o status do seu pedido.
Caso precise de algo, estamos à disposição!
'''
        return msg
    if stt == '2':
        if pg:
            msg = f'''
Olá, *{pedido.cliente.nome}!* Seu pedido está pronto e disponível para retirada.
Código do pedido: \`\`\`#{pedido.codigo}\`\`\`
_• Produto: {pedido.produto}._
_• Detalhes do pedido: {pedido.observacao}._

Em breve, você receberá mais informações sobre o status do seu pedido.
Caso precise de algo, estamos à disposição!
'''     
        else:
            msg = f'''
Olá, *{pedido.cliente.nome}!* Seu pedido está pronto.
Código do pedido: \`\`\`#{pedido.codigo}\`\`\`
_• Produto: {pedido.produto}._
_• Detalhes do pedido: {pedido.observacao}._
_• Valor: {locale.currency(pedido.valor_total, grouping=True)}._

Lembrando que seu pedido está com pagamento pendente.
Abaixo segue codigo pix copia/cola para facilitar o processo:

{qr_pix}
'''     
        return msg


def enviar_msg(num, pedido):
    num_format = f"+55{num}"
    dados = {
        'numero': num_format,
        'mensagem': f'{mensagem(pedido)}',
        'codigo': pedido.codigo
    }
    return dados
