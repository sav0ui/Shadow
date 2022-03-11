"""
Video + Music Stream Telegram Bot
Copyright (c) 2022-present levina=lab <https://github.com/levina-lab>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/licenses.html>
"""


import traceback

from cache.admins import admins
from driver.core import calls
from pyrogram import Client, filters
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.queues import QUEUE, clear_queue
from driver.filters import command, other_filters
from driver.utils import skip_current_song, skip_item, remove_if_exists
from config import BOT_USERNAME, IMG_5

from driver.database.dbqueue import (
    is_music_playing,
    remove_active_chat,
    music_off,
    music_on,
)
from program.utils.inline import stream_markup, close_mark
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message(command(["reload", f"حديث", "تحديث"]) & other_filters)
@authorized_users_only
@check_blacklist()
async def update_admin(client, message: Message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ تم تحديث قائمة المشرفين بنجاح"
    )


@Client.on_message(
    command(["stop", f"قف", "end", f"انهاء", "نهاء"])
    & other_filters
)
@authorized_users_only
@check_blacklist()
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ **تم ايقاف التشغيل**")
        except Exception as e:
            traceback.print_exc()
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await m.reply("ℹ️ The music is already paused.")
                return
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await m.reply(
                "⏸ **تم ايقاف المسار موقتآ**\n\n• **لٲستئناف البث استخدم**\n» /resume الامر."
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await m.reply("ℹ️ The music is already resumed.")
                return
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await m.reply(
                "▶️ **تم استئناف المسار**\n\n• **لايقاف البث موقتآ استخدم**\n» /pause الامر"
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_message(command(["skip", f"تخطي", "خطي"]) & other_filters)
@authorized_users_only
@check_blacklist()
async def skip(c: Client, m: Message):
    user_id = m.from_user.id
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await c.send_message(chat_id, "❌ **قائمة التشغيل فارغه**")
        elif op == 1:
            await c.send_message(chat_id, "✅ قوائم الانتظار ** فارغة. ** \n\n** • خروج المستخدم من الدردشة الصوتية ** ")
        elif op == 2:
            await c.send_message(chat_id, "🗑️مسح قوائم الانتظار ** \n \n ** • مغادرة المستخدم الآلي للدردشة الصوتية ** ")
        else:
            buttons = stream_markup(user_id)
            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
            thumbnail = f"{IMG_5}"
            title = f"{op[0]}"
            userid = m.from_user.id
            gcname = m.chat.title
            ctitle = await CHAT_TITLE(gcname)
            image = await thumb(thumbnail, title, userid, ctitle)
            await c.send_photo(
                chat_id,
                photo=image,
                reply_markup=InlineKeyboardMarkup(buttons),
                caption=f"⏭ **تم التخطي الئ المسار التالي**\n\n🏷 **الاسم:** [{op[0]}]({op[1]})\n💭 **المجموعة:** `{chat_id}`\n💡 **الحالة:** `شغال`\n🎧 **طلب بواسطة:** {m.from_user.mention()}",
            )
            remove_if_exists(image)
    else:
        skip = m.text.split(None, 1)[1]
        track = "🗑 **تمت إزالة الأغنية من قائمة الانتظار:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    data = await skip_item(chat_id, x)
                    if data == 0:
                        pass
                    else:
                        track = track + "\n" + f"**#{x}** - {data}"
            await m.reply(track)


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await m.reply("ℹ️ The stream userbot is already muted.")
                return
            await calls.mute_stream(chat_id)
            await music_off(chat_id)
            await m.reply(
                "🔇 **تم كتم الصوت**\n\n• **لرفع الكتم استخدم**\n» /unmute الامر" 
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await m.reply("ℹ️ The stream userbot is already unmuted.")
                return
            await calls.unmute_stream(chat_id)
            await music_on(chat_id)
            await m.reply(
                "🔊 **تم رفع الكتم**\n\n• **لكتم الصوت استخدم**\n» /mute الامر"
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_callback_query(filters.regex("set_pause"))
@check_blacklist()
async def cbpause(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer("ℹ️ The music is already paused.", show_alert=True)
                return
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await query.answer("⏸ The music has paused !\n\n» to resume the music click on resume button !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("set_resume"))
@check_blacklist()
async def cbresume(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer("ℹ️ The music is already resumed.", show_alert=True)
                return
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await query.answer("▶️ The music has resumed !\n\n» to pause the music click on pause button !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"🚫 **خزأ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ nothing is currently streaming", show_alert=True)


@Client.on_callback_query(filters.regex("set_stop"))
@check_blacklist()
async def cbstop(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("❌ **قائمة التشغيل فارغه**", reply_markup=close_mark)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("set_mute"))
@check_blacklist()
async def cbmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer("ℹ️ The stream userbot is already muted.", show_alert=True)
                return
            await calls.mute_stream(chat_id)
            await music_off(chat_id)
            await query.answer("🔇 The stream userbot has muted !\n\n» to unmute the userbot click on unmute button !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ nothing is currently streaming", show_alert=True)


@Client.on_callback_query(filters.regex("set_unmute"))
@check_blacklist()
async def cbunmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer("ℹ️ The stream userbot is already unmuted.", show_alert=True)
                return
            await calls.unmute_stream(chat_id)
            await music_on(chat_id)
            await query.answer("🔊 The stream userbot has unmuted !\n\n» to mute the userbot click on mute button !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ nothing is currently streaming", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def change_volume(client, m: Message):
    if len(m.command) < 2:
        await m.reply_text("usage: `/volume` (`0-200`)")
        return
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **volume set to** `{range}`%"
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")
