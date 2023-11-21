##Einladen der benötigten Bibliotheken
##Wird jede einzelne benötigt und wenn ja, warum?
import time
from random import randint
import requests
import matplotlib.pyplot as plt
##Pandas als CSV-Tabellen-Einlademodul
import pandas as pd
from PIL import Image
import urllib.request
import getpass
import librosa
import numpy as np
from pydub import AudioSegment
import pygame
## OS für plattformunabhängige Dateipfade
import os

## Der AudioSegmentConverter (ASC) wandelt die Rufe in Spektrogramme um?
## Warum doppelte Variablendefinition? Würde Dopplung streichen.
AudioSegment.converter = r"D:\Lukas_data\Private\Python_R_Shortcuts\Quiz_Alle_Arten\ffmpeg.exe"
AudioSegment.converter = r"D:\Lukas_data\Private\Python_R_Shortcuts\Quiz_Alle_Arten\\ffmpeg.exe"

## Definieren der Optionseinstellungen
## Änderungen beibehalten mittels folgender Funktion:
def settings_question():
    Select_Settings = input("Hi! Would you like to select new Settings? (type yes or no): ")
    if Select_Settings == "yes":
        Spec_Num = select_species()
        select_audio_settings()
## Wenn "no", dann Einladen der verfügbaren Species-IDs
## Ich verstehe zwar, dass eine neue Settingsdatei ("First.txt", im Lesemodus) geöffnet wird, aber was macht File2? Es zeigt letztlich auf sich selbst (nirgends anders im Code erwähnt)?
    else:
        File = open('First.txt', 'rt')
        File2 = File.read()
        Spec_Num = File2.count('+')
    return Spec_Num

## Auswahl der zu übenden Spezies:
## Wie wird mit mehrfacher Eingabe umgegangen (Trennung per Komma, Punkt oder Semikolon)? Ist sie prinzipiell vorgesehen (potenzielle Fehlerquelle bei Eingabe)?
def select_species():
    Spec_Num = int(input("Select number of species to practice: "))
    ## Öffnen der Settingsdatei "First.txt" im Schreibmodus
    output_file = open('First.txt', 'w')
    for i in range(0,Spec_Num):
            Species_Deu = input("Insert species "+ str(i+1) + " (Deutscher Artname): ")
            ##Erstellen eines Dataframes (df), der mittels Pandas folgende csv-Datei öffnet (für ID-Hinterlegung)
            df = pd.read_csv('Europ_Species.csv')
            for i, a in zip(df['Wissenschaftlich'], df['Deutsch']):
                if a == Species_Deu:
                    Species_Ltn = i
                    ## An der Stelle wäre es sinnvoll, noch eine Fehlerausgabe bei falscher Schreibweise zu implementieren
            ## Wenn ich diesen Codeblock richtig verstehe, funktioniert nur die Eingabe des deutschen Artnamens (Verweis auf ID über Feld "Wissenschaftlich" nicht möglich? Wenn ja wieso nicht?)? UPDATE: siehe Zeile 89
            output_file.write(Species_Ltn + ',')
    output_file.close()
    return Spec_Num

## Funktion zur Auswahl der Audio (Ruf oder Lied)
def select_audio_settings():
    output_file = open('Second.txt', 'w')
    Type = input("Practice song or call? ")
    ##Auswahl wird in Audiosettingsdatei "Second.txt" geschrieben, ABER: Fehlt hier nicht analog zu settings_question eine Schleife, grob etwa so:
    #if Type == "song":
    # Type = Type_song in <Hier wird ein Auswahlkriterium in Xenocanto für Song/Call benötigt; welches bietet sich da an?>
    #Analog für if Type == "call":
    # Type = Type_call in <...>
    output_file.write(Type)
    output_file.close()
##Selbes Problem in Audiosettingsdatei für Geschlecht "Third.txt":
    output_file = open('Third.txt', 'w')
    Sex = input("Male or female? ")
    output_file.write(Sex)
    output_file.close()

## Hauptfunktion zum Abrufen der Audiodaten von Xenocanto mittels Überführung der bisherigen Settingsdateien in die URL
def load_species_data(Spec_Num):
    d = {}
    with open('First.txt', 'rt') as myfile:
        Settings = myfile.read().split(',')
    with open('Second.txt', 'rt') as myfile:
        Type = myfile.read()
    with open('Third.txt', 'rt') as myfile:
        Sex = myfile.read()
    for a in range(1,Spec_Num+1):
        Species = Settings[a-1]
        url = "https://www.xeno-canto.org/api/2/recordings?query=" + Species + "+type:" + Type  #+ "+sex:" + Sex
        d["Species {0}".format(a)] = requests.get(url).json()
    ## Was genau wird hier zurückgegeben? Eine .json-Datei? Was macht sie?
    return(d)

