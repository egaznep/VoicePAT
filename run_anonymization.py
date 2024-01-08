import logging
from pathlib import Path
import torch
import typer
from typing import Optional
from typing_extensions import Annotated, Callable

from anonymization.pipelines.sttts_pipeline import STTTSPipeline
from anonymization.pipelines.dsp_pipeline import DSPPipeline
from anonymization.pipelines.base_pipeline import BasePipeline

from utils import parse_yaml, get_datasets

PIPELINES: dict[str, Callable[..., BasePipeline]] = {
    "sttts": STTTSPipeline,
    "dsp": DSPPipeline,
}

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
            help="Comma separated list of GPU ids to use. If not specified, CPU will be used.",
        ),
    ] = '0',
    force_compute: Annotated[
        bool,
        typer.Option(
            '--force-compute',
            help="If given, forces re-computation of all steps. Otherwise uses saved results.",
        ),
    ] = False,
):
    config = parse_yaml(Path(config))
    datasets = get_datasets(config)
    gpus = gpu_ids.split(",")

    devices = []
    if torch.cuda.is_available():
        for gpu in gpus:
            devices.append(torch.device(f"cuda:{gpu}"))
    else:
        devices.append(torch.device("cpu"))

    with torch.no_grad():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s- %(levelname)s - %(message)s",
        )
        logging.info(f'Running pipeline: {config["pipeline"]}')
        pipeline = PIPELINES[config["pipeline"]](
            config=config, force_compute=force_compute, devices=devices
        )
        pipeline.run_anonymization_pipeline(datasets)


if __name__ == "__main__":
    typer.run(main)
