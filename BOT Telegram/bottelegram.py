import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from PIL import Image, ImageDraw, ImageFont
import os

# Token de conexão do bot (substitua pelo seu)
CHAVE_API = "8104013049:AAGN2vM_lzko5M62drNHAVeoSn0__V1hcwY"

# Instancia o bot
bot = telebot.TeleBot(CHAVE_API)

# Função para criar o menu com imagem de fundo
def criar_imagem_menu(texto):
    # URL da imagem de fundo
    url_imagem = 'https://i.pinimg.com/736x/63/03/d9/6303d9cebd756db03250ed597a690d59.jpg'

    # Baixando a imagem
    response = requests.get(url_imagem)
    if response.status_code == 200:
        with open('imagem_fundo.jpg', 'wb') as f:
            f.write(response.content)

    # Carrega a imagem de fundo
    fundo = Image.open('imagem_fundo.jpg')
    fundo = fundo.resize((800, 600))  # Ajuste o tamanho conforme necessário

    # Cria um objeto ImageDraw
    draw = ImageDraw.Draw(fundo)

    # Define a fonte e o tamanho do texto
    try:
        fonte = ImageFont.truetype('arialbd.ttf', 40)  # Fonte bold; substitua pelo caminho correto se necessário
    except IOError:
        fonte = ImageFont.load_default()

    # Define a cor do texto (preto)
    cor_texto = (0, 0, 0)  # Preto

    # Adiciona texto à imagem
    draw.text((50, 50), texto, font=fonte, fill=cor_texto)

    # Salva a nova imagem
    fundo.save('menu_criado.jpg')

# Função para criar o menu principal
def criar_menu():
    menu = InlineKeyboardMarkup(row_width=2)
    botoes = [
        InlineKeyboardButton("1️⃣ Planos e Preços", callback_data="planos"),
        InlineKeyboardButton("2️⃣ Como Funcionamos", callback_data="como_funcionamos"),
        InlineKeyboardButton("3️⃣ Horários das Aulas", callback_data="horarios"),
        InlineKeyboardButton("4️⃣ Benefícios do Jiu-Jitsu", callback_data="beneficios"),
        InlineKeyboardButton("5️⃣ Fale Conosco", callback_data="fale_conosco"),
        InlineKeyboardButton("🔙 Voltar ao Menu Principal", callback_data="menu_principal")
    ]
    menu.add(*botoes)
    return menu

# Envia o menu inicial
@bot.message_handler(commands=["start", "menu"])
def enviar_menu(mensagem):
    # Cria a imagem com o texto do menu
    texto_menu = "👋 Bem-vindo à Gracie Barra!\nEscolha uma das opções abaixo:"
    criar_imagem_menu(texto_menu)

    # Envia a imagem criada
    with open('menu_criado.jpg', 'rb') as imagem:
        bot.send_photo(mensagem.chat.id, imagem, caption="Escolha uma opção:", parse_mode="Markdown", reply_markup=criar_menu())

# Função para enviar a resposta baseada na opção escolhida
def enviar_resposta(chat_id, titulo, descricao):
    bot.send_message(chat_id, f"✨ *{titulo}* ✨\n\n{descricao}", parse_mode="Markdown", reply_markup=criar_menu())

# Manipulador de callback para o menu
@bot.callback_query_handler(func=lambda call: True)
def callback_menu(call):
    respostas = {
        "planos": {
            "titulo": "Planos e Preços",
            "descricao": (
                "💎 *Plano Básico*: R$ 150/mês\n"
                "💪 *Plano Intermediário*: R$ 200/mês\n"
                "🥋 *Plano Premium*: R$ 300/mês\n\n"
                "📢 Escolha o plano ideal para você e comece hoje mesmo!"
            ),
        },
        "como_funcionamos": {
            "titulo": "Como Funcionamos",
            "descricao": (
                "✅ Aulas estruturadas com graduações por faixas\n"
                "✅ Professores certificados e experientes\n"
                "✅ Ambiente seguro para todas as idades\n\n"
                "🌟 Experimente a comunidade Gracie Barra!"
            ),
        },
        "horarios": {
            "titulo": "Horários das Aulas",
            "descricao": (
                "🕒 Segunda a Sexta:\n"
                "• Manhã: 7h às 9h\n"
                "• Tarde: 14h às 17h\n"
                "• Noite: 19h às 21h\n\n"
                "🕒 Sábados:\n"
                "• 9h às 12h (aulas especiais e workshops)\n\n"
                "📅 Venha treinar no horário que melhor se encaixa na sua rotina!"
            ),
        },
        "beneficios": {
            "titulo": "Benefícios do Jiu-Jitsu",
            "descricao": (
                "✅ Fortalecimento físico e mental\n"
                "✅ Redução do estresse\n"
                "✅ Disciplina e autocontrole\n"
                "✅ Defesa pessoal\n\n"
                "🎯 Junte-se à nossa equipe e transforme sua vida!"
            ),
        },
        "fale_conosco": {
            "titulo": "Fale Conosco",
            "descricao": (
                "📍 *Endereço*: Rua da Academia, 123, Cidade XYZ\n"
                "📱 *WhatsApp*: +55 11 99999-9999\n"
                "📧 *E-mail*: contato@graciebarra.com\n\n"
                "📞 Estamos aqui para ajudar você!"
            ),
        },
        "menu_principal": {
            "titulo": "Menu Principal",
            "descricao": "👋 Bem-vindo de volta ao Menu Principal!\nEscolha uma das opções abaixo:"
        },
    }

    resposta = respostas.get(call.data)
    if resposta:
        # Envia a nova resposta
        enviar_resposta(call.message.chat.id, resposta["titulo"], resposta["descricao"])
    else:
        bot.send_message(call.message.chat.id, "Opção inválida. Por favor, escolha novamente.")

# Inicializa o bot
if __name__ == "__main__":
    bot.polling()
