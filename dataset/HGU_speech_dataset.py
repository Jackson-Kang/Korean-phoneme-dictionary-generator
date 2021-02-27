from utils import copy_file, get_path, create_dir, do_multiprocessing, read_meta, write_file
from utils import create_phoneme_dictionary, write_dictionary, write_multispeaker_emotion_metadata

from tqdm import tqdm
import glob


class HGU_Speech():

	def __init__(self, source_dataset_path, savepath, savepath_wavs, metadata_savepath, grapheme_dictionary_savepath, phoneme_dictionary_savepath, num_threads):
		self.source_dataset_path = source_dataset_path
		self.savepath = savepath
		self.savepath_wavs = savepath_wavs
		self.metadata_savepath = metadata_savepath
		self.grapheme_dictionary_savepath = grapheme_dictionary_savepath
		self.phoneme_dictionary_savepath = phoneme_dictionary_savepath
		self.num_threads = num_threads


	def job(self, filepath):
		pass



	def prepare_mfa_training(self):

		lines = read_meta(get_path(self.source_dataset_path, "metadata.csv"))

		print("\n[LOG] create dataset...")	
		copy_file(source_file=" -r {}".format(get_path(self.source_dataset_path, "wavs", "*")), dest_file="{}/".format(self.savepath))
		copy_file(source_file=" -r {}".format(get_path(self.source_dataset_path, "wavs", "*")), dest_file="{}/".format(self.savepath_wavs))
		copy_file(source_file=get_path(self.source_dataset_path, "metadata.csv"), dest_file="{}".format(self.metadata_savepath))

	
		for line in tqdm(lines):
			wav_name, transcript, _, _, _= line.rstrip().split("|")
			lab_name = wav_name.replace("wav", "lab")
			dir_name = lab_name.split("_")[0]
			if dir_name == "acriil":
				dir_name = lab_name.split("__")[0] + "_"

			lab_path = get_path(self.savepath, dir_name, lab_name)
			write_file(lab_path, transcript)

		print("\n[LOG] create phoneme dictionary...")
		grapheme_dictionary, phoneme_dictionary = create_phoneme_dictionary(self.savepath)	

		print("\n[LOG] write grapheme and phoneme dictionary and metadata...")	
		write_dictionary(savepath=self.grapheme_dictionary_savepath, dictionary=grapheme_dictionary)
		write_dictionary(savepath=self.phoneme_dictionary_savepath, dictionary=phoneme_dictionary)
		write_multispeaker_emotion_metadata(source_path=self.savepath, savepath=self.metadata_savepath, speaker_dict=speaker_dict)
		print("[LOG] done!\n")
