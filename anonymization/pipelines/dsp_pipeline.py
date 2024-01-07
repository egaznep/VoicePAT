from datetime import datetime
import logging
from pathlib import Path

from anonymization.modules.dsp.anonymise_dir_mcadams_rand_seed import process_data
from utils import save_yaml


logger = logging.getLogger(__name__)

class DSPPipeline:
    """
    This pipeline consists of:
          - LPC residual (untouched)     -
    input - LPC coefficients - shrinking - TTS -> output
    """

    def __init__(self, config):
        self.config = config
        self.modules_config = config['modules']
        self.results_dir = config['results_dir']

    def run_anonymization_pipeline(self, datasets):

        for i, (dataset_name, dataset_path) in enumerate(datasets.items()):
            logger.info(f"{i + 1}/{len(datasets)}: Processing {dataset_name}...")
            process_data(dataset_path=dataset_path, anon_level=self.modules_config['anon_level'], settings=self.modules_config)
        logger.info("Anonymization pipeline completed.")

        save_yaml(
            self.config, self.results_dir / "formatted_data" / now / "config.yaml"
            )
