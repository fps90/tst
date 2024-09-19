from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.stream import AudioStream  # استبدال AudioPiped بـ AudioStream
from yt_dlp import YoutubeDL

# إعدادات العميل
api_id = "8934899"
api_hash = "bf3e98d2c351e4ad06946b4897374a1e"
session_string = "BACIVfMATb0BpsmMaPEORGdSRUC7zt71hM2llM8JduJHCre9PsZyM9VpxQaFxcq0xppAb7CeQW4-GksJzmpguSOzfWebdjpJgmJwKKyYsLvaZZOapToKH_uHf_tB8fhqXcKqCFgz13LbXAiJEbcg-LKzvfo5_QilONL7X9FMvgO9l7qH5XgXcHQ0pno8X-JUuKz2GClkxbJJgzVQWkKoAIloMuZcheqzryVReW2PveG8I3lBhfb-0kGb1OryW9Av7W7cT1D-Jp7Yp6kw0hAAalV1FfpfQ2s7uOSZUbrvuhK11XopNXjX5Rkp5Hb3igmTv0VhT8rHszPnRSsVM1GihmiOyvroNgAAAAGTF-IEAA"

app = Client("my_account", api_id=api_id, api_hash=api_hash, session_string=session_string)
call = PyTgCalls(app)

# إعداد yt-dlp لتحميل الصوت من يوتيوب
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# عند استقبال مكالمة، قبولها وتشغيل أغنية
@app.on_call
async def handle_call(_, update):
    chat_id = update.chat.id
    await call.accept(update)
    
    # تنزيل الأغنية من يوتيوب
    song_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # ضع هنا رابط الأغنية العشوائي أو المُدخل
    audio_file = download_audio(song_url)
    
    # تشغيل الصوت في المكالمة
    await call.start_audio(chat_id, AudioStream(audio_file))

    print(f"Started playing {audio_file} in call with {chat_id}")

app.start()
call.run()
