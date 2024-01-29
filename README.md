# [VoicePAT: Voice Privacy Anonymization Toolkit](http://arxiv.org/abs/2309.08049)

**Note: This repository and its documentation are still under construction but can already be used for both 
anonymization and evaluation. We welcome all contributions to introduce more generation methods or evaluation metrics to the VoicePAT framework. 
If you are interested in contributing, please leave comments on a GitHub issue.**

VoicePAT is a toolkit for speaker anonymization research. It is based on the framework(s) by the [VoicePrivacy Challenges](https://github.com/Voice-Privacy-Challenge/Voice-Privacy-Challenge-2022) but contains the following improvements:

* It consists of **two separate procedures for anonymization and evaluation**. This means that the generation of 
  anonymized speech is independent of the evaluation of anonymization systems. Both processes do not need to be 
  executed in the same run or with the same settings. Of course, you need to perform the anonymization of evaluation 
  data with one system before you can evaluate it but this could have happened at an earlier time and with an 
  external codebase.
* Anonymization and evaluation procedures are **structured as pipelines** consisting of separate **modules**. Each 
  module may have a selection of different models or algorithm to fulfill its role. The settings for each procedure 
  / pipeline are defined exclusively in configuration files. See the *Usage* section below for more information.
* **Evaluation models** have been exchanged by models based on [SpeechBrain](https://github.com/speechbrain/speechbrain/) and [ESPnet](https://github.com/espnet/espnet/) which are **more powerful** than the 
  previous Kaldi-based models. Furthermore, we added new techniques to make evaluation significantly **more 
  efficient**.
* The framework is written in **Python**, making it easy to include and adapt other Python-based models, e.g., using 
  PyTorch. When using the framework, you do not need in-depth knowledge about anything outside the Python realm 
  (Disclaimer: While being written in Python, the ASR evaluation is currently included with an ESPnet-based model 
  which in turn is based on Kaldi. However, you do not need to modify that part of the code for using or 
  changing the ASR model and ESPnet is currently working on a Kaldi-free version.)


## Installation

Requires `conda` for environment management. Installation of `mamba` is also recommended for speeding up the environment-related tasks. Simply clone the repository and run the following commands, a conda environment will be generated in the project root folder and the pretrained models will be downloaded.

```bash
git clone -b vpc  https://github.com/DigitalPhonetics/VoicePAT.git
make install pretrained_eval_models
make pretrained_GAN # OPTIONAL: if you want to use the GAN model
```

The datasets have to be downloaded via the VoicePrivacy Challenge framework. Once the download is complete, the `.scp` files need to be converted to the absolute path, because they are relative to the challenge folder. Use [utils/relative_scp_to_abs.py](utils/relative_scp_to_abs.py) for this purpose. Then simply point `data_path` in the YAML configurations to the data folder of the VoicePrivacy Challenge framework.

## Usage

![](figures/framework.png)

For using the toolkit with the existing methods, you can use the configuration files in [configs](configs). You can also add more modules and models to the code and create your own config by using the existing ones as template. The configuration files use HyperPyYAML syntax, for which a useful reference is available [here](https://colab.research.google.com/drive/1Pg9by4b6-8QD2iC0U7Ic3Vxq4GEwEdDz?usp=sharing).

### Anonymization

The framework currently contains two pipelines for anonymization, [anon_ims_sttts_pc.yaml](configs/anon_ims_sttts_pc.yaml) and [anon_dsp.yaml](configs/anon_dsp.yaml). 

Running an anonymization pipeline is done like this:

```bash
python run_anonymization.py --config=configs/anon_ims_sttts_pc.yaml --gpu_ids=0,1 # optional: --force-compute
python run_anonymization.py --config=configs/anon_dsp.yaml  # optional: --force-compute
```

This will perform all computations that support parallel computing on the gpus with ID 0 and 1, and on GPU 0 
otherwise. If no gpu_ids are specified, it will run only on GPU 0 or CPU, depending on whether cuda is available. 
`--force-compute` causes all previous computations to be run again. In most cases, you can delete that flag from the 
command to speed up the anonymization.

Pretrained models for anonymization using STTTS-GAN pipeline are downloaded by `make pretrained_GAN_models`

### Evaluation

All other config files in [configs](configs) can be used for evaluation with different settings. In these configs, you need to adapt at least

```YAML
eval_data_dir: path to anonymized evaluation data in Kaldi-format
```

Running an evaluation pipeline could be done like this:

```bash
python run_evaluation.py --config=configs/eval_pre.yaml --gpu-ids 1,2,3
# OR
python run_evaluation.py --config=configs/eval_pre.yaml --gpu-ids 1,2,3 path/to/anonymized/data/in/KALDI/format # given path overrides the eval_data_dir specified in the .yaml config
```

The latter also allows piping the anonymization and the evaluation in the following way:

```bash
python run_anonymization.py --config=configs/anon_ims_sttts_pc.yaml --gpu-ids 1,2,3 | tail -n 1 | xargs python run_evaluation.py --config=configs/eval_pre.yaml --gpu-ids 1,2,3
```

Pretrained models for evaluation are downloaded by `make pretrained_eval_models`

## Acknowledgements

Several parts of this toolkit are based on or use code from external sources, i.e.,

* [VoicePrivacy Challenge 2022](https://github.com/Voice-Privacy-Challenge/Voice-Privacy-Challenge-2022), [ESPnet](https://github.com/espnet/espnet/), [SpeechBrain](https://github.com/speechbrain/speechbrain/) for evaluation
* the [GAN-based anonymization system by IMS (University of Stuttgart)](https://github.com/DigitalPhonetics/speaker-anonymization) for anonymization

See the READMEs for [anonymization](anonymization/README.md) and [evaluation](evaluation/README.md) for more information.

