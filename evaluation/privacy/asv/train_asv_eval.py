from copy import deepcopy
import torch

from .asv_train.train_speaker_embeddings import train_asv_speaker_embeddings
from .asv_train.speechbrain_defaults import run_opts


def train_asv_eval(train_params, output_dir):
    backend = train_params.get('backend', 'speechbrain').lower()
    if backend == 'speechbrain':
        asv_train_speechbrain(train_params=train_params, output_dir=output_dir)
    else:
        raise ValueError(f'Unknown backend {backend} for ASR evaluation. Available backends: speechbrain.')


def asv_train_speechbrain(train_params, output_dir):
    print(f'Train ASV model: {output_dir}')
    hparams = {
        'pretrained_path': str(train_params['pretrained_model']),
        'batch_size': train_params['batch_size'],
        'lr': train_params['lr'],
        'num_utt': train_params['num_utt'],
        'num_spk': train_params['num_spk'],
        'utt_selected_ways': train_params['utt_selection'],
        'number_of_epochs': train_params['epochs'],
        'anon': train_params['anon'],
        'data_folder': str(train_params['train_data_dir']),
        'output_folder': str(output_dir)
    }

    config = train_params['train_config']

    if train_params['num_spk'] == 'ALL':
        hparams['out_n_neurons'] = 921
    else:
        hparams['out_n_neurons'] = int(train_params['num_spk'])

    sb_run_opts = deepcopy(run_opts)
    if torch.cuda.device_count() > 1:
        sb_run_opts['distributed_launch'] = True
        from torch.distributed.launcher.api import LaunchConfig, elastic_launch
        # assuming single node
        launch_config = LaunchConfig(min_nodes=1, max_nodes=1, nproc_per_node=torch.cuda.device_count(), rdzv_endpoint='localhost:0', rdzv_backend='c10d')
        elastic_launch(launch_config, train_asv_speaker_embeddings)(config, hparams, sb_run_opts)
    else:
        train_asv_speaker_embeddings(config, hparams, run_opts=sb_run_opts)
