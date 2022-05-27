"Name       : Roi Halali & Dor Kershberg        "
"Titel      : Random Signals Prossesing project "
"Sub Titel  : Spider Diagram                    "


#%%
# Libraries:
import os
import glob
import librosa
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import python_speech_features as spf
import shutil



# Functions:

Nj=[]  #number frames of each speaker
Njp=[] #number frames per feachers of each speaker
ejp=[] #Njp/Nj

# reduce list hebrew
k_v = ['k', 'kcl']
t_v = ['t', 'tcl', 'dcl']


def reduce_phonemes_heb(old_phoneme):
    if old_phoneme in k_v:
        return 'k'
    elif old_phoneme in t_v:
        return 't'
    else:
        return old_phoneme


def radar_features(num_speaker, phoneme, start, end):
    # Pre-Process

    count_phonemes_dic = ['b', 'd', 'f', 'g', 'eh', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 'sh', 't', 'th', 'v', 'z',
                          'ch', 'zh', 'iy', 'ae', 'eh', 'uw', 'aa', 'ow']
    features = np.zeros((1, 13))

    num_frames = np.floor((end - start) / (0.02 * 16e03))

    if (num_speaker + 1 == len(Nj)):
        Nj[num_speaker] += num_frames
        Njp[num_speaker] += eval(phoneme) * num_frames

    elif (num_speaker + 1 > len(Nj)):
        Nj.append(num_frames)
        Njp.append(eval(phoneme) * num_frames)


def spyder_diagram(features):
    features_new = np.zeros(len(features) + 1)
    features_new[:13] = features.T
    features_new[len(features_new) - 1] = features_new[0]
    categories = ['Vocalic', 'Consonantal', 'high', 'Back', 'Low', 'Anterior', 'Coronal'
        , 'Round', 'Tense', 'Voice', 'Continuant', 'Nasal', 'Strident', '']

    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(features_new))

    plt.figure(figsize=(40, 20))
    plt.subplot(111, polar=True)
    plt.plot(label_loc, features_new, label='Speaker 0')
    plt.title('Speaker comparison', size=20)
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
    plt.legend()
    plt.show()


#%%
ignore_list_heb = ['ax-h','h#','1', '2','epi','pau','ah','ax','ax_h','ao','aw','axr','ih','ay',
                   'oy','bcl','pcl','dh','el','dx','em','en','eng','ng','er','ey'
                   ,'gcl','hh','hv','ix','jh','nx','uh','ux','w','y'] #irrelevant phonemes

#Hebrew Phonemes
b   = np.array([0,1,0,0,0,1,0,0,0,1,0,0,0],dtype=int)
d   = np.array([0,1,1,0,0,1,1,0,0,1,0,0,0],dtype=int)
f   = np.array([0,1,0,0,0,1,0,0,0,0,1,0,1],dtype=int)
g   = np.array([0,1,0,1,0,0,0,0,0,1,1,0,0],dtype=int)
k   = np.array([0,1,1,1,0,0,0,0,0,0,0,0,0],dtype=int)
# kcl = np.array([0,1,1,1,0,0,0,0,0,0,0,0,0],dtype=int)
l   = np.array([0,1,1,0,0,1,1,0,0,1,1,0,0],dtype=int)
m   = np.array([0,1,0,0,0,1,0,0,0,1,0,1,0],dtype=int)
n   = np.array([0,1,0,0,0,1,0,0,0,1,0,1,0],dtype=int)
p   = np.array([0,1,1,0,0,1,0,0,0,0,0,0,0],dtype=int)
q   = np.array([0,1,0,1,1,0,0,0,0,0,0,0,0],dtype=int)
r   = np.array([1,1,0,0,0,0,1,0,0,1,1,0,0],dtype=int)
s   = np.array([0,1,0,0,0,1,1,0,0,0,1,0,1],dtype=int)
sh  = np.array([0,1,1,0,0,0,1,0,0,0,1,0,1],dtype=int)
t   = np.array([0,1,0,0,0,1,1,0,0,0,0,0,0],dtype=int)
#tcl = np.array([0,1,0,0,0,1,1,0,0,0,0,0,0],dtype=int)
#dcl = np.array([0,1,0,0,0,1,1,0,0,0,0,0,0],dtype=int)
th  = np.array([0,1,0,0,0,1,1,0,0,1,1,0,0],dtype=int)
v   = np.array([0,1,0,0,0,1,0,0,0,1,1,0,1],dtype=int)
z   = np.array([0,1,0,0,0,1,1,0,0,1,1,0,1],dtype=int)# 'חסר כ' סופית,ח' וע

