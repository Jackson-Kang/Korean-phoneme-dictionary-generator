from multiprocessing import Pool
from tqdm import tqdm

from g2pk import G2p
from jamo import h2j

from glob import glob
import os



g2p = G2p()

def do_multiprocessing(job, tasklist, num_jobs=8):
	p = Pool(num_jobs)
	with tqdm(total=len(tasklist)) as pbar:
		for _ in tqdm(p.imap_unordered(job, tasklist)):
			pbar.update()	

def get_path(*args):
	return os.path.join('', *args)

def create_dir(*args):
        path = get_path(*args)
        if not os.path.exists(path):
                os.mkdir(path)
        return path

def copy_file(source_file, dest_file):
	if not os.path.exists(dest_file):
		os.system("cp {} {}".format(source_file, dest_file))


def read_file(source_path):
	with open(source_path, mode="r", encoding="utf-8-sig") as f:
		content = f.readline().rstrip()
	return content

def create_phoneme_dictionary(source_path):
	phoneme_dict = {}
	for lab_file in tqdm(glob(get_path(source_path, "**", "*.lab"))):
		sentence = read_file(lab_file)
		word_list = sentence.split(" ")
		phoneme_list = h2j(g2p(sentence)).split(" ")

		for idx, word in enumerate(word_list):
			if not word in phoneme_dict.keys():
				phoneme_dict[word] = " ".join(phoneme_list[idx])

	return phoneme_dict


def write_phoneme_dictionary(savepath, phoneme_dictionary):
	"""
		input-dict format
			key: word of transcript delimited by <space> (e.g. 국물이)	
			value: phoneme of hangul-word decomposed into syllables  (e.g. ㄱㅜㅇㅁㅜㄹㅣ)
				=> i.e., input dictionary must define word-phoneme mapping
	"""

	with open(savepath, "w", encoding="utf-8") as f:
		for key in phoneme_dictionary.keys():
			content = "{}\t{}\n".format(key, phoneme_dictionary[key])
			f.write(content)


def write_multispeaker_emotion_metadata(source_path, savepath, speaker_dict):
	"""
		save-format
			filename | transcript | transcript_jamo | transcript_phoneme | speaker_label | emotion_label
				=> LJ-Speech-styled metadata format
	"""
	contents = ""

	for lab_file in tqdm(glob(get_path(source_path, "**", "*.lab"))):

		filename = lab_file.split("/")[-1].replace("lab", "wav")
		transcript = read_file(lab_file)
		transcript_jamo = h2j(transcript)
		transcript_phoneme = h2j(g2p(transcript))
		speaker_label = speaker_dict[filename[:3]]
		emotion_label = "{:05d}".format(int(lab_file.replace(".lab", "")[-5:]) - 1)[-3]

		contents += "{}|{}|{}|{}|{}|{}\n".format(filename, transcript, transcript_jamo, transcript_phoneme, speaker_label, emotion_label)

	with open(savepath, "w", encoding='utf-8') as f:
		f.write(contents)


