from pathlib import Path
import os
import subprocess
import torch
from copy import deepcopy
from .speechbrain_asr.asr_train.train import train_speechbrain_asr

def train_asr_eval(params):
    backend = params.get('backend', 'speechbrain').lower()
    if backend == 'speechbrain':
        asr_train_speechbrain(train_params=params)
    else:
        raise ValueError(f'Unknown backend {backend} for ASR evaluation. Available backends: speechbrain.')

def asr_train_speechbrain(train_params):
    output_folder=train_params['model_dir']
    print(f'Train SpeechBrain ASR model: {output_folder}')
    hparams = {
        'batch_size': train_params['batch_size'],
        'lr_adam': train_params['lr'],
        'number_of_epochs': train_params['epochs'],
        'anon': train_params['anon'],
        'data_folder': str(train_params['train_data_dir']),
        'output_folder': str(train_params['model_dir']),
        'pretrained_path': str(train_params['pretrained_model']),
        'train_splits': [train_params['train_splits']],
    }

    config = train_params['train_config']

    run_opts = {
    'debug': False,
    'debug_batches': 2,
    'debug_epochs': 2,
    'debug_persistently': False,
    'device': 'cuda:0',
    'data_parallel_backend': False,
    'distributed_launch': False,
    'distributed_backend': 'nccl',
    'find_unused_parameters': False,
    'tqdm_colored_bar': False
}

    sb_run_opts = deepcopy(run_opts)
    if torch.cuda.device_count() > 1:
        sb_run_opts['distributed_launch'] = True
        from torch.distributed.launcher.api import LaunchConfig, elastic_launch
        # assuming single node
        launch_config = LaunchConfig(min_nodes=1, max_nodes=1, nproc_per_node=torch.cuda.device_count(), rdzv_endpoint='localhost:0', rdzv_backend='c10d')
        elastic_launch(launch_config, train_speechbrain_asr)(config, hparams, sb_run_opts)
    else:
        train_speechbrain_asr(config, hparams, run_opts=sb_run_opts)


