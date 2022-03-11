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


from driver.core import me_bot, me_user
from driver.queues import QUEUE
from driver.decorators import check_blacklist
from program.utils.inline import menu_markup, stream_markup

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import (
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
    SUDO_USERS,
    OWNER_ID,
)


@Client.on_callback_query(filters.regex("home_start"))
@check_blacklist()
async def start_set(_, query: CallbackQuery):
    await query.answer("الصفحه الرئيسيه")
    await query.edit_message_text(
        f"""✨ **مرحبا عزيزي ↤「 [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) 」!**\n
💭 **انا بوت استطيع تشغيل الموسيقي والفديو في محادثتك الصوتية**

💡 تعلم طريقة تشغيلي واوامر التحكم بي عن طريق  » 📚 الاوامر !

🔖 لتعلم طريقة تشغيلي بمجموعتك اضغط علي » ❓طريقة التفعيل !
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕اضـف الـبـوت لـمـجـمـوعـتـك➕",
                        url=f"https://t.me/USDDBOT?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ طريقة التفعيل", callback_data="user_guide")],
                [
                    InlineKeyboardButton("📚 الاوامر", callback_data="command_list"),
                    InlineKeyboardButton("❤ المطور", url=f"https://t.me/{OWNER_USERNAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 جروب الدعم", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 قناة البوت", url=f"https://t.me/FA9SH"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "𓌹●↯‌•ʙᴏᴛ ѕʜᴀᴅᴏᴡ•↯●𓌺", url="https://t.me/USDDBOT?startgroup=true"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("user_guide"))
@check_blacklist()
async def quick_set(_, query: CallbackQuery):
    await query.answer("طريقة الاستخدام")
    await query.edit_message_text(
        f""" الدليل الأساسي لاستخدام هذا البوت:

 1 ↤ أولاً ، أضفني إلى مجموعتك
 2 ↤ بعد ذلك ، قم بترقيتي كمشرف ومنح جميع الصلاحيات باستثناء الوضع الخفي
 3 ↤ بعد ترقيتي ، اكتب /reload مجموعة لتحديث بيانات المشرفين
 4 ↤ أضف @{ASSISTANT_NAME} إلى مجموعتك أو اكتب /userbotjoin لدعوة حساب المساعد
 5 ↤ قم بتشغيل المكالمة  أولاً قبل البدء في تشغيل الفيديو / الموسيقى
 6 ↤ في بعض الأحيان ، يمكن أن تساعدك إعادة تحميل البوت باستخدام الأمر /reload في إصلاح بعض المشكلات
 📌 إذا لم ينضم البوت إلى المكالمة ، فتأكد من تشغيل المكالمة  بالفعل ، أو اكتب /userbotleave ثم اكتب /userbotjoin مرة أخرى

 💡 إذا كانت لديك أسئلة  حول هذا البوت ، فيمكنك إخبارنا منن خلال قروب الدعم الخاصة بي هنا ↤ @{GROUP_SUPPORT}

⚡ قناة البوت @{UPDATES_CHANNEL}
""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="home_start")]]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("user_guideg"))
@check_blacklist()
async def guide_set(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""❓ How to use this Bot ?, read the Guide below !

1.) First, add this bot to your Group.
2.) Then, promote this bot as administrator on the Group also give all permissions except Anonymous admin.
3.) After promoting this bot, type /reload in Group to update the admin data.
3.) Invite @{me_user.username} to your group or type /userbotjoin to invite her, unfortunately the userbot will joined by itself when you type `/play (song name)` or `/vplay (song name)`.
4.) Turn on/Start the video chat first before start to play video/music.

`- END, EVERYTHING HAS BEEN SETUP -`

📌 If the userbot not joined to video chat, make sure if the video chat already turned on and the userbot in the chat.

