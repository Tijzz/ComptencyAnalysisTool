# importing libraries
import speech_recognition as sr
import os
import csv
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
from datetime import datetime
from playsound import playsound


# Adjust target amplitude
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path, filename, r):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using Pydub
    sound = AudioSegment.from_wav(path)
    # normalize audio_segment to -20dBFS
    normalized_sound = match_target_amplitude(sound, -10.0)
    print("Length of audio_segment = {} seconds".format(len(normalized_sound) / 1000))

    # Print detected non-silent chunks, which in our case would be spoken words.
    timestamp_chunks = detect_nonsilent(normalized_sound, min_silence_len=500, silence_thresh=-33, seek_step=1)
    print(timestamp_chunks)
    # Convert ms to seconds
    timestamps = []
    for timestamp_chunk in timestamp_chunks:
        timestamps.append([timestamp__single_chunk / 1000 for timestamp__single_chunk in timestamp_chunk])
    print(timestamps)
    print("Finished timestamps:", filename, datetime.now().strftime("%H:%M:%S"))

    folder_name = "chunks-" + filename
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""

    text_folder_name = "text-translation"
    if not os.path.isdir(text_folder_name):
        os.mkdir(text_folder_name)
    if not os.path.isfile("text-translation/translation_file.csv"):
        open("text-translation/translation_file.csv", "x")
    text_file = open("text-translation/translation_file.csv", 'a', newline='')
    csv_writer = csv.writer(text_file)

    # print("Amount of chunks:", len(chunks))
    print("TIMESTAMPS LIST LENGTH", len(timestamps))
    # Process each chunk
    for i, audio_chunk in enumerate(timestamps):
        # Export audio chunk and save it in the `folder_name` directory.
        audio = sound[audio_chunk[0]*1000:(audio_chunk[1]+0.5)*1000]
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        # audio.export(chunk_filename, format="wav")
        audio.export(chunk_filename, format="wav")
        playsound(chunk_filename)
        # Recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                # print("Error:", str(e))
                while True:
                    text = str(input())
                    if text == "r":
                        playsound(chunk_filename)
                    else:
                        break
                csv_writer.writerow([text, [timestamps[i], path]])
            else:
                text = f"{text.capitalize()}. "
                while True:
                    text = str(input())
                    if text == "r":
                        playsound(chunk_filename)
                    else:
                        break
                csv_writer.writerow([text, [timestamps[i - 1], path]])
                # print(chunk_filename, ":", text)
                whole_text += text
        print("Finished chunk:", i)
    # Return the text for all chunks detected
    return whole_text
