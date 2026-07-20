import telebot
import threading

TOKEN = '6108990032:AAFpdv0KmEPOwY3DlSnv32YPGL0dwfHmFmU'
bot = telebot.TeleBot(TOKEN)

GRUPO_NOME = "Putaria dos Parças"
GRUPO_LINK = 'https://t.me/+dO79EwVFMak2YzY0'
ADMIN_ID = 918023038

REGRAS = f"""
🚨 **REGRAS DO {GRUPO_NOME.upper()}** 🚨

1. Conteúdo +18 apenas.
2. Respeito mútuo, sem spam ou flood.
3. Proibido menores de idade (ban imediato).
4. Sem divulgação de outros grupos sem permissão.
5. Divirta-se com moderação 😈

Bem-vindo(a)! Siga as regras para ficar no grupo. 🔥
"""

@bot.message_handler(commands=['regras'])
def regras(message):
    bot.send_message(message.chat.id, REGRAS, parse_mode='Markdown')

@bot.message_handler(commands=['link', 'grupo', 'join', 'parcas'])
def send_group_link(message):
    bot.send_message(message.chat.id, f"🔗 **Link do {GRUPO_NOME}:**\n{GRUPO_LINK}\n\nEntra aí e aproveita! 🔥")

@bot.message_handler(commands=['putaria'])
def putaria(message):
    bot.send_message(message.chat.id, "😈 Tá afim de putaria? Manda uma foto ou vídeo pra gente ver então!")

@bot.message_handler(commands=['desafio'])
def desafio(message):
    bot.send_message(message.chat.id, "🔥 Desafio do dia: manda uma foto safada no PV de um membro aleatório!")

@bot.message_handler(commands=['confissao'])
def confissao(message):
    bot.send_message(message.chat.id, "😏 Envie sua confissão no PV do bot que eu publico anonimamente!")

@bot.message_handler(commands=['punheta'])
def punheta(message):
    bot.send_message(message.chat.id, "💦 Tá com a mão na rola? Relaxa e aproveita o grupo! 🔥")

@bot.message_handler(commands=['casal'])
def casal(message):
    bot.send_message(message.chat.id, "❤️ Sugestão de casal: vai no PV de alguém e manda um 'oi gostoso' 🔥")

@bot.message_handler(commands=['role'])
def role(message):
    bot.send_message(message.chat.id, "🎉 Role de hoje: manda seu vídeo mais safado no grupo!")

@bot.message_handler(commands=['top'])
def top(message):
    bot.send_message(message.chat.id, "🏆 Top Putos do Grupo: Ainda em desenvolvimento... manda conteúdo pra subir no ranking!")

@bot.message_handler(commands=['status'])
def status(message):
    bot.send_message(message.chat.id, f"📊 Grupo: {GRUPO_NOME}\nMembros: Ativos e safados 🔥")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"""
Olá! Sou o bot oficial do **{GRUPO_NOME}** 🔥

Comandos:
/regras - Regras do grupo
/link - Link do grupo
/putaria - Modo putaria
/desafio - Desafio picante
/confissao - Envie confissão anônima
/punheta - Motivação
/casal - Sugestão de casal
/role - Role do dia
/top - Ranking
/status - Status do grupo
/ajuda - Esta mensagem
    """)

# Bloqueio de links (só admins podem enviar)
@bot.message_handler(func=lambda m: True)
def block_links(message):
    if message.from_user.id == ADMIN_ID:
        return
    if message.entities:
        for entity in message.entities:
            if entity.type in ['url', 'text_link']:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                    warning = bot.send_message(message.chat.id, "🚫 Apenas admins podem enviar links!")
                    threading.Timer(15, lambda: bot.delete_message(message.chat.id, warning.message_id)).start()
                except:
                    pass
                return

# Sistema de palavras proibidas
@bot.message_handler(func=lambda m: True)
def filter_words(message):
    if message.from_user.id == ADMIN_ID:
        return
    text = message.text.lower() if message.text else ""
    palavras_proibidas = ["menor", "lolita", "pedo", "criança", "kid", "underage", "spam", "flood"]
    for palavra in palavras_proibidas:
        if palavra in text:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "⚠️ Palavra proibida detectada! Cuidado com o que posta.")
            except:
                pass
            return

# Boas-vindas com deleção automática após 60 segundos
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    for member in message.new_chat_members:
        if not member.is_bot:
            try:
                sent_msg = bot.send_message(
                    message.chat.id, 
                    f"👋 Bem-vindo(a), **{member.first_name}**! {REGRAS}", 
                    parse_mode='Markdown'
                )
                # Deleta a mensagem de boas-vindas após 60 segundos
                def delete_welcome():
                    try:
                        bot.delete_message(message.chat.id, sent_msg.message_id)
                    except:
                        pass
                threading.Timer(60, delete_welcome).start()
            except:
                pass

# Deleção de todas as mensagens de serviço
@bot.message_handler(content_types=[
    'left_chat_member', 
    'new_chat_title', 
    'new_chat_photo', 
    'delete_chat_photo', 
    'group_chat_created', 
    'supergroup_chat_created', 
    'channel_chat_created', 
    'message_auto_delete_timer_changed',
    'pinned_message'
])
def delete_service_messages(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

print(f"🤖 {GRUPO_NOME} Bot iniciado!")
bot.infinity_polling()
