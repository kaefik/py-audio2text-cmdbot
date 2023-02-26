# py-audio2text-cmdbot
audio recognition to text file

при отправке аудио файла боту, бот скачивает в папку audio_files/id_user 
и запускает процесс распознавания текста. Результат распознования сохраняется с тем же именем входного файла 
просто расшифровка (имя_файла.txt) и расшифровка с тайм комами (имя_файла_timecode.txt), 
также эти текстовые файлы отправляются пользователю. 

# Установка библиотек 

```bash
pip3 install telethon
pip install -U openai-whisper
sudo apt update && sudo apt install ffmpeg
```

[Whisper](https://github.com/openai/whisper) is a general-purpose speech recognition model. 
It is trained on a large dataset of diverse audio and is also a multi-task model that 
can perform multilingual speech recognition as well as speech translation and language identification.

