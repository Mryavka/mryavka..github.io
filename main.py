import pip

pip.main(['install', 'python-telegram-bot'])
import logging
from background import keep_alive
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto, InputMediaVideo
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler

TG_TOKEN = "6192367753:AAHwWNyKUcL6tS18Xvr8a72wEWpgyTNsysI"
strategy = "🎮 Тактика"
scores = "Очки"
cups = "🏆 Инфо по кубкам"
tournament = "🏆 Турнир"
evolution = "⬆ Эволюция"
usual_day = "⛅ Типичный день"
wind = "🌀 Ветер перемен"
starfall = "🌠 Звездопад"
chaosstorm = "🌩️ Шторм хаоса"
surprise = "🎇 Сюрприз"
corners = "🎯 Углы"
slimes = "👾 Атака слизней"
curse = "💀 Проклятье"
brownian_motion = "🔄 Броумовское движение"
extremum = "🗡 Экстремум"
drying = "🫗 Засуха"
next_b = "⏩ Далее"
back_b = "⏪ Назад"
main_menu = "📱 Главное меню"
hero_gear = "Герои и Предметы"
robbery = "⚔ Грабежи"
items = "Предметы"
heroes = "Герои"
heroic_items = "Героические предметы"
daily_fight = "🤳 Бой дня"
peshki = "♟ Инфо по пешкам"
usual_p = "Обычная"
rare_p = "Редкая"
epic_p = "Эпическая"
leg_p = "Легендарная"
bot_page = 1
dragon = "🐲 Измерение драконов"
d1 = "☠️ Жизнекрад ☠️"
d2 = "⚡️ Молниеносец ⚡️"
d3 = "🔥 Пламеносец 🔥"
d4 = "😈 Душелов 😈"
mark = "Печать"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_page
    bot_page = 1
    keyboard_main = [
        [KeyboardButton(tournament), KeyboardButton(dragon)],
        [KeyboardButton(hero_gear), KeyboardButton(peshki)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard_main, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.message.chat_id, text="Выберите опцию:", reply_markup=reply_markup)


async def handle_tournament_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    keyboard_tournament = [
        [KeyboardButton(strategy), KeyboardButton(robbery)],
        [KeyboardButton(daily_fight), KeyboardButton(cups)],
        [KeyboardButton(scores), KeyboardButton(main_menu)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard_tournament, resize_keyboard=True)
    if text == tournament:
        await context.bot.send_message(chat_id=update.message.chat_id, text="Выберите категорию:",
                                       reply_markup=reply_markup)
    elif text == scores:
        await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'images/{text}.jpg', 'rb'))
        ])
        await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'images/{text} 1.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'images/{text} 2.jpg', 'rb'))
        ], caption="День 1")
        await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'images/{text} 3.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'images/{text} 4.jpg', 'rb'))
        ], caption="День 2")
    else:
        caption = get_caption(text)
        await context.bot.send_message(chat_id=update.message.chat_id, text=caption)


async def handle_daily_fight_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    global bot_page
    if text == next_b:
        bot_page = bot_page + 1
    elif text == back_b:
        bot_page = bot_page - 1

    if bot_page == 1:
        keyboard_daily_fight = [
            [KeyboardButton(tournament), KeyboardButton(main_menu)],
            [KeyboardButton(evolution), KeyboardButton(usual_day)],
            [KeyboardButton(wind), KeyboardButton(starfall)],
            [KeyboardButton(next_b)]
        ]
    elif bot_page == 2:
        keyboard_daily_fight = [
            [KeyboardButton(tournament), KeyboardButton(main_menu)],
            [KeyboardButton(chaosstorm), KeyboardButton(surprise)],
            [KeyboardButton(corners), KeyboardButton(slimes)],
            [KeyboardButton(back_b), KeyboardButton(next_b)]
        ]
    elif bot_page == 3:
        keyboard_daily_fight = [
            [KeyboardButton(tournament), KeyboardButton(main_menu)],
            [KeyboardButton(curse), KeyboardButton(brownian_motion)],
            [KeyboardButton(extremum), KeyboardButton(drying)],
            [KeyboardButton(back_b)]
        ]

    reply_markup = ReplyKeyboardMarkup(keyboard_daily_fight, resize_keyboard=True)

    if text == daily_fight:
        f = open(rf'texts/{text}.txt', 'r', encoding='utf-8')
        caption = f.read()
        f.close()

        await context.bot.send_message(chat_id=update.message.chat_id, text=caption)
        await context.bot.send_message(chat_id=update.message.chat_id, text="Выберите Бой дня:",
                                       reply_markup=reply_markup)
    elif text == back_b or text == next_b:
        await context.bot.send_message(chat_id=update.message.chat_id, text="Выберите Бой дня:",
                                       reply_markup=reply_markup)
    else:
        caption = get_caption(text)
        if text != strategy:
            await context.bot.sendMediaGroup(chat_id=update.message.chat_id, caption=caption, media=[
                InputMediaPhoto(media=open(rf'images/{text}.jpg', 'rb'))])
        else:
            await context.bot.send_message(chat_id=update.message.chat_id, text=caption)


