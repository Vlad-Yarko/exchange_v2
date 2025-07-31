from abc import ABC, abstractmethod

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from src.bot.utils.button import Button


class Keyboard(ABC):
    def __init__(self, buttons: list[list[Button]]):
        self.buttons = buttons

    @abstractmethod
    def keyboard(self):
        pass


class InlineKeyboard(Keyboard):
    def keyboard(self):
        return InlineKeyboardMarkup(inline_keyboard=self.buttons)


class ReplyKeyboard(Keyboard):
    def keyboard(self):
        return ReplyKeyboardMarkup(keyboard=self.buttons, resize_keyboard=True, one_time_keyboard=True)
