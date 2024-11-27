from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

mp3_fp = BytesIO()
tts = gTTS('안녕하세요', lang='ko')
tts.write_to_fp(mp3_fp)
mp3_fp.seek(0)
audio = AudioSegment.from_file(mp3_fp, format='mp3')
play(audio)
