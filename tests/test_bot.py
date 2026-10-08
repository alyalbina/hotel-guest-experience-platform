import asyncio
from datetime import datetime, timezone

from aiogram import Bot, Dispatcher
from aiogram.client.session.base import BaseSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import AnswerCallbackQuery, SendMessage, SendPhoto
from aiogram.types import CallbackQuery, Chat, Message, Update, User

from app.bot import make_router
from app.config import Settings


class OfflineTelegram(BaseSession):
    """Exercises real aiogram dispatch without connecting to Telegram."""

    def __init__(self):
        super().__init__()
        self.sent = []

    async def close(self):
        pass

    async def make_request(self, bot, method, timeout=None):
        if isinstance(method, AnswerCallbackQuery):
            return True
        if isinstance(method, (SendMessage, SendPhoto)):
            self.sent.append(getattr(method, "text", None) or "PHOTO")
            return Message(
                message_id=len(self.sent),
                date=datetime.now(timezone.utc),
                chat=Chat(id=int(method.chat_id), type="private"),
                text=getattr(method, "text", None),
            )
        raise AssertionError(f"Unexpected Telegram method: {type(method).__name__}")

    async def stream_content(self, url, headers=None, timeout=30, chunk_size=65536, raise_for_status=True):
        yield b""


def harness(svc, extended=False):
    session = OfflineTelegram()
    bot = Bot(token="12345:" + "A" * 35, session=session)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(make_router(svc, Settings(extended_profile=extended)))
    user = User(id=789123, is_bot=False, first_name="Fictional")
    counter = 0

    async def send(text=None, callback=None):
        nonlocal counter
        counter += 1
        message = Message(
            message_id=counter,
            date=datetime.now(timezone.utc),
            chat=Chat(id=user.id, type="private"),
            from_user=user,
            text=text,
        )
        if callback:
            update = Update(
                update_id=counter,
                callback_query=CallbackQuery(
                    id=str(counter), from_user=user, chat_instance="demo", data=callback, message=message
                ),
            )
        else:
            update = Update(update_id=counter, message=message)
        await dp.feed_update(bot, update)

    return session, send, dp, bot


def test_real_dispatch_registration_request_failure_recovery_rating(domain, manager, monkeypatch):
    _, svc, _ = domain

    async def scenario():
        session, send, dp, bot = harness(svc)
        await send("/start")
        await send(callback="room:R101")
        await send("Demo Guest")
        assert svc.guest_for_telegram(789123)
        await send(callback="cat:amenities")
        await send(callback="svc:99")
        assert "Select a listed service" in session.sent[-1]
        await send(callback="svc:0")
        original = svc.create_request
        monkeypatch.setattr(
            svc, "create_request", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("Offline"))
        )
        await send("Two towels")
        assert "could not save" in session.sent[-1]
        monkeypatch.setattr(svc, "create_request", original)
        await send("Two towels")
        assert any("has been saved" in s for s in session.sent)
        guest = svc.guest_for_telegram(789123)
        requests = svc.guest_requests(guest["id"])
        assert len(requests) == 1
        rid = requests[0]["id"]
        svc.mutate(rid, manager, 1, status="acknowledged")
        svc.mutate(rid, manager, 2, status="resolved")
        await send("/requests")
        assert rid in session.sent[-1]
        await send("/rate " + rid + " 5")
        assert "rating has been saved" in session.sent[-1]
        await send("/cancel")
        await send(callback="svc:0")
        await dp.storage.close()
        await bot.session.close()

    asyncio.run(scenario())


def test_extended_registration_validates_and_allows_skips(domain):
    _, svc, _ = domain

    async def scenario():
        session, send, dp, bot = harness(svc, extended=True)
        await send("/start")
        await send(callback="room:bad")
        await send(callback="room:R102")
        await send("Demo Guest")
        await send("invalid-date")
        assert "valid date" in session.sent[-1]
        await send("2000-01-01")
        await send("Prefer not to say")
        await send("demo@example.invalid")
        await send("/skip")
        assert svc.guest_for_telegram(789123)["room_id"] == "R102"
        await dp.storage.close()
        await bot.session.close()

    asyncio.run(scenario())
