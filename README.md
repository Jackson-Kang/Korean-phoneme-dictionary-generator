# Korean-phoneme-dictionary-generator
 Korean phoneme dictionary generator for training Montreal Forced Aligner (MFA)

# Introduction

Recently, the most major issue in Deep-learning based speech synthesis is to estimate duration for parallel(non-autoregressive) mel-spectrogram generation. One of the popular approaches is to use external aligner, replacing convertional attention-based seq2seq models. Recently proposed models such as [FastSpeech2](https://arxiv.org/pdf/2006.04558.pdf)(Y. Ren et. al., Microsoft, 2020), [Parallel Tacotron](https://arxiv.org/pdf/2010.11439.pdf)(I. Elias et. al., Google, 2020) and others utilize the external aligner and extract duration from text-wav utterances. The extracted durations are used as ground-truth target for training duration predictor. In synthesis-phase, the estimated duration from duration predictor is used to generate mel-spectrogram (or wav-signal) parallely (non-autoregressively).

To get the duration from Korean text-mel datset, we can use [Montreal Forced Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner)(MFA) as described in [FastSpeech2](https://arxiv.org/pdf/2006.04558.pdf) paper. However, we must do some hassles. Therefore, this repository offers some references and conviniences to reduce that hassels. Specifically, this repository provides followings:

* <sample.lab, sample.wav> paired structure in ``results/<dataset_name>/<wavs_with_lab>/`` directory
* Word-phoneme dictionary applied to Korean phoneme conversion and syllable decomposition (초성, 중성, 종성 분리)


# Install dependencies
Install dependencies via following command:
```
pip install -r requirements.txt
```


# How-to-use

Just run following command:
```
python main.py
```
After running, see the ``results/<dataset_name>/`` directory to check the generated word-phoneme dictionary and <sample.lab, sample.wav> paired structure.

To train the Korean MFA model, see this [docs](https://github.com/Kyubyong/g2pK) and just point the generated dictionary and path to ``results/<datset_name>/<wav_with_labs>/``.

# Notes
* The result of training [FastSpeech2](https://arxiv.org/pdf/2006.04558.pdf) with duration(TextGrid) extracted from pretrained Korean G2P and acoustic model is not good. See the [issues](https://github.com/HGU-DLLAB/Korean-FastSpeech2-Pytorch/issues/3#issuecomment-731979268) for details.
* I used [G2PK](https://github.com/Kyubyong/g2pK)(K. Park, 2019), a rule-based Korean G2P to convert grapheme to phoneme.
* Currently, only supports [emotiontts-open-db dataset](https://github.com/emotiontts/emotiontts_open_db/tree/master/Dataset/SpeechCorpus/Emotional)([KAIST](https://www.kaist.ac.kr/kr/) and [Selvas AI](https://www.selvasai.com/), 2020)
