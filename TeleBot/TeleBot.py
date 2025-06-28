import telebot
from telebot import types
import json
import os

chave = "7842614654:AAFymeWI5pw1YeS759FkX9lwoasrL4g-zR8"
bot = telebot.TeleBot(chave)

# Carregando o menu de um arquivo JSON
with open('menu.json', 'r') as file:
    menu = json.load(file)

@bot.message_handler(commands=['start'])
def start(msg: telebot.types.Message): 
    markup = types.InlineKeyboardMarkup()
    
    botao_cardapio = types.InlineKeyboardButton('Cardápio', callback_data='botao_cardapio')
    botao_contato = types.InlineKeyboardButton('Contato', callback_data='botao_contato')
    
    markup.add(botao_cardapio, botao_contato)
    bot.send_message(msg.chat.id, 'Bem vindo!', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def responder(msg: telebot.types.Message):
    if msg.text == '/ok':
        confirmar_pedido(msg)
    else:
        bot.send_message(msg.chat.id, 'Digite /start para ver o menu.')

@bot.callback_query_handler(func=lambda call: True)
def resposta_botao(call: types.CallbackQuery):
    if call.data == 'botao_cardapio':
        cardapio = types.InlineKeyboardMarkup()
        for dish in menu.keys():
            cardapio.add(types.InlineKeyboardButton(dish, callback_data=f'prato_{dish}'))
        bot.send_message(call.message.chat.id, 'Escolha um prato:', reply_markup=cardapio)
    elif call.data == 'botao_contato':
        contatos(call.message.chat.id)
    elif call.data.startswith('prato_'):
        dish = call.data[len('prato_'):]
        prato_detalhes(call.message.chat.id, dish)
        bot.send_message(call.message.chat.id, f'Você escolheu {dish}. Digite /ok para confirmar o pedido.')
    elif call.data == 'botao_feed':
        feedback(call.message)
    elif call.data == 'botao_avalicao1':
        bot.send_message(call.message.chat.id, '"Lamentamos que sua experiência tenha sido muito ruim. Agradecemos seu feedback e estamos comprometidos em melhorar nosso atendimento. Por favor, nos diga como podemos fazer melhor."')
    elif call.data == 'botao_avalicao2':
        bot.send_message(call.message.chat.id, '"Sentimos muito que sua experiência tenha sido ruim. Obrigado por nos informar. Estamos trabalhando para melhorar e garantir que isso não aconteça novamente."')
    elif call.data == 'botao_avalicao3':
        bot.send_message(call.message.chat.id, '"Agradecemos sua avaliação. Parece que sua experiência foi média. Se tiver sugestões sobre como podemos melhorar, gostaríamos muito de ouvi-las."')
    elif call.data == 'botao_avalicao4':
        bot.send_message(call.message.chat.id, '"Obrigado por sua avaliação! Ficamos felizes em saber que você teve uma boa experiência. Se tiver alguma sugestão para nos ajudar a alcançar uma avaliação excelente, por favor, compartilhe conosco."')
    elif call.data == 'botao_avalicao5':
        bot.send_message(call.message.chat.id, '"Uau! Muito obrigado por sua avaliação excelente! Estamos muito felizes em saber que você teve uma experiência fantástica. Seu feedback positivo nos motiva a continuar oferecendo o melhor serviço possível."')

@bot.message_handler(commands=['ok'])
def confirmar_pedido(message):
    bot.send_message(message.chat.id, "✅ Pedido confirmado!\nStatus: em preparo")
    tempo_previsto = "30 minutos"
    bot.send_message(message.chat.id, f"O tempo previsto para entrega é de {tempo_previsto}.")
    perguntar_feedback(message.chat.id)

def perguntar_feedback(chat_id):
    markup = types.InlineKeyboardMarkup()
    botao_sim = types.InlineKeyboardButton('Sim', callback_data='botao_feed')
    botao_nao = types.InlineKeyboardButton('Não', callback_data='botao_nao')
    
    markup.add(botao_sim, botao_nao)
    bot.send_message(chat_id, "Gostaria de avaliar nosso atendimento?", reply_markup=markup)

def prato_detalhes(chat_id, dish):
    photo_path = menu[dish]['image_path']
    price = menu[dish]['price']
    description = menu[dish]['description']
    
    if os.path.exists(photo_path):
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=f'{dish} - {price}\n{description}')
    else:
        bot.send_message(chat_id, f'{dish} - {price}\n{description}\nDesculpe, não consegui encontrar a imagem para {dish}.')

def contatos(chat_id):
    bot.send_message(chat_id, 'Contatos: \n📧 Email: bot@gmail.com\n📞 Número: 65817864\n📸 Instagram: @gastro_bot')

def feedback(message):
    bot.send_message(message.chat.id, "Por favor, avalie nosso atendimento.")
    botao_avaliacao(message.chat.id)

def botao_avaliacao(chat_id):
    markup = types.InlineKeyboardMarkup()
    botao_avaliacao1 = types.InlineKeyboardButton('⭐', callback_data='botao_avalicao1')
    botao_avaliacao2 = types.InlineKeyboardButton('⭐⭐',callback_data='botao_avalicao2')
    botao_avaliacao3 = types.InlineKeyboardButton('⭐⭐⭐',callback_data='botao_avalicao3')
    botao_avaliacao4 = types.InlineKeyboardButton('⭐⭐⭐⭐',callback_data='botao_avalicao4')
    botao_avaliacao5 = types.InlineKeyboardButton('⭐⭐⭐⭐⭐',callback_data='botao_avalicao5')
    
    markup.add(botao_avaliacao1, botao_avaliacao2, botao_avaliacao3, botao_avaliacao4, botao_avaliacao5)
    bot.send_message(chat_id, "Escolha uma avaliação:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
def handle_rating(message):
    rating = message.text
    bot.send_message(message.chat.id, f"Obrigado pela sua avaliação: {rating}!")

bot.polling(timeout=60, long_polling_timeout=60)