#special
ch  = np.array([0,1,0,1,0,0,1,0,0,0,0,0,1],dtype=int)
zh  = np.array([0,1,1,0,0,0,1,0,0,1,1,0,1],dtype=int)

#vowels
iy  = np.array([0,0,1,0,0,0,0,0,1,1,1,0,0],dtype=int)#'אי
ae  = np.array([1,0,0,0,1,0,0,0,1,1,1,0,0],dtype=int)#'אה
eh  = np.array([0,0,0,0,0,0,0,0,0,1,1,0,0],dtype=int)#'אה
uw  = np.array([1,0,1,1,0,0,0,1,1,1,1,0,0],dtype=int)#'אוו
aa  = np.array([1,0,0,1,1,0,0,0,1,1,1,0,0],dtype=int)#'אאאא
ow  = np.array([1,0,0,1,0,0,0,1,1,1,1,0,0],dtype=int)#'או

# %%
# Dirs & Mode:

train = False
test = False
val = True

# data dirs:
train_data_dir = 'TIMIT/TRAIN/'
test_data_dir = 'TIMIT/TEST/'
val_data_dir = 'TIMIT/EVALUATION/'

# save dirs phonemes
train_save_dir = 'DATA/train/'
test_save_dir = 'DATA/test/'
val_save_dir = 'DATA/evaluation/'

# save dirs speekers
speakers_save_dir = 'DATA/speakers data/'

if train == True:
    data_dir = train_data_dir
    save_dir = train_save_dir

if test == True:
    data_dir = test_data_dir
    save_dir = test_save_dir

if val == True:
    data_dir = val_data_dir
    save_dir = val_save_dir
#%%
#information gathering

i=0
speaker=0
speaker_sentence=0

for phoneme_file in glob.iglob(data_dir + '**', recursive=True):
    if phoneme_file[-3:] == 'PHN':  # check PHN file's from lest three letters

        # set sentence & speeker number:
        if speaker_sentence % 10 == 0 and speaker_sentence != 0:  # new speaker after 10 sentenses
            speaker += 1

            phoneme_speaker_count = np.zeros((26, 1), dtype=int)  # phoneme vector for each sentence
            speaker_sentence = 0
            sentenses_dir = speakers_save_dir + '/' + 'speaker' + str(speaker) + '/'

        speaker_sentence += 1  # sentence number

        # load file:
        wav_file_name = phoneme_file[:-3] + 'WAV.wav'  # changing into wav file
        audio, fs = librosa.core.load(wav_file_name, sr=None)  # load the file from lobrosa

        # pre-processing auidio file:
        audio = librosa.effects.preemphasis(audio)
        audio = audio[1:-1]  # ignore DC
        audio = audio / np.max(np.abs(audio))  # normalization

        with open(phoneme_file) as file:
            lines = file.readlines()  # get rid of \n
        for line in lines:
            splitted_line = line.split(' ')
            phoneme = splitted_line[-1][:-1]

            # if not in ignore list, saving the phoneme
            if phoneme not in ignore_list_heb:
                phoneme = reduce_phonemes_heb(phoneme)
                i += 1

                # radar features gathering:
                end_phone = int(splitted_line[1])
                begin_phon = int(splitted_line[0])
                radar_features(speaker, phoneme, begin_phon, end_phone)

#%%
# %% Radar Diagram
avg_column = []
Njp = np.array(Njp)
u_p = []
for i in range(len(Njp[:, 0])):
    ejp.append(Njp[i] / Nj[i])

for i in range(len(Njp[0, :])):
    u_p.append(sum(Njp[:, i]) / sum(Nj))

ejp = np.array(ejp)
u_p = np.array(u_p)
var_p = []

for i in range(13):
    var_p.append(((sum(ejp[:, i]) - u_p[i]) ** 2) / 13)

for i in range(13):
    ejp[:, i] = ejp[:, i] / np.average(ejp[:, i])

D = []
avg_column = []
for i in range(13):
    D.append(np.sqrt((ejp[:, i] - u_p[i]) ** 2) / var_p[i])
    avg_column.append(np.average(D[i]))
    D[i] = D[i] / avg_column[i]

D = np.array(D)

D = D.T

for i in range(10):
    spyder_diagram(ejp[i])
    
    
