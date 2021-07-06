import SpeechToText
import BalesIPA
import DataFormatter
import Dash
from datetime import datetime
import speech_recognition as sr

audio_files = ["Paulus.wav", "Dick.wav", "Robro.wav", "Snotgun.wav", "Zandtman.wav"]
# text_file_path = "merged-text/CSGO-Team/merged-text-nbremoved-manual-dupe.csv"
text_file_path = "merged-text/merged-text-file-dupe.csv"


def run_audio_transcriber():
    print("Start Time: ", datetime.now().strftime("%H:%M:%S"))

    # create a speech recognition object
    r = sr.Recognizer()

    for j in range(len(audio_files)):
        SpeechToText.get_large_audio_transcription("audio-data/" + audio_files[j], audio_files[j], r)
    print("End Time: ", datetime.now().strftime("%H:%M:%S"))
    print("DONE")


def run_bales_ipa():
    results = BalesIPA.bales_ipa(text_file_path)
    return results


def run_dashboard(results):
    bales_graph_file_path = DataFormatter.format_bales_graph(results)
    pie_chart_file_path = DataFormatter.format_pie_chart(results)
    bar_chart_file_path = DataFormatter.format_bar_chart(results)
    leader_chart_file_path, leader = DataFormatter.format_leader_chart(results)

    application = Dash.run_dash(bales_graph_file_path, pie_chart_file_path, bar_chart_file_path, leader_chart_file_path, leader)
    return application


print("START")
bales_ipa_results = run_bales_ipa()
app = run_dashboard(bales_ipa_results)
app.run_server(debug=True)
print("DONE")
