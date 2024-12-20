import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from PIL import Image
import os

#conexão 
CHAVE_API = "8104013049:AAGN2vM_lzko5M62drNHAVeoSn0__V1hcwY"

# instancia do bot
bot = telebot.TeleBot(CHAVE_API)

# criar o menu com imagem de fundo
def criar_imagem_menu():
    url_imagem = 'https://i.pinimg.com/736x/0c/7f/db/0c7fdbc5b34079e77ec3f9ce31ad2f56.jpg'

    # upp da imagem
    response = requests.get(url_imagem)
    if response.status_code == 200:
        with open('imagem_fundo.jpg', 'wb') as f:
            f.write(response.content)

    # carrega a imagem com as config corretas
    fundo = Image.open('imagem_fundo.jpg')
    fundo = fundo.resize((800, 600))  # Ajuste o tamanho conforme necessário

    # save da image
    fundo.save('menu_criado.jpg')

# função criar o menu 
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

# envia o menu inicial
@bot.message_handler(commands=["start", "menu"])
def enviar_menu(mensagem):
    # Cria a imagem sem texto
    criar_imagem_menu()

    # envia a imagem junto
    with open('menu_criado.jpg', 'rb') as imagem:
        bot.send_photo(mensagem.chat.id, imagem, caption="Escolha uma opção:", parse_mode="Markdown", reply_markup=criar_menu())

# enviar a resposta baseada na opção escolhida
def enviar_resposta(chat_id, titulo, descricao):
    bot.send_message(chat_id, f"✨ *{titulo}* ✨\n\n{descricao}", parse_mode="Markdown", reply_markup=criar_menu())

# manipulador de callback para o menu
@bot.callback_query_handler(func=lambda call: True)
def callback_menu(call):
    respostas = {
        "planos": {
            "titulo": "Planos e Preços",
            "descricao": (
    "🌟 **Nossos Planos de Jiu-Jitsu** 🌟\n\n"
    "🔹 *Plano KIDs* (3x na semana): R$ 90/mês\n"
    "   - Ideal para crianças, desenvolvendo disciplina e habilidades motoras.\n"
    "   - Aulas divertidas que promovem o aprendizado e a socialização!\n\n"
    
    "🔹 *Plano Teen* (4x na semana): R$ 100/mês\n"
    "   - Perfeito para adolescentes, focando em autocontrole e confiança.\n"
    "   - Melhora a forma física e ensina técnicas de defesa pessoal!\n\n"
    
    "🔹 *Plano Adulto* (5x na semana): R$ 110/mês\n"
    "   - Para adultos que buscam fitness e autodefesa, com treinos intensivos.\n"
    "   - Aumenta a resistência física, reduz o estresse e melhora a qualidade de vida!\n\n"
    
    "📈 **Benefícios de Investir em Nossa Academia**:\n"
    "   - Acesso a professores qualificados e experientes.\n"
    "   - Ambiente seguro e acolhedor para todos os alunos.\n"
    "   - Desenvolvimento de habilidades que vão além do tatame, como disciplina e respeito.\n\n"
    "💰 *Invista em sua saúde e bem-estar! Cada aula é um passo em direção a um você mais forte e confiante!*"
),
        },
        "como_funcionamos": {
            "descricao": (
    "🏆 *Como Funcionamos na Gracie Barra* 🏆\n\n"
    "🔹 *Aulas Estruturadas com Graduações por Faixas*: Cada aluno avança em seu próprio ritmo, garantindo um aprendizado sólido e eficaz. Ao conquistar novas faixas, você não apenas celebra seu progresso, mas também ganha confiança em suas habilidades!\n\n"
    "🔹 *Professores Certificados e Experientes*: Nossa equipe de instrutores é altamente qualificada e apaixonada por ensinar. Eles estão aqui para guiar você em cada passo do caminho, assegurando que você receba a melhor orientação e suporte possíveis.\n\n"
    "🔹 *Ambiente Seguro e Inclusivo*: Na Gracie Barra, criamos um espaço acolhedor para alunos de todas as idades e habilidades. Nossos valores incluem respeito, disciplina e camaradagem, proporcionando uma experiência de aprendizado positiva e enriquecedora.\n\n"
    "✨ **Por que escolher a Gracie Barra?** ✨\n"
    "   - **Transformação Pessoal**: Ao se juntar à nossa comunidade, você não apenas aprende Jiu-Jitsu; você transforma sua vida! Melhore sua condição física, reduza o estresse e aumente sua autoestima.\n"
    "   - **Networking e Amizades**: Conheça pessoas incríveis que compartilham os mesmos interesses. A Gracie Barra é mais do que uma academia; é uma comunidade onde você faz amigos para a vida toda.\n"
    "   - **Resultados Visíveis**: Nossos alunos frequentemente relatam melhorias significativas em sua saúde física e mental. Não perca a chance de experimentar essas mudanças positivas em sua vida!\n\n"
    "🚀 Junte-se a nós e descubra o verdadeiro significado de aprendizado e crescimento. A primeira aula é por nossa conta! Venha sentir a energia da comunidade Gracie Barra!"
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
            "titulo": "Benefícios Incríveis do Jiu-Jitsu",
"descricao": (
    "🥋 *Descubra os Benefícios Transformadores do Jiu-Jitsu!* 🥋\n\n"
    "✅ **Fortalecimento Físico e Mental**: O Jiu-Jitsu não apenas aprimora sua força e resistência, mas também fortalece sua mente. Ao enfrentar desafios no tatame, você desenvolve uma mentalidade resiliente que o ajuda a superar obstáculos na vida.\n\n"
    "✅ **Redução do Estresse**: Após um longo dia, não há nada como uma aula de Jiu-Jitsu para liberar o estresse acumulado. A prática regular ajuda a liberar endorfinas, proporcionando uma sensação de bem-estar e alívio da tensão.\n\n"
    "✅ **Disciplina e Autocontrole**: Aprender Jiu-Jitsu exige foco e dedicação. Através das aulas, você aprende a importância da disciplina, que se reflete em todas as áreas da sua vida, promovendo uma mentalidade de crescimento contínuo.\n\n"
    "✅ **Defesa Pessoal**: O Jiu-Jitsu é uma arte marcial eficaz que ensina técnicas de defesa pessoal práticas e eficientes. Aprender a se proteger não só aumenta sua confiança, mas também proporciona uma sensação de segurança.\n\n"
    "🌟 **Por que escolher o Jiu-Jitsu?** 🌟\n"
    "   - **Comunidade Solidária**: Junte-se a uma comunidade unida de praticantes que se apoiam mutuamente. Aqui, você fará amigos que se tornam parte da sua jornada.\n"
    "   - **Resultados Visíveis**: Não apenas um exercício, o Jiu-Jitsu transforma sua saúde física, sua mente e sua autoestima. Você verá resultados tangíveis rapidamente!\n"
    "   - **Aventura e Diversão**: O Jiu-Jitsu é desafiador e divertido! Aprender novas técnicas e se superar em cada treino torna a prática emocionante e envolvente.\n\n"
    "🚀 *Venha experimentar os benefícios do Jiu-Jitsu!* Junte-se a nós e inicie sua transformação hoje mesmo! A primeira aula é gratuita e está esperando por você!"
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

