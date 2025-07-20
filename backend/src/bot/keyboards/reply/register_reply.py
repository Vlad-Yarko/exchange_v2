from src.bot.utils.keyboard import ReplyKeyboard
from src.bot.utils.button import ContactButton, ReplyButton


register_keyboard = ReplyKeyboard(
    [
        [
            ContactButton('Share phone number').button
        ],
        [
            ReplyButton('quit').button
        ]
    ]
).keyboard()
