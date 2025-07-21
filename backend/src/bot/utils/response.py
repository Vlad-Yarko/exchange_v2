from abc import ABC, abstractmethod
from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.utils.keyboard import Keyboard


class Response(ABC):
    @abstractmethod
    def __init__(self):
        pass


class MessageResponse(Response):
    def __init__(
        self, 
        message: Message, 
        text: str = '', 
        keyboard: Optional[Keyboard] = None, 
        state: Optional[FSMContext] = None):
        self.message = message
        self.keyboard = keyboard
        self.text = text
        self.state = state

    async def answer(self):
        await self.message.answer(
            text=self.text,
            reply_markup=self.keyboard
        )


class CallbackResponse(Response):
    def __init__(
        self, 
        callback: CallbackQuery, 
        text: str, 
        keyboard: Optional[Keyboard] = None, 
        click_text: str = "", 
        state: Optional[FSMContext] = None):
        self.callback = callback
        self.keyboard = keyboard
        self.text = text
        self.click_text = click_text
        self.state = state

    async def response(self):
        await self.callback.answer(self.click_text)
        await self.callback.answer(
            text=self.text,
            reply_markup=self.keyboard
        )
