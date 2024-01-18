#!/usr/bin/env python3.0
# -*- coding: utf-8 -*-
"""
This pipeline consists of:
                         -> non-real poles -> McAdam coef -> modified poles
    input -> LP analysis -> real poles     ---------------->                -> LP synthesis -> output
                         -> residual       ---------------->
"""
from datetime import datetime
import logging
import utils.logging

from pathlib import Path

from anonymization.modules.dsp.anonymise_dir_mcadams_rand_seed import process_data
from anonymization.pipelines.base_pipeline import BasePipeline
from utils import save_yaml


logger = logging.getLogger(__name__)


class DSPPipeline(BasePipeline):
    """
    This pipeline consists of:
                             -> non-real poles -> McAdam coef -> modified poles
        input -> LP analysis -> real poles     ---------------->                -> LP synthesis -> output
                             -> residual       ---------------->
    """

    def __init__(self, config, **kwargs):
        self.config = config
        self.modules_config = config["modules"]
        self.results_dir = config["results_dir"]

    def run_anonymization_pipeline(self, datasets, force_compute=False):
        """
        Runs the anonymization pipeline on the given datasets. Optionally
        prepares the results such that the evaluation pipeline
        can interpret them.

        Args:
            datasets (dict of str -> Path): The datasets on which the
                anonymization pipeline should be runned on. These dataset
                will be processed sequentially. The dictionary should
                contain the dataset name as key and the path to the dataset
                as value.
        """
        for i, (dataset_name, dataset_path) in enumerate(datasets.items()):
            logger.log(utils.logging.NOTICE, f"{i + 1}/{len(datasets)}: Processing {dataset_name}...")
            process_data(
                dataset_path=dataset_path,
                anon_level=self.modules_config["anon_level"],
                settings=self.modules_config,
                results_dir=self.results_dir,
                force_compute=force_compute,
            )
        logger.log(utils.logging.NOTICE, "Anonymization pipeline completed.")

        # save config
        now = datetime.strftime(datetime.today(), "%d-%m-%y_%H:%M")
        save_yaml(
            self.config, self.results_dir / f"config-{now}.yaml"
        )
        return self.results_dir

if __name__ == '__main__':
    print(__doc__)