## Hier gibt es also doch eine Funktion, die die Eingabe von "Wissenschaftlich" ermöglicht. Die würde ich oben direkt nach select_species einfügen? Oder spricht etwas dagegen?
## Ich verstehe nur nicht, wieso d2 nur hier erwähnt wird - das dürfte dann nicht funktionieren beim Ausführen des Codes? Oder was sind deine bisherigen Erfahrungen zur Eingabe der wiss. Artnamen?
def define_species_list(Spec_Num):
    d2 = {}
    with open('First.txt', 'rt') as myfile:
        Settings = myfile.read().split(',')
    for b in range(1, Spec_Num+1):
        Species_Ltn = Settings[b-1]
        df = pd.read_csv('Europ_Species.csv')
        for i, a in zip(df['Deutsch'], df['Wissenschaftlich']):
            if a == Species_Ltn:
                Species_Deu = i
        d2["Species {0}".format(b)] = Species_Deu
    return(d2)

## Ist die folgende Funtkion für die Auswahl einer zufälligen Audiodatei zur gewählten Spezies in Xenocanto zuständig oder wählt sie sowohl Audiosample als auch Spezies zufällig aus?
## Müsste in Zeile 107 nicht auch d2 inkludiert werden bzw ein d OR d2 Statement?
def select_random_species(d, Spec_Num):
    Random_species = "Species " + str(randint(1,Spec_Num))
    json_data = d[Random_species]
    recordings = json_data['recordings']
    Length = len(recordings)
    recording = recordings[randint(0, Length-1)]
    audio_url = recording['file']
    # download file
    response = requests.get(audio_url)
    with open("audio_file.mp3", "wb") as f:
       f.write(response.content)
    # load file and convert to wav
    duration = 10
    mp3 = 'audio_file.mp3'
    wav = "audio.wav"
    #time.sleep(2)
    sound = AudioSegment.from_mp3(mp3)
    sound.export(wav, format="wav")

## Initialisieren des Pygame-Moduls:
## Wie soll das Spiel aufgebaut sein? Die Endbedingung ist offenbar eine bestimmte Punktzahl zu erreichen (0 oder 999?)
    pygame.mixer.init()
    pygame.mixer.music.load(wav)
    pygame.mixer.music.play()

    # load as spectrogramme
    audio_data, sample_rate = librosa.load(wav, sr=None)
    num_samples = int(sample_rate * duration)
    audio_data = audio_data[:num_samples]
    spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate,  fmin=110, fmax=10000)
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    # plot file
    plt.figure(figsize=(10, 5))
    plt.imshow(log_spectrogram, aspect='auto', origin='lower', cmap='viridis')
    plt.show()
    return(Random_species)

## Welche Eingabe muss erfolgen für "Right!" - nur die korrekte ID? Aber die weiß der Nutzende ja nicht? Außerdem ist Übung ja bissl pointless, wenn in Settings vorher Spezies X gewünscht wird (außer bei sehr variablen Arten)?
## Generell verstehe ich die "Spielregeln" noch nicht; bitte um Protokollierung des verbleibenden Codes!
def Right_False(Score, Negative_Score, Ending):
    if int(True_Species[-1]) == int(Answer):
        print("Right!")
        Score += 1
    elif 99 == int(Answer):
        print("skipped")
    elif 999 == int(Answer):
        Ending = input("Are you sure? Write end: ")
    else:
        print("False!")
        print("Right answer was " + str(True_Species))
        Negative_Score += 1
    input("End audio?")
    pygame.mixer.music.stop()
    pygame.quit()
    os.remove("audio_file.mp3")
    os.remove("audio.wav")
    return(Score, Negative_Score, Ending)


def assesment(Score, Negative_Score):
    Labels = ['Right', 'Wrong']
    Colors = ['green', 'red']
    Scores = [Score, Negative_Score]
    plt.pie(Scores, colors = Colors)
    plt.legend(Labels, loc="best")
    plt.show()
    input("Press Key to end")


###########################################
#Preparation
print("Loading Program...")
#driver = webdriver.Firefox(executable_path="D:\Lukas Dateien\Krimskrams\geckodriver-v0.29.1-win64\geckodriver.exe")
#driver.minimize_window()


#Settings
Spec_Num = settings_question()
print("Loading species data...")
Species_data = load_species_data(Spec_Num)
Species_names = define_species_list(Spec_Num)


#Game
Score = 0
Negative_Score = 0
Ending = "NULL"
while Ending != "end":
    True_Species = select_random_species(Species_data, Spec_Num)
    Answer = input(str(Species_names) + ', insert species-number or "99" to skip or "999" to end: ')
    Score, Negative_Score, Ending = Right_False(Score, Negative_Score, Ending)
    #Score = Scores[0]
    #Negative_Score = Scores[1]
    print(str(Score)+" right answers!")

#End
assesment(Score, Negative_Score)

print("The End")
