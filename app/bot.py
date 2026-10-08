"""Aiogram 3 adapter. All database work runs outside the asyncio event loop."""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.catalog import CATEGORIES, ROOMS
from app.config import Settings
from app.db import Database
from app.service import DomainError, Service, clean, validate_profile


class Registration(StatesGroup):
    room = State()
    name = State()
    profile = State()


class Ordering(StatesGroup):
    category = State()
    service = State()
    detail = State()


def keyboard(items):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=value)] for text, value in items]
    )


def make_router(service, settings):
    router = Router(name="guest")

    async def menu(message, state):
        await state.set_state(Ordering.category)
        await message.answer(
            "Choose a service category:", reply_markup=keyboard([(x[1], "cat:" + x[0]) for x in CATEGORIES])
        )

    @router.message(CommandStart())
    async def start(message: Message, state: FSMContext):
        await state.clear()
        guest = await asyncio.to_thread(service.guest_for_telegram, message.from_user.id)
        if guest:
            await menu(message, state)
        else:
            text = "Welcome to the hotel service prototype. Your room, name and requests will be stored for this demo. Use fictional information. This is not a verified check-in system. Choose a room:"
            await state.set_state(Registration.room)
            await message.answer(text, reply_markup=keyboard([(r, "room:" + r) for r in ROOMS]))

    @router.message(Command("cancel"))
    async def cancel(message: Message, state: FSMContext):
        await state.clear()
        await message.answer("Current entry cancelled. Use /start to return to services.")

    @router.message(Command("requests"))
    async def requests(message: Message):
        guest = await asyncio.to_thread(service.guest_for_telegram, message.from_user.id)
        if not guest:
            await message.answer("Please register with /start first.")
            return
        rows = await asyncio.to_thread(service.guest_requests, guest["id"])
        text = "\n".join(f"{r['id']} | {r['service']} | {r['status']}" for r in rows) or "No requests yet."
        await message.answer(text + "\n\nAfter resolution: /rate REQUEST_ID 1-5")

    @router.message(Command("rate"))
    async def rate(message: Message):
        guest = await asyncio.to_thread(service.guest_for_telegram, message.from_user.id)
        bits = (message.text or "").split()
        if not guest or len(bits) != 3 or not bits[2].isdigit():
            await message.answer("Use /rate REQUEST_ID 1-5 after registering.")
            return
        try:
            await asyncio.to_thread(service.rate, bits[1], guest["id"], int(bits[2]))
        except DomainError as error:
            await message.answer(error.message)
        else:
            await message.answer("Thank you. Your service rating has been saved.")

    @router.callback_query(Registration.room, F.data.startswith("room:"))
    async def room(call: CallbackQuery, state: FSMContext):
        await call.answer()
        value = call.data.split(":", 1)[1]
        if value not in ROOMS:
            await call.message.answer("Choose a room from the list.")
            return
        await state.update_data(room=value)
        await state.set_state(Registration.name)
        await call.message.answer("What name should we use? Use a fictional name for the demo.")

    async def finish_registration(message, state):
        data = await state.get_data()
        try:
            await asyncio.to_thread(
                service.register_guest,
                message.from_user.id,
                data["room"],
                data["name"],
                **data.get("profile", {}),
            )
        except DomainError as error:
            await message.answer(error.message)
            return
        await state.clear()
        await message.answer("Registration saved. You can now submit service requests.")
        await menu(message, state)

    @router.message(Registration.name, F.text)
    async def name(message: Message, state: FSMContext):
        try:
            value = clean(message.text, maximum=80)
        except DomainError as error:
            await message.answer(error.message)
            return
        await state.update_data(name=value)
        if settings.extended_profile:
            await state.update_data(profile={}, profile_index=0)
            await state.set_state(Registration.profile)
            await message.answer(
                "Optional legacy profile: date of birth YYYY-MM-DD, or /skip. Use fictional data."
            )
        else:
            await finish_registration(message, state)

    profile_fields = [
        ("birthday", "date of birth YYYY-MM-DD"),
        ("gender", "gender: Female, Male or Prefer not to say"),
        ("email", "email address"),
        ("phone", "phone number"),
    ]

    @router.message(Registration.profile, F.text)
    async def profile(message: Message, state: FSMContext):
        data = await state.get_data()
        index = data["profile_index"]
        field = profile_fields[index][0]
        value = None
        if message.text != "/skip":
            try:
                value = validate_profile(field, message.text)
            except DomainError as error:
                await message.answer(error.message + ", or /skip")
                return
        data["profile"][field] = value
        await state.update_data(profile=data["profile"], profile_index=index + 1)
        if index == 3:
            await finish_registration(message, state)
        else:
            await message.answer("Optional " + profile_fields[index + 1][1] + ", or /skip")

    @router.callback_query(Ordering.category, F.data.startswith("cat:"))
    async def category(call: CallbackQuery, state: FSMContext):
        await call.answer()
        guest = await asyncio.to_thread(service.guest_for_telegram, call.from_user.id)
        if not guest:
            await call.message.answer("Register with /start first.")
            return
        cat = next((x for x in CATEGORIES if x[0] == call.data.split(":", 1)[1]), None)
        if not cat:
            await call.message.answer("Select a listed category.")
            return
        await state.update_data(category=cat[0])
        await state.set_state(Ordering.service)
        if cat[0] == "safety":
            await call.message.answer(
                "For an urgent incident, contact reception directly. This prototype does not provide emergency response."
            )
        await call.message.answer(
            "Choose a service:", reply_markup=keyboard([(x, f"svc:{i}") for i, x in enumerate(cat[3])])
        )

    @router.callback_query(Ordering.service, F.data.startswith("svc:"))
    async def subservice(call: CallbackQuery, state: FSMContext):
        await call.answer()
        data = await state.get_data()
        cat = next((x for x in CATEGORIES if x[0] == data.get("category")), None)
        index = call.data.split(":", 1)[1]
        if not cat or not index.isdigit() or int(index) >= len(cat[3]):
            await call.message.answer("Select a listed service.")
            return
        await state.update_data(service=cat[3][int(index)])
        await state.set_state(Ordering.detail)
        if cat[0] == "room_service" and settings.menu_file_id:
            try:
                await call.message.answer_photo(settings.menu_file_id)
            except Exception as error:
                logging.warning("Optional menu could not be displayed (%s)", type(error).__name__)
        await call.message.answer(
            "Add timing, quantities or preferences (1-1000 characters). Use /cancel to cancel."
        )

    @router.message(Ordering.detail, F.text)
    async def submit(message: Message, state: FSMContext):
        data = await state.get_data()
        guest = await asyncio.to_thread(service.guest_for_telegram, message.from_user.id)
        if not guest:
            await message.answer("Register with /start first.")
            return
        try:
            rid = await asyncio.to_thread(
                service.create_request,
                guest["id"],
                data["category"],
                data["service"],
                message.text,
                f"tg:{message.chat.id}:{message.message_id}",
            )
        except DomainError as error:
            await message.answer(error.message)
            return
        except Exception as error:
            logging.error("Request persistence failed (%s)", type(error).__name__)
            await message.answer("We could not save this request. Please retry or contact reception.")
            return
        await state.clear()
        await message.answer(f"Request {rid} has been saved. Use /requests to check its status.")
        await menu(message, state)

    @router.callback_query()
    async def stale_callback(call: CallbackQuery):
        await call.answer("This button has expired. Use /start.", show_alert=True)

    @router.message(StateFilter("*"))
    async def fallback(message: Message):
        await message.answer(
            "Please use text and the listed buttons. /start opens services; /cancel cancels an entry."
        )

    return router


async def main():
    settings = Settings.from_env()
    if not settings.bot_token:
        raise SystemExit("Set a newly issued TELEGRAM_BOT_TOKEN in your private .env file first.")
    db = Database(settings.database)
    db.initialize()
    dispatcher = Dispatcher(storage=MemoryStorage(), events_isolation=SimpleEventIsolation())
    dispatcher.include_router(make_router(Service(db), settings))
    async with Bot(settings.bot_token) as bot:
        await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