💡 If you have a follow-up questions about this bot, you can tell it on my support chat here: @{GROUP_SUPPORT}.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("» Quick use Guide «", callback_data="quick_use")
                ],[
                    InlineKeyboardButton("🔙 Go Back", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("command_list"))
@check_blacklist()
async def commands_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.answer("قائمة الاوامر")
    await query.edit_message_text(
        f"""» **قم بالضغط علي الزر الذي تريده لمعرفه الاوامر لكل فئه منهم !**

⚡ قناة البوت @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👷🏻 اوامر الادمنيه", callback_data="admin_command"),
                    InlineKeyboardButton("🧙🏻 اوامر المطور", callback_data="sudo_command"),
                ],[
                    InlineKeyboardButton("📚 اوامر اساسيه", callback_data="user_command"),
                ],[
                    InlineKeyboardButton("🔙 رجوع", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("user_command"))
@check_blacklist()
async def user_set(_, query: CallbackQuery):
    await query.answer("الاوامر الاساسيه")
    await query.edit_message_text(
        f"""🏮 الاوامر الاساسيه:

» /play +「اسم الأغنية / رابط」لتشغيل اغنيه في المحادثه الصوتيه
» /vplay +「اسم الفيديو / رابط 」 لتشغيل الفيديو داخل المكالمة
» /vstream 「رابط」 تشغيل فيديو مباشر من اليوتيوب
» /playlist 「تظهر لك قائمة التشغيل」
» /end「لإنهاء الموسيقى / الفيديو في الكول」
» /song + 「الاسم تنزيل صوت من youtube」
»/vsong + 「الاسم  تنزيل فيديو من youtube」
» /skip「للتخطي إلى التالي」
» /ping 「إظهار حالة البوت بينغ」
» /uptime 「لعرض مده التشغيل للبوت」
» /alive「اظهار معلومات البوت(في المجموعه)」
⚡ قناة البوت @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("admin_command"))
@check_blacklist()
async def admin_set(_, query: CallbackQuery):
    await query.answer("اوامر الادمنيه")
    await query.edit_message_text(
        f"""🏮 هنا أوامر الادمنيه:

» /pause 「ايقاف التشغيل موقتآ」
» /resume 「استئناف التشغيل」
» /stop「لإيقاف التشغيل」
» /vmute 「لكتم البوت」
» /vunmute 「لرفع الكتم عن البوت」
» /volume 「ضبط مستوئ الصوت」
» /reload「لتحديث البوت و قائمة المشرفين」
» /userbotjoin「لاستدعاء الحساب المساعد」
» /userbotleave「لطرد الحساب المساعد」
⚡ قناة البوت @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("sudo_command"))
@check_blacklist()
async def sudo_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in SUDO_USERS:
        await query.answer("⚠️ هذه الاوامر تخص مطور البوت فقط", show_alert=True)
        return
    await query.answer("sudo commands")
    await query.edit_message_text(
        f"""🏮 هنا اوامر المطور:

» /rmw「لحذف جميع الملفات 」
» /rmd「حذف جميع الملفات المحمله」
» /sysinfo「لمعرفه معلومات السيرفر」
» /update「لتحديث بوتك لاخر نسخه」
» /restart「اعاده تشغيل البوت」
» /leaveall「خروج الحساب المساعد من جميع المجموعات」

⚡ قناة البوت @{UPDATES_CHANNEL}""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("owner_command"))
@check_blacklist()
async def owner_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in OWNER_ID:
        await query.answer("⚠️ You don't have permissions to click this button\n\n» This button is reserved for owner of this bot.", show_alert=True)
        return
    await query.answer("owner commands")
    await query.edit_message_text(
        f"""✏️ Command list for bot owner.

» /gban (`username` or `user_id`) - for global banned people, can be used only in group
» /ungban (`username` or `user_id`) - for un-global banned people, can be used only in group
» /update - update your bot to latest version
» /restart - restart your bot server
» /leaveall - order userbot to leave from all group
» /leavebot (`chat id`) - order bot to leave from the group you specify
» /broadcast (`message`) - send a broadcast message to all groups in bot database
» /broadcast_pin (`message`) - send a broadcast message to all groups in bot database with the chat pin""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("stream_menu_panel"))
@check_blacklist()
async def at_set_markup_menu(_, query: CallbackQuery):
    user_id = query.from_user.id
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.message.from_user.id
    buttons = menu_markup(user_id)
    if chat_id in QUEUE:
        await query.answer("control panel opened")
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("stream_home_panel"))
@check_blacklist()
async def is_set_home_menu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    await query.answer("control panel closed")
    user_id = query.message.from_user.id
    buttons = stream_markup(user_id)
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex("set_close"))
@check_blacklist()
async def on_close_menu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    await query.message.delete()


@Client.on_callback_query(filters.regex("close_panel"))
@check_blacklist()
async def in_close_panel(_, query: CallbackQuery):
    await query.message.delete()
