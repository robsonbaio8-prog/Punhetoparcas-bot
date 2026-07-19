import logging
import threading
import os
from telebot import TeleBot
from telebot.types import Message

TOKEN = '6108990032:AAFpdv0KmEPOwY3DlSnv32YPGL0dwfHmFmU'
bot = TeleBot(TOKEN)

GRUPO_NOME = "Putaria dos Parças"
GRUPO_LINK = 'https://t.me/+CU0LO7sCpLdjMmIx'
ADMIN_ID = 918023038

# Sistema de advertências
warnings = {}

# Lista de palavras proibidas
PALAVRAS_PROIBIDAS = [
    "menor", "lolita", "pedo", "criança", "kid", "underage", "cp", "child",
    "spam", "flood", "divulgação", "propaganda", "venda", "compra",
    "viado", "bicha", "puta", "puto"  # ajuste conforme necessário
]

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
    bot.reply_to(message, REGRAS, parse_mode='Markdown')

@bot.message_handler(commands=['link', 'grupo', 'join', 'parcas'])
def send_group_link(message):
    bot.reply_to(message, f"🔗 **Link do {GRUPO_NOME}:**\n{GRUPO_LINK}\n\nEntra aí e aproveita! 🔥")

@bot.message_handler(commands=['putaria'])
def putaria(message):
    bot.reply_to(message, "😈 Tá afim de putaria? Manda uma foto ou vídeo pra gente ver então!")

@bot.message_handler(commands=['desafio'])
def desafio(message):
    bot.reply_to(message, "🔥 Desafio do dia: manda uma foto safada no PV de um membro aleatório!")

@bot.message_handler(commands=['confissao'])
def confissao(message):
    bot.reply_to(message, "😏 Envie sua confissão no PV do bot que eu publico anonimamente!")

@bot.message_handler(commands=['punheta'])
def punheta(message):
    bot.reply_to(message, "💦 Tá com a mão na rola? Relaxa e aproveita o grupo! 🔥")

@bot.message_handler(commands=['casal'])
def casal(message):
    bot.reply_to(message, "❤️ Sugestão de casal: vai no PV de alguém e manda um 'oi gostoso' 🔥")

@bot.message_handler(commands=['role'])
def role(message):
    bot.reply_to(message, "🎉 Role de hoje: manda seu vídeo mais safado no grupo!")

@bot.message_handler(commands=['top'])
def top(message):
    bot.reply_to(message, "🏆 Top Putos do Grupo: Ainda em desenvolvimento... manda conteúdo pra subir no ranking!")

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, f"📊 Grupo: {GRUPO_NOME}\nMembros: Ativos e safados 🔥")

# Sistema de palavras proibidas
@bot.message_handler(func=lambda m: True)
def filter_words(message: Message):
    if message.from_user.id == ADMIN_ID:
        return

    text = message.text.lower() if message.text else ""
    for palavra in PALAVRAS_PROIBIDAS:
        if palavra in text:
            user_id = message.from_user.id
            warnings[user_id] = warnings.get(user_id, 0) + 1
            count = warnings[user_id]

            bot.delete_message(message.chat.id, message.message_id)
            warning_msg = bot.reply_to(message, f"⚠️ Palavra proibida detectada! Advertência {count}/3")

            if count >= 3:
                bot.ban_chat_member(message.chat.id, user_id)
                bot.reply_to(message, f"🚫 Usuário banido por repetidas infrações.")
                warnings.pop(user_id, None)
            else:
                threading.Timer(15, lambda: bot.delete_message(message.chat.id, warning_msg.message_id)).start()
            return

# Welcome e delete service messages
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    for member in message.new_chat_members:
        if not member.is_bot:
            bot.send_message(message.chat.id, f"👋 Bem-vindo(a), **{member.first_name}**! {REGRAS}", parse_mode='Markdown')

@bot.message_handler(content_types=['left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'pinned_message'])
def delete_service_messages(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"""
Olá! Sou o bot oficial do **{GRUPO_NOME}** 🔥

Comandos disponíveis:
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

print(f"🤖 {GRUPO_NOME} Bot iniciado!")
bot.infinity_polling()