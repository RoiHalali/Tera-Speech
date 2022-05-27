"Name       : Roi Halali          "
"Titel      : TIMIT               "
"Subtitel   : phonemas analysis   "

import glob
import os
import librosa
import matplotlib.pyplot as plt
import numpy as np
from librosa import display
import scipy as sp
from scipy import signal
#from python_speech_features import fbank


FRAME_SIZE = 10
HOP_LENGTH = 5

def amplitude_envelope(signal, frame_size=FRAME_SIZE, hop_length=HOP_LENGTH):
    """Calculate the amplitude envelope of a signal with a given frame size nad hop length."""
    amplitude_envelope = []
    
    # calculate amplitude envelope for each frame
    for i in range(0, len(signal), hop_length): 
        amplitude_envelope_current_frame = max(signal[i:i+frame_size])
        amplitude_envelope.append(amplitude_envelope_current_frame)
     
    return np.array(amplitude_envelope)

def mel_filter_bank(N_MelBends,fs,frame_size,stft):
        
    '''
    
    definition:
    mel scale= 2596* log (1+f/700)
    
    f=700(10^(mel/2595)-1) 
      
    algorithem for mel spectogram
    1. Ectract STFT
    2.convert amplitude to DB's
    
    3.convert frequencies to Mel Scale:
        3.1 choose number of mel bands
        3.2 contruct mel filter banks:
            *filter banks shape- (bands,frame size/2 +1)
            3.2.1 convert to mel scale the highest and lowest frequency
            3.2.2 create equaly spased points between
            3.2.3 convert back to frequency
        3.3 apply mel filter banks to spectogram
            *spectogram shape- (frame size/2 +1,frames) 
            multipky spectogram metrix by filter banks metrix
    ''' 
    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (fs / 2) / 700))  # Convert Hz to Mel

    mel_points = np.linspace(low_freq_mel, high_freq_mel, N_MelBends + 2)  # Equally spaced in Mel scale

    hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = np.floor((frame_size + 1) * hz_points / fs)

    fbank = np.zeros((N_MelBends, int(np.floor(frame_size / 2 + 1))))
    for m in range(1, N_MelBends + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])

    #frequency axis for frame STST:
    df = (fs/2)/(frame_size/2)                        #freq. resolution
    fbank_faxis = np.arange(0,(frame_size/2)*df,df)   #freq. axis
    fbank_plot=fbank[:,:-1] 

    #3.3 apply mel filter banks to spectogram:   
    mel_spectogram = np.dot(fbank,stft)
    mel_spectogram = np.where(mel_spectogram == 0, np.finfo(float).eps, mel_spectogram)  # Numerical Stability
    #mel_spectogram = 20 * np.log10(mel_spectogram)  # dB

    return fbank_plot,fbank_faxis,mel_spectogram

def signal_features(Signal,sr):
       
    #LPF:
    LPF = signal.butter(6, 5500,'low', fs=16000, output='sos')
    filtered = signal.sosfilt(LPF,Signal)

    #HPF:
    HPF = signal.butter(3, 400, 'hp', fs=16000, output='sos')
    filtered = signal.sosfilt(HPF, filtered)

    #fft:
    Nsmp=len(filtered)
    Nsmp=2**np.around(np.log2(Nsmp)).astype(int)
    L=np.floor(Nsmp/2).astype(int)
    df = sr/Nsmp                            #freq. resolution
    frequency = np.arange(0,(Nsmp)*df,df)   #freq. axis
    fft = sp.fft.fft(x=filtered,n=Nsmp)    #calculate the spectrum
    fft = sp.fft.fftshift(fft)              #shift the DC to the middle
    PSD=np.abs(fft)                      #magnitude
    #PSD=(PSD/np.max(PSD))
     
    #spectogram:
    frame_size=int(np.floor(16*(10**-3)/(1/sr)))
    hoplen=int(frame_size/2)

    n_fft = int(256)
    stft=librosa.stft(filtered,n_fft=n_fft,win_length=frame_size ,hop_length=hoplen)
    stft=np.abs(stft)

    # normalization:
    stft = (stft - np.min(stft)) / (np.max(stft) - np.min(stft))
    #stft=librosa.amplitude_to_db(np.abs(stft)**2,ref=np.max(stft))
        
    #mel filter bank:
    N_MelBends=40      
    #fbank_plot,fbank_faxis,mel_spectogram=mel_filter_bank(N_MelBends,sr,frame_size,stft )
                   
    #clean the signal + make logable
    PSD_clean=PSD
    for i in range (len(PSD_clean)):
        if PSD_clean[i]<max(PSD_clean)*0.15 :
            PSD_clean[i]=min(PSD_clean)
    
    #calulate envelope:
    env=amplitude_envelope(PSD_clean)
    frames = range(len(env))
    x_env = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)
    L_env=int(np.floor(len(x_env)/2))
    
    #cepstrum method:
    PSD_log=np.log10(PSD) #log of PSD in frequency domain
   
    cepstrum=np.fft.ifft(PSD_log) #cepstrum=IFFT of log(PSD)
    cepstrum=np.absolute(cepstrum)                #magnitude 
    
    
    return    filtered,PSD_clean,frequency,L,stft,hoplen,frame_size,x_env,L_env,env

