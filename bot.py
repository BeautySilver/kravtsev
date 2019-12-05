from flask import Flask, render_template, url_for, redirect, request
import telebot
from telebot import types
import os


token = '978400572:AAExdSjEBoV8DH55G5ypRLvNBf5Zq0U5j9o'
bot = telebot.TeleBot(token)

users = {}
keyboard_for_sex = types.ReplyKeyboardMarkup(True, True)
keyboard_for_sex.row('Ã')
keyboard_for_sex.row('∆')
keyboard_for_sex_change = types.ReplyKeyboardMarkup(True, True)
keyboard_for_sex_change.row('Ã')
keyboard_for_sex_change.row('∆')
keyboard_for_sex_change.row('Õ‡Á‡‰')

main_menu_keyboard = types.InlineKeyboardMarkup()
change_name = types.InlineKeyboardButton(text='»ÁÏÂÌËÚ¸ ËÏˇ', callback_data='change_name')
change_sex = types.InlineKeyboardButton(text='»ÁÏÂÌËÚ¸ ÔÓÎ', callback_data='change_sex')
change_age = types.InlineKeyboardButton(text='»ÁÏÂÌËÚ¸ ‚ÓÁ‡ÒÚ', callback_data='change_age')
main_menu_keyboard.add(change_name, change_sex, change_age)

return_to_main = types.InlineKeyboardMarkup()
return_to_main.add(types.InlineKeyboardButton(text='Õ‡Á‡‰', callback_data='return_to_main'))


app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.from_user.id not in users:
        bot.send_message(message.from_user.id, 'œË‚ÂÚ! ¬‚Â‰Ë Ò‚Ó∏ ËÏˇ.')
        users.update({message.from_user.id:{'name':None, 'sex':None, 'age':None, 'changing':None}})


@bot.message_handler(commands=['menu'])
def menu_handler(message):
    bot.send_message(message.from_user.id, '√Î‡‚ÌÓÂ ÏÂÌ˛', reply_markup=main_menu_keyboard)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    if users[message.from_user.id]['name'] is None:
        users[message.from_user.id]['name'] = message.text
        bot.send_message(message.from_user.id, '“ÂÔÂ¸ ‚˚·ÂË ÔÓÎ.', reply_markup=keyboard_for_sex)

    elif users[message.from_user.id]['sex'] is None:
        users[message.from_user.id]['sex'] = message.text
        bot.send_message(message.from_user.id, '“ÂÔÂ¸ ‚‚Â‰Ë Ò‚ÓÈ ‚ÓÁ‡ÒÚ.')

    elif users[message.from_user.id]['age'] is None:
        try:
            users[message.from_user.id]['age'] = int(message.text)
            menu_handler(message)

        except ValueError:
            bot.send_message(message.from_user.id, '¬ÓÁ‡ÒÚ ÏÓÊÂÚ ·˚Ú¸ ÚÓÎ¸ÍÓ ˜ËÒÎÓÏ! œÓÔÓ·ÛÈ Â˘∏ ‡Á.')

    elif users[message.from_user.id]['changing'] == 'name':
        if message.text != users[message.from_user.id]['name']:
            users[message.from_user.id]['name'] = message.text
            menu_handler(message)
        else:
            bot.send_message(message.from_user.id, '›ÚÓ ‚‡¯Â ÔÂ‰˚‰Û˘ÂÂ ËÏˇ, ‚‚Â‰ËÚÂ ÌÓ‚ÓÂ ËÎË ‚ÂÌËÚÂÒ¸ ‚ „Î‡‚ÌÓÂ ÏÂÌ˛.',
                                reply_markup=return_to_main)

    elif users[message.from_user.id]['changing'] == 'age':
        try:
            if int(message.text) != users[message.from_user.id]['age']:
                users[message.from_user.id]['sex'] = message.text
                menu_handler(message)
            else:
                bot.send_message(message.from_user.id,
                                 '›ÚÓ ‚‡¯ ÔÂ‰˚‰Û˘ËÈ ‚ÓÁ‡ÒÚ, ‚‚Â‰ËÚÂ ÌÓ‚˚È ËÎË ‚ÂÌËÚÂÒ¸ ‚ „Î‡‚ÌÓÂ ÏÂÌ˛.',
                                 reply_markup=return_to_main)

        except ValueError:
            bot.send_message(message.from_user.id, '¬ÓÁ‡ÒÚ ÏÓÊÂÚ ·˚Ú¸ ÚÓÎ¸ÍÓ ˜ËÒÎÓÏ! œÓÔÓ·ÛÈ Â˘∏ ‡Á.')

    elif users[message.from_user.id]['changing'] == 'sex':
        if message.text == 'Õ‡Á‡‰':
            users[message.from_user.id]['changing'] = None
            menu_handler(message)
        elif message.text != users[message.from_user.id]['sex']:
            users[message.from_user.id]['name'] = message.text

        else:
            bot.send_message(message.from_user.id, '›ÚÓ ‚‡¯ ÔÂ‰˚‰Û˘ËÈ ÔÓÎ, ‚˚·ÂËÚÂ ÌÓ‚˚È ËÎË ‚ÂÌËÚÂÒ¸ ‚ „Î‡‚ÌÓÂ ÏÂÌ˛.',
                                reply_markup=keyboard_for_sex_change)


@bot.callback_query_handler(func=lambda call: True)
def main_menu(call):
    if call.data == 'change_name':
        bot.send_message(call.from_user.id, '¬‚Â‰ËÚÂ ÌÓ‚ÓÂ ËÏˇ', reply_markup=return_to_main)
        users[call.from_user.id]['changing'] = 'name'

    elif call.data == 'change_sex':
        bot.send_message(call.from_user.id, '¬˚·ÂËÚÂ ÌÓ‚˚È ÔÓÎ', reply_markup=keyboard_for_sex_change)
        users[call.from_user.id]['changing'] = 'sex'

    elif call.data == 'change_age':
        bot.send_message(call.from_user.id, '¬‚Â‰ËÚÂ ÌÓ‚˚È ‚ÓÁ‡ÒÚ', reply_markup=return_to_main)
        users[call.from_user.id]['changing'] = 'age'

    elif call.data == 'return_to_main':
        users[call.from_user.id]['changing'] = None
        menu_handler(call)


def send_to_all(text):
    for user in users.keys():
        bot.send_message(user, text)


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('index.html')


@app.route('/' + token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://glacial-springs-03014.herokuapp.com/ ' + token)
    return "!", 200


@app.route('/send_message', methods=['POST'])
def send_message():
    send_to_all(request.form['message'])
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
