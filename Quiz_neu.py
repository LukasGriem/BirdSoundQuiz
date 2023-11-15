import time
from random import randint
import requests
import matplotlib.pyplot as plt
import pandas as pd
import vlc
from PIL import Image
import urllib.request
import getpass
import librosa
import numpy as np
from pydub import AudioSegment
import pygame
import os

AudioSegment.converter = r"D:\Lukas_data\Private\Python_R_Shortcuts\Quiz_Alle_Arten\ffmpeg.exe"
AudioSegment.converter = r"D:\Lukas_data\Private\Python_R_Shortcuts\Quiz_Alle_Arten\\ffmpeg.exe"

def settings_question():
    Select_Settings = input("Hi! Would you like to select new Settings? (type yes or no): ")
    if Select_Settings == "yes":
        Spec_Num = select_species()
        select_audio_settings()
    else:
        File = open('First.txt', 'rt')
        File2 = File.read()
        Spec_Num = File2.count('+')
    return Spec_Num

def select_species():
    Spec_Num = int(input("Select number of species to practice: "))
    output_file = open('First.txt', 'w')
    for i in range(0,Spec_Num):
            Species_Deu = input("Insert species "+ str(i+1) + " (Deutscher Artname): ")
            df = pd.read_csv('Europ_Species.csv')
            for i, a in zip(df['Wissenschaftlich'], df['Deutsch']):
                if a == Species_Deu:
                    Species_Ltn = i
            output_file.write(Species_Ltn + ',')
    output_file.close()
    return Spec_Num

def select_audio_settings():
    output_file = open('Second.txt', 'w')
    Type = input("Practice song or call? ")
    output_file.write(Type)
    output_file.close()

    output_file = open('Third.txt', 'w')
    Sex = input("Male or female? ")
    output_file.write(Sex)
    output_file.close()


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
    return(d)

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
