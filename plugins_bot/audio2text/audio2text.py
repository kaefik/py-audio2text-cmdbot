"""
Example plugins for tlgbotcore (send hi)
"""

from telethon import events
from telethon.types import DocumentAttributeFilename

import os
import re
import whisper


# whisper_model = 'tiny' # Very fast and very inaccurate speech recognition
# whisper_model = 'base' # Fast and fourius
# whisper_model = 'small' # Worse than medium but still OK
# whisper_model = 'medium'  # Good recognition results but too slow on CPU
# whisper_model = 'large' # Use on GPU only

# text_language = 'ru'  # Force usage of specified language


async def process_audiofile(event, fname, text_language='ru', whisper_model='medium'):
    """
    функция бфла взята из https://github.com/dimonier/batch-speech-to-text
    """
    fext = fname.split('.')[-1]
    fname_noext = fname[:-(len(fext) + 1)]

    model = whisper.load_model(whisper_model)

    result = model.transcribe(fname, verbose=True, language=text_language)

    fname_timecode = fname_noext + '_timecode.txt'
    fname_txt = fname_noext + '.txt'

    with open(fname_timecode, 'w', encoding='UTF-8') as f:
        for segment in result['segments']:
            timecode_sec = int(segment['start'])
            hh = timecode_sec // 3600
            mm = (timecode_sec % 3600) // 60
            ss = timecode_sec % 60
            timecode = f'[{str(hh).zfill(2)}:{str(mm).zfill(2)}:{str(ss).zfill(2)}]'
            text = segment['text']
            await event.respond(f'{timecode} {text}\n')
            f.write(f'{timecode} {text}\n')

    rawtext = ' '.join([segment['text'].strip() for segment in result['segments']])
    rawtext = re.sub(" +", " ", rawtext)

    alltext = re.sub("([\.\!\?]) ", "\\1\n", rawtext)

    with open(fname_txt, 'w', encoding='UTF-8') as f:
        f.write(alltext)

    return fname_txt, fname_timecode


@tlgbot.on(events.NewMessage(chats=tlgbot.settings.get_all_user_id()))  # , pattern='hi'))
async def handler(event):
    path_audio_files = "audio_files"  # папка куда сохраняется файлы
    # await event.reply('Привет!')
    sender = await event.get_sender()
    # проверка на право доступа к боту
    sender_id = sender.id
    # chat = await event.get_input_chat()
    sender = await event.get_sender()
    sender_id = sender.id
    user_folder = str(sender.id)

    path_audio_files_user = f"{path_audio_files}/{user_folder}"

    if not event.media:
        print("Это не файл, а просто текст ", event.raw_text)
        return

    print("file_document => ", event.media)
    print("mime_type => ", event.document.mime_type)

    audio_mime_type = ['audio/mp4', 'audio/mpeg', 'audio/x-wav', 'audio/aac', 'audio/x-vorbis+ogg']

    if not (event.document.mime_type in audio_mime_type):
        print("Файл не является аудио файлом.")
        return

    # находим атрибут докумета в котором есть имя файла отправленного пользователем
    for el in event.document.attributes:
        if isinstance(el, DocumentAttributeFilename):
            filename_audio = el.file_name

    full_filename = await tlgbot.download_media(event.media, f"{path_audio_files_user}/{filename_audio}")
    print("Path file  = ", full_filename)

    print("BEGIN: Обработка файла")

    result_files = await process_audiofile(event, full_filename, text_language="ru", whisper_model="medium")

    print("Result files => ", result_files)

    await event.respond(file=result_files[0])
    await event.respond(file=result_files[1])

    print("END: Обработка файла")
