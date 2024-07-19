import numpy as np
from pydub import AudioSegment
import random
import librosa
import os
from pathlib import Path
from scipy.io import wavfile
from PIL import Image, ImageOps
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def converter(mp3_path):
    if '.mp3' in mp3_path:
        mp3_audio = AudioSegment.from_mp3(mp3_path)
        wav_path = Path(mp3_path).with_suffix(".wav")
        wav_file = mp3_audio.export(wav_path, format="wav")
    elif '.wav' in mp3_path: # just in case some files are wav, not mp3
        wav_path = mp3_path

    sr, audio = wavfile.read(wav_path)

    audio = audio / 32768.0

    # scaled_audio = np.int16(audio / np.max(np.abs(audio)) * 32767)

    return sr, audio


def multithreading_sampling(
    mp3_path,
    output_path,
    num_samples_per_song,
    sample_duration=5,
    y_parameter=250,
    max_workers=4,
    min_db=-80,
):

    """
    Intended for more efficient sampling; rather than cropping the array and then generating the spectrogram, generates one large spectrogram and crops the image afterwards
    """
    sr, array = converter(mp3_path)
    if len(array.shape) > 1:
        array = array[:, 0]

    # now, generating the image array
    print("currently working directory is", os.getcwd())
    D = librosa.stft(array)
    print("stft success. Now converting amplitude to decibel.")
    img_array = librosa.amplitude_to_db(np.abs(D), ref=np.max) # img height is always 1025
    img_array = img_array[0:y_parameter, :][::-1,] # cutting down array to relevant data and then flipping it

    # scale the array to 0-255
    img_arr = (img_array / min_db * 255).astype(np.uint8) # uint8 - u avoids negatives
    # img_arr = (img_array - min_db * 255/abs(min_db)).astype(np.uint8)

    duration_seconds = len(array)/sr
    x_pixel_per_second = img_arr.shape[1] / duration_seconds

    sample_window = int(x_pixel_per_second * sample_duration)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        # submit the jobs to run
        for i in tqdm(range(0, num_samples_per_song), desc="Submitting tasks"):
            if '.mp3' in mp3_path:
                save_path = output_path.replace('.mp3', f'{i}' + '.png')
            elif '.wav' in mp3_path:
                save_path = output_path.replace('.wav', f'{i}' + '.png')

            futures.append(
                executor.submit(
                    sample_random_sample_worker,
                    img_arr=img_arr,
                    sample_window=sample_window,
                    save_path=save_path,
                    image_size=(256,256),
                )
            )

    # execute and collect results from jobs
        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc="Collecting results"):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                pass # print(e)
        if len(results) != len(futures):
            raise ValueError("Not all threads finished successfully!")


def sample_random_sample_worker(
    img_arr: np.ndarray,
    sample_window: int,
    save_path: str,
    image_size=(256, 256),
):
    start = random.randint(0, img_arr.shape[1] - sample_window)
    sample = img_arr[:, start:start + sample_window]

    if np.mean(img_arr) < 240:  # data validation - white should be silence
        image = Image.fromarray(sample)

        image = image.resize(image_size, resample=Image.BICUBIC) #turn it into a square

        image.save(save_path)
        return True


def multithreading_stft_test(
        mp3_path,
        max_workers=4
):
    '''
    Intended to test if STFT can be done in a multithreaded environment.
    '''
    sr, array = converter(mp3_path)
    if len(array.shape) > 1:
        array = array[:, 0]

    chunk_size = len(array) // max_workers

    # Define a worker function to perform STFT on a chunk
    def stft_worker(chunk):
        return librosa.stft(chunk)

    # Split the audio array into chunks
    chunks = [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]

    # Use ThreadPoolExecutor to run STFT on each chunk
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(stft_worker, chunk) for chunk in chunks]

        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc="Collecting results"):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(e)
                pass
        if len(results) != len(futures):
            raise ValueError("Not all threads finished successfully!")