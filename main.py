from dataset import emotiontts_open_db
from utils import create_dir, get_path

import configs as cfg


def main():

	_ 			  = create_dir(cfg.savedir)
	savedir			  = create_dir(cfg.savedir, cfg.dataset_name)
	savepath		  = create_dir(savedir, "wavs_with_lab")
	savepath_wavs		  = create_dir(savedir, "wavs")
	metadata_savepath	  = get_path(savedir, cfg.metadata_name)
	grapheme_dict_savepath	  = get_path(savedir, cfg.grapheme_dictionary_name)
	phoneme_dict_savepath	  = get_path(savedir, cfg.phoneme_dictionary_name)

	if cfg.dataset_name == "emotiontts_open_db":
		instance = emotiontts_open_db.EmotionTTS_OpenDB(
						source_dataset_path = cfg.source_dataset_path,
						savepath = savepath,
						savepath_wavs = savepath_wavs,
						metadata_savepath = metadata_savepath,
						grapheme_dictionary_savepath = grapheme_dict_savepath,
						phoneme_dictionary_savepath = phoneme_dict_savepath,
						num_threads=cfg.NUM_THREADS)

	else:
		print("[LOG] No dataset named {}".format(cfg.dataset_name))

	instance.prepare_mfa_training()


if __name__ == "__main__":
	main()
