import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Token de conexão do bot (substitua pelo seu)
CHAVE_API = "8104013049:AAGN2vM_lzko5M62drNHAVeoSn0__V1hcwY"

# Instancia o bot
bot = telebot.TeleBot(CHAVE_API)

# Função para criar o menu principal
def criar_menu():
    menu = InlineKeyboardMarkup(row_width=2)
    botoes = [
        InlineKeyboardButton("1️⃣ Planos e Preços", callback_data="planos"),
        InlineKeyboardButton("2️⃣ Como Funcionamos", callback_data="como_funcionamos"),
        InlineKeyboardButton("3️⃣ Horários das Aulas", callback_data="horarios"),
        InlineKeyboardButton("4️⃣ Benefícios do Jiu-Jitsu", callback_data="beneficios"),
        InlineKeyboardButton("5️⃣ Fale Conosco", callback_data="fale_conosco"),
    ]
    menu.add(*botoes)
    return menu

# Envia o menu inicial
@bot.message_handler(commands=["start", "menu"])
def enviar_menu(mensagem):
    texto = (
        "👋 *Bem-vindo à Gracie Barra!*\n\n"
        "📋 Escolha uma das opções abaixo para saber mais:"
    )
    bot.send_message(mensagem.chat.id, texto, parse_mode="Markdown", reply_markup=criar_menu())

# Função para enviar respostas sem imagens
def enviar_resposta(chat_id, titulo, descricao):
    bot.send_message(
        chat_id,
        f"📌 *{titulo}*\n\n{descricao}",
        parse_mode="Markdown",
    )

# Callback para lidar com os botões interativos
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
    }

    resposta = respostas.get(call.data)
    if resposta:
        enviar_resposta(
            call.message.chat.id,
            resposta["titulo"],
            resposta["descricao"],
        )
    else:
        bot.send_message(call.message.chat.id, "Opção inválida. Por favor, escolha novamente.")

# Inicializa o bot
if __name__ == "__main__":
    bot.polling()