# Обработчик нажатия кнопок уровня Шмот героя
async def hero_gear_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    keyboard_gear = [
        [KeyboardButton(heroes), KeyboardButton(items)],
        [KeyboardButton(heroic_items), KeyboardButton(main_menu)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard_gear, resize_keyboard=True)
    if text == hero_gear:
        await context.bot.send_message(chat_id=update.message.chat_id, text="Выберите раздел:",
                                       reply_markup=reply_markup)
    elif text == heroes:
      await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
          InputMediaPhoto(media=open(rf'images/{text}.jpg', 'rb')),])
      await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'images/{text} 1.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'images/{text} 2.jpg', 'rb'))
        ])
    elif text == heroic_items:
        await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'images/{text}.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'images/{text} 1.jpg', 'rb'))
        ])
    elif text == items:
        await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'images/{text}.jpg', 'rb'))])
        await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'images/{text} 1.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'images/{text} 2.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'images/{text} 3.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'images/{text} 4.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'images/{text} 5.jpg', 'rb'))
        ])


async def peshki_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(usual_p), KeyboardButton(rare_p)],
        [KeyboardButton(epic_p), KeyboardButton(leg_p)],
        [KeyboardButton(main_menu)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    text = update.message.text
    await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[    
      InputMediaPhoto(media=open(rf'images/{text}.jpg', 'rb'))
    ])
    await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
        InputMediaPhoto(media=open(rf'images/{text} 1.jpg', 'rb')),
        InputMediaPhoto(media=open(rf'images/{text} 2.jpg', 'rb')),
        InputMediaPhoto(media=open(rf'images/{text} 3.jpg', 'rb')),
        InputMediaPhoto(media=open(rf'images/{text} 4.jpg', 'rb')),
        InputMediaPhoto(media=open(rf'images/{text} 5.jpg', 'rb'))
    ])
    if text == peshki:
        caption = get_caption(text)
        await context.bot.send_message(chat_id=update.message.chat_id, text=caption, reply_markup=reply_markup)
    else:
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(rf'images/{text}.jpg', 'rb'),
                                     reply_markup=reply_markup)


async def dragon_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(d1), KeyboardButton(d2)],
        [KeyboardButton(d3), KeyboardButton(d4)],
        [KeyboardButton(mark), KeyboardButton(main_menu)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    text = update.message.text
    if text == dragon:
        caption = "Выберите дракона:"
        await context.bot.send_message(chat_id=update.message.chat_id, text=caption, reply_markup=reply_markup)
    elif text == mark:
        caption = get_caption(text)
        await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'dragons/{text}.jpg', 'rb')),
            InputMediaVideo(media=open(rf'dragons/{text} 1.mp4', 'rb')),
            InputMediaVideo(media=open(rf'dragons/{text} 2.mp4', 'rb'))
        ])
        await context.bot.send_message(chat_id=update.message.chat_id, text=caption, parse_mode='Markdown')
    else:
        caption = get_caption(text)
        await context.bot.sendMediaGroup(chat_id=update.message.chat_id, media=[
            InputMediaPhoto(media=open(rf'dragons/{text} 1.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'dragons/{text} 2.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'dragons/{text} 3.jpg', 'rb')),
            InputMediaPhoto(media=open(rf'dragons/{text} 4.jpg', 'rb'))
        ])
        await context.bot.send_message(chat_id=update.message.chat_id, text=caption, parse_mode='html')


def get_caption(text):
    f = open(rf'texts/{text}.txt', 'r', encoding='utf-8')
    caption = f.read()
    f.close()
    return caption


if __name__ == '__main__':
    application = ApplicationBuilder().token(TG_TOKEN).build()

    start_handler = CommandHandler('start', start)
    daily_fight_handler = MessageHandler(filters.Regex(f'^({daily_fight}|{evolution}|{usual_day}|{wind}|'
                                                      f'{starfall}|{chaosstorm}|{surprise}|{corners}|'
                                                      f'{slimes}|{curse}|{brownian_motion}|{extremum}|'
                                                      f'{drying}|{next_b}|{back_b})$'), handle_daily_fight_button)
    tournament_handler = MessageHandler(filters.Regex(f'^({tournament}|{strategy}|{robbery}|{cups}|{scores})$'),
                                        handle_tournament_button)
    main_menu_handler = MessageHandler(filters.Regex(f'^({main_menu})$'), start)
    hero_gear_handler = MessageHandler(filters.Regex(f'^({heroes}|{heroic_items}|{items}|{hero_gear})$'), hero_gear_button)
    peshki_handler = MessageHandler(filters.Regex(f'^({peshki}|{usual_p}|{rare_p}|{epic_p}|{leg_p})$'), peshki_button)
    dragon_handler = MessageHandler(filters.Regex(f'^({dragon}|{d1}|{d2}|{d3}|{d4}|{mark})$'), dragon_button)

    application.add_handler(start_handler)
    application.add_handler(daily_fight_handler)
    application.add_handler(tournament_handler)
    application.add_handler(hero_gear_handler)
    application.add_handler(main_menu_handler)
    application.add_handler(peshki_handler)
    application.add_handler(dragon_handler)
    keep_alive()
    application.run_polling()
