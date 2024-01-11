###############################
## CONFIGURATION
###############################
.ONESHELL:
PHONY: install uninstall pretrained_models data

PROJECT_NAME = voicepat
ENV_NAME = $(PROJECT_NAME)_env

ifeq (, $(which mamba))
CONDA = conda
else
CONDA = mamba
endif

###############################
##@ INSTALLATION
###############################

install: $(ENV_NAME) ## Performs the installation. Currently the only step is to install the conda environment

uninstall:
	@rm -rf $(ENV_NAME)
	@rm -rf models/
	@rm -rf evaluation/utility/asr/exp
	@rm -rf exp

data: ## Downloads the datasets from challenge server. This requires interactively entering the password a few times.
	@echo Downloading data from challenge server. This requires interactively entering the password a few times.
	@./01-download_data.sh

pretrained_eval_models: ## Downloads the pretrained evaluation (ASV,ASR) models
	@echo Downloading evaluation models from IMS repositories
	@wget -q https://github.com/DigitalPhonetics/VoicePAT/releases/download/v2/data.zip
	@wget -q https://github.com/DigitalPhonetics/VoicePAT/releases/download/v2/pre_model.zip
	@unzip -q data.zip
	@unzip -q pre_model.zip
	@rm data.zip
	@rm pre_model.zip

pretrained_GAN: ## Downloads the pretrained GAN anonymization models from IMS repositories
	@echo Downloading GAN models from IMS repositories
	@rm -rf models
	@mkdir -p models
	@wget -q -O models/anonymization.zip https://github.com/DigitalPhonetics/speaker-anonymization/releases/download/v2.0/anonymization.zip
	@wget -q -O models/asr.zip https://github.com/DigitalPhonetics/speaker-anonymization/releases/download/v2.0/asr.zip
	@wget -q -O models/tts.zip https://github.com/DigitalPhonetics/speaker-anonymization/releases/download/v2.0/tts.zip
	@unzip -oq models/asr.zip -d models
	@unzip -oq models/tts.zip -d models
	@unzip -oq models/anonymization.zip -d models
	@rm models/*.zip


$(ENV_NAME): environment.yaml
	@($(CONDA) env create -f $< -p ./$@) || $(CONDA) env update -f $< -p ./$@
	@(. $(ENV_NAME)/bin/activate && conda develop .)
	@conda config --set env_prompt '($$(basename {default_env})) '
	@(cat .gitignore | grep -q $(ENV_NAME)) || echo $(ENV_NAME) >> .gitignore

###############################
##@ SELF-DOCUMENTING COMMAND
###############################

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
