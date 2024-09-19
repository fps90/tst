from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import yt_dlp
import random

# بيانات الحساب
api_id = "8934899"
api_hash = "bf3e98d2c351e4ad06946b4897374a1e"
session_string = "BACIVfMATb0BpsmMaPEORGdSRUC7zt71hM2llM8JduJHCre9PsZyM9VpxQaFxcq0xppAb7CeQW4-GksJzmpguSOzfWebdjpJgmJwKKyYsLvaZZOapToKH_uHf_tB8fhqXcKqCFgz13LbXAiJEbcg-LKzvfo5_QilONL7X9FMvgO9l7qH5XgXcHQ0pno8X-JUuKz2GClkxbJJgzVQWkKoAIloMuZcheqzryVReW2PveG8I3lBhfb-0kGb1OryW9Av7W7cT1D-Jp7Yp6kw0hAAalV1FfpfQ2s7uOSZUbrvuhK11XopNXjX5Rkp5Hb3igmTv0VhT8rHszPnRSsVM1GihmiOyvroNgAAAAGTF-IEAA"

# إنشاء التطبيق
app = Client("my_account", api_id=api_id, api_hash=api_hash, session_string=session_string)
call_app = PyTgCalls(app)

# دالة لتحميل وتشغيل الأغنية من YouTube
def get_song_url(song_name):
    query = f"ytsearch:{song_name}"
    with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
        info_dict = ydl.extract_info(query, download=False)
        audio_url = info_dict['entries'][0]['url']
    return audio_url

# قبول المكالمة
@app.on_call(filters.incoming)
async def handle_call(client, call):
    await call.accept()  # قبول المكالمة
    await client.send_message(call.chat.id, "تم قبول المكالمة! يمكنك الآن طلب أغنية عبر إرسال 'تشغيل [اسم الأغنية]'.")

# تنفيذ طلب تشغيل الأغنية
@app.on_message(filters.private & filters.regex(r'^تشغيل (.+)'))
async def play_song(client, message: Message):
    song_name = message.matches[0].group(1)
    audio_url = get_song_url(song_name)  # البحث عن الأغنية
    await client.send_message(message.chat.id, f"جاري تشغيل الأغنية: {song_name}")
    
    # التأكد من وجود مكالمة حالياً
    if call_app.active_calls:
        call = list(call_app.active_calls.values())[0]  # جلب أول مكالمة نشطة
        await call_app.change_stream(call.chat_id, AudioPiped(audio_url))  # تغيير الأغنية التي يتم تشغيلها

# بدء التطبيق
app.start()
call_app.start()

print("Bot is running...")
app.idle()  # استمرارية التطبيق
