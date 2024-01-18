import logging
import utils.logging
from pathlib import Path
import sys
import torch # import torch only if gpu_ids is given
import typer
from typing import Optional
from typing_extensions import Annotated, Callable

from anonymization.pipelines.base_pipeline import BasePipeline
from utils import parse_yaml, get_datasets

logger = logging.getLogger('root:anonymizer')

def main(
    config: Annotated[
        Optional[Path],
        typer.Option(
            help="Path to the config file.",
        ),
    ] = "configs/anon_config.yaml",
    gpu_ids: Annotated[
        str,
        typer.Option(
            help="Comma separated list of GPU ids to use. If not specified, a torch.device will not be created.",
        ),
    ] = None,
    force_compute: Annotated[
        bool,
        typer.Option(
            '--force-compute',
            help="If given, forces re-computation of all steps. Otherwise uses saved results.",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            '--verbose', '-v',
            help="If given, sets logging level to DEBUG.",
        ),
    ] = False,
):
    
    logging.basicConfig(
        level=logging.DEBUG if verbose else utils.logging.NOTICE,
        format="%(asctime)s - Anonymization:%(name)s- %(levelname)s - %(message)s",
    )
    
    config = parse_yaml(Path(config))
    datasets = get_datasets(config)
    if gpu_ids is not None:
        gpus = gpu_ids.split(",")

        devices = []
        if torch.cuda.is_available():
            for gpu in gpus:
                devices.append(torch.device(f"cuda:{gpu}"))
        else:
            devices.append(torch.device("cpu"))
        logger.log(utils.logging.NOTICE, f'Using devices: {devices}')
    else:
        devices = None
        logger.log(utils.logging.NOTICE, f'No device specified, running on CPU.')


    logger.log(utils.logging.NOTICE, f'Running pipeline: {config["pipeline"]}')
    pipeline: BasePipeline = config["pipeline"](
        config=config, force_compute=force_compute, devices=devices
    )
    out = pipeline.run_anonymization_pipeline(datasets)
    print(out, file=sys.stdout)


if __name__ == "__main__":
    typer.run(main)