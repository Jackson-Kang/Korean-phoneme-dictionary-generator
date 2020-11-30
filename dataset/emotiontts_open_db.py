from utils import copy_file, get_path, create_dir, do_multiprocessing
from utils import create_phoneme_dictionary, write_phoneme_dictionary, write_multispeaker_emotion_metadata

import glob

class EmotionTTS_OpenDB():

	def __init__(self, source_dataset_path, savepath, savepath_wavs, metadata_savepath, phoneme_dictionary_savepath, num_threads):
		self.source_dataset_path = source_dataset_path
		self.savepath = savepath
		self.savepath_wavs = savepath_wavs
		self.metadata_savepath = metadata_savepath
		self.phoneme_dictionary_savepath = phoneme_dictionary_savepath
		self.num_threads = num_threads


	def job(self, filepath):
		source_transcript_filepath, source_wav_filepath = filepath

		target_transcript_filepath = source_transcript_filepath.split("/")[-1]
		target_wav_filepath = source_wav_filepath.split("/")[-1]		

		dest_transcript_filepath = get_path(self.savepath, target_transcript_filepath[:3], target_transcript_filepath.replace("txt", "lab"))
		dest_wav_and_lab_filepath = get_path(self.savepath, target_wav_filepath[:3], target_wav_filepath)	
		dest_wav_filepath = get_path(self.savepath_wavs, target_wav_filepath[:3], target_wav_filepath)

		copy_file(source_file=source_transcript_filepath, dest_file=dest_transcript_filepath)
		copy_file(source_file=source_wav_filepath, dest_file=dest_wav_and_lab_filepath)
		copy_file(source_file=source_wav_filepath, dest_file=dest_wav_filepath)


	def prepare_mfa_training(self):

		emotional_base_path = get_path(self.source_dataset_path, "*emotional", "**")
		emotional_speaker_list = [speaker.split("/")[-1] for speaker in glob.glob(emotional_base_path) if not "." in speaker]
		emotional_source_transcript_path = glob.glob(get_path(emotional_base_path, "transcript", "*.txt"))
		emotional_source_wav_path = glob.glob(get_path(emotional_base_path, "wav", "*.wav"))
		emotional_filepath = list(zip(emotional_source_transcript_path, emotional_source_wav_path))	
	
		[[create_dir(self.savepath, speaker), create_dir(self.savepath_wavs, speaker)] for speaker in emotional_speaker_list]
		speaker_dict = dict([(speaker, idx) for idx, speaker in enumerate(emotional_speaker_list)])
		num_of_speakers = len(emotional_speaker_list)

		print("\n[LOG] create dataset...")
		do_multiprocessing(self.job, emotional_filepath, num_jobs=self.num_threads)

		print("\n[LOG] create phoneme dictionary...")
		phoneme_dictionary = create_phoneme_dictionary(self.savepath)	

		print("\n[LOG] write phoneme dictionary and metadata...")	
		write_phoneme_dictionary(savepath=self.phoneme_dictionary_savepath, phoneme_dictionary=phoneme_dictionary)
		write_multispeaker_emotion_metadata(source_path=self.savepath, savepath=self.metadata_savepath, speaker_dict=speaker_dict)
		print("[LOG] done!\n")
