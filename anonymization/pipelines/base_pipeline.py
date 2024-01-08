from pathlib import Path
import typing


class BasePipeline:
    def __init__(self, config: dict):
        pass

    def run_anonymization_pipeline(
        self,
        datasets: typing.Dict[str, Path],
    ) -> dict:
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
        raise NotImplementedError("You must implement this method in a subclass")