def analysis(Signal,Signal_Name,sr):
    
    filtered,PSD,frequency,L,stft,hoplen,frame_size,x_env,L_env,env=signal_features(Signal,sr) #Power Spectrum Dencity of signal
    
    with plt.style.context('dark_background'):
        
        plt.figure(figsize=(20,20))
        plt.suptitle(Signal_Name + ' ' + 'anaysis', fontsize=25)

        #original signal:           
        plt.subplot(2, 2, 1)
        plt.plot(filtered,color='c',linewidth=.5,label='Signal')
        plt.title('original signal')
        plt.xlabel('Time [sec]')
        plt.ylabel('Amplitude')
        
        #PSD
        plt.subplot(2, 2, 2)
        plt.plot(frequency[:L],PSD[-L:],color='c',linewidth=.5 ,label='PSD')
        plt.title('PSD')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
                        
        #spectogram
        plt.subplot(2, 2, 3)
        plt.title('Spectogram')
        display.specshow(stft,sr=sr,x_axis='time',y_axis='linear',hop_length=hoplen,win_length=frame_size,fmax=int(5500))
        plt.colorbar(format="%+2.f")

        # #mel filter benk
        # plt.subplot(2, 2, 5)
        # plt.title('mel filter benk')
        # plt.plot(fbank_faxis,fbank_plot.T)
        # plt.title('mel filter banks on frequency domain')
        # plt.xlabel('frequency [Hz]')
        # plt.ylabel('Amplitude')
        
        # #mel spectogram
        # plt.subplot(3, 2, 6)
        # plt.title('Mel Spectogram')
        # plt.matshow(mel_spectogram,fignum=0)
        
        
        #envelop:
        plt.subplot(2, 2, 4)
        plt.plot(x_env[:L_env],env[-L_env:],color='c' ,label='envelop')
        plt.title('Envelop')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel(' Amplitude')

        # #log scale:
        # plt.subplot(3, 2, 4)
        # plt.plot(t_env[:L_env],PSD_log[:L_env],color='c',LineWidth=.5 ,label='PSD log')
        # plt.xlabel('time [ms]')
        # plt.ylabel(' Amplitude')
        # plt.legend()        
        # #cepstrum
        # plt.subplot(3, 2, 5)
        # plt.plot(t_env[:L_env],cepstrum[:L_env],color='c',LineWidth=.5 ,label='cepstrum')
        # plt.xlabel('time [ms]')
        # plt.ylabel(' Amplitude')
        # plt.legend()
               
    plt.show()

"specific analysis:"
# #load the file from lobrosa
# wav_file_name="TIMIT/TRAIN/FAEM0/SA1.WAV"
# audio, sr = librosa.core.load(wav_file_name,sr=None)
#
# audio = audio/np.max(np.absolute(audio))
#
# analysis(audio,"Audio",sr) #ploting signal information
#
# #get phonema file
# phonemes_file="TIMIT/TRAIN/FAEM0/SA1.PHN"
#
# with open(phonemes_file) as f:
#     lines = f.readlines() # get rid of \n
#
#     #phonema information :
#     for line in lines:
#
#         splitted_line = line.split(' ')
#         phonema_name = splitted_line[-1][:-1]
#
#         end_phone = int(splitted_line[1])
#         begin_phon = int(splitted_line[0])
#         phonema_length = end_phone - begin_phon + 1
#
#         phonema=audio[begin_phon:end_phone]
#         if phonema_name in vowels_list :
#             analysis(phonema,phonema_name,sr) #ploting information


"phonemas analysis:"
data_dir="TIMIT/PREDICTION/"
sr=16000

for phoneme_file in glob.iglob(data_dir + '**', recursive=True):
    if phoneme_file[-3:] == 'wav':
        # load file:
        wav_file_name = phoneme_file[:-3]+'wav'  # changing into wav file
        audio, fs = librosa.core.load(wav_file_name, sr=None)  # load the file from librosa

        # pre-processing auidio file:
        audio = librosa.effects.preemphasis(audio)

        with open(phoneme_file) as file:
            lines = file.readlines()  # get rid of \n
        for line in lines:
            splitted_line = line.split(' ')
            phonema_name = splitted_line[-1][:-1]

            # if not in ignore list, saving the phoneme
            vowels_list = ["ow"]
            if phonema_name in vowels_list:
                print(wav_file_name)
                # phonema length
                end_phone = int(splitted_line[1])
                begin_phon = int(splitted_line[0])

                # fixed phoneme len:
                target_sr = 16000  # note: The sample rate used for audio for TIMIT is 16000.
                phoneme_fixed_len = int(0.03 * target_sr)  # note: (mel window length)*(semple rate)=phonema length
                phon_len = end_phone - begin_phon

                # take missing samples from adjacent samples
                if phon_len < phoneme_fixed_len:
                    continue

                samples_start = audio[begin_phon:begin_phon + phoneme_fixed_len]
                #samples_start=samples_start/np.max(np.abs(samples_start))  # normalization

                analysis(samples_start,phonema_name,sr) #ploting signal information


"mathematics signal analysis:"

# fs = 16000    #sampling freq.
# Ts=1/fs
# Nsmp = 550   #No. of samples
# L=int(Nsmp/2)

# f1 = 4000     #even freq.
# f2 = 2000     #odd freq.
# A1 = 1      #amplitude
# A2 = 1      #amplitude

# n = np.arange(0,Nsmp*Ts, Ts)    #time
# x = A1*np.sin(2*np.pi*f1*n)+A2*np.sin(2*np.pi*f2*n)  #signal

# analysis(x,"random signal",fs) #ploting signal information





















