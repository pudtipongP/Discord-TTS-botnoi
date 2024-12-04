### Discord Text-to-Speech (TTS) Bot Documentation

This document describes the functionality of a Discord bot that listens for messages, converts them into speech using the Botnoi Text-to-Speech (TTS) API, and plays the generated audio in a voice channel.

---

### **Bot Features**

- **Text-to-Speech (TTS)**: Converts messages from Discord channels into audio using the Botnoi TTS API. The bot supports multiple languages and speakers.
  
- **Voice Channel Integration**: The bot can join and speak in voice channels, providing a seamless integration for TTS in voice chats.

- **Customizable Speaker**: The bot allows users to choose different speakers for the TTS output by including the speaker ID in the message (e.g., `message%speaker_id`).

- **Error Handling**: If the message cannot be converted to speech, the bot will log an error message, ensuring easy troubleshooting.

---

### **How It Works**

1. **Receive Message**: The bot listens for messages in Discord channels. If the message comes from a channel where TTS is enabled (e.g., channel named 'tts' or specific channel IDs), it triggers the TTS functionality.

2. **Process Message**: The bot checks if the user is in a voice channel. If so, it proceeds to convert the message into speech using the Botnoi API. If the user is not in a voice channel, the bot asks the user to join one.

3. **TTS API**: The bot sends the message content to the Botnoi API to generate the audio file. The API supports Thai language and multiple speakers. The audio is returned as a URL, which the bot downloads.

4. **Play Audio**: Once the audio file is downloaded, the bot connects to the voice channel and plays the audio using Discord's `FFmpegPCMAudio` feature. If the bot is already playing audio, it waits until the current audio finishes before playing the new one.

5. **Bot Commands**:
   - `!join`: Command to make the bot join the user's voice channel.
   - `!play <url>`: Command to play a provided audio URL.
   - `!stop`: Stops the currently playing audio.
   - `!leave`: Command to disconnect the bot from the voice channel.

---

### **Bot Code Breakdown**

1. **Bot Initialization**:
   - The bot is created using the `discord.py` library with `Intents` enabled for message reception.
   - A command prefix of `!` is used for bot commands.
   
   ```python
   intents = discord.Intents.all()  # Enable all intents
   bot = commands.Bot(command_prefix='!', intents=intents)
   ```

2. **TTS API Request**:
   - The bot sends a POST request to the Botnoi API with the text to be converted into speech, specifying the language, speaker, volume, and speed.
   
   ```python
   url = "https://api-voice.botnoi.ai/openapi/v1/generate_audio"
   headers = {
       'Botnoi-Token': 'YOUR_BOTNOI_API_KEY',  # Replace with your Botnoi API token
       'Content-Type': 'application/json'
   }
   ```

3. **Message Handling**:
   - The `on_message` event listens for messages from users. If the message is from a specific channel, it processes the message for TTS conversion.
   
   ```python
   @bot.event
   async def on_message(message):
       if message.author == bot.user:
           return

       if message.channel.name == 'tts' or message.channel.id == 988359881931239455:
           if message.author.voice:
               channel = message.author.voice.channel
               await create_v(message.content, channel)
           else:
               await message.channel.send("Please join a voice channel first.")
       await bot.process_commands(message)  # Process commands after custom message handling
   ```

4. **Voice Channel Interaction**:
   - The bot checks if the user is in a voice channel and joins if not already connected.
   
   ```python
   @bot.command()
   async def join(ctx):
       if ctx.author.voice:
           channel = ctx.author.voice.channel
           await channel.connect()
           await ctx.send(f"Joined {channel.name}")
       else:
           await ctx.send("You need to join a voice channel first.")
   ```

5. **TTS Playback**:
   - The `create_v` function downloads the generated speech audio and plays it in the voice channel using `FFmpegPCMAudio`.
   
   ```python
   async def create_v(message, channel):
       # Prepare the message and speaker parameters
       response = requests.post(url, headers=headers, json=payload)
       rr = response.json()

       if 'message' not in rr and rr['point'] != 0:
           file_name = rr['audio_url']
           urllib.request.urlretrieve(file_name, f'test.mp3')
           
           voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
           if voice_client is None:
               voice_client = await channel.connect()

           if not voice_client.is_playing():
               voice_client.play(discord.FFmpegPCMAudio(f'test.mp3'), after=lambda e: print('done', e))
   ```

---

### **Bot Commands**
1. **`!join`**: Makes the bot join the user's voice channel.
2. **`!play <url>`**: Plays the audio at the provided URL.
3. **`!stop`**: Stops any currently playing audio.
4. **`!leave`**: Disconnects the bot from the voice channel.

---

### **Deployment Instructions**
1. **Install Dependencies**:
   - Install the necessary libraries with `pip`:
     ```bash
     pip install discord.py requests
     ```

2. **FFmpeg Installation**:
   - Ensure that **FFmpeg** is installed and accessible in the system PATH to play audio files.
   - Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html).

3. **Run the Bot**:
   - Replace the Botnoi API token in the `headers` dictionary with your own API key.
   - Run the bot by executing the script in a Python environment:
     ```bash
     python bot_script.py
     ```

---

### **Final Notes**
- The bot uses **FFmpeg** to play audio and requires access to a voice channel to function.
- The bot currently supports Thai language TTS but can be extended to support more languages by adjusting the payload sent to the Botnoi API.
