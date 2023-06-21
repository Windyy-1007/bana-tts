import argparse
import json
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as ipd
from tqdm import tqdm
from scipy.io.wavfile import write
import soundfile as sf

import torch

# For Grad-TTS
import TTS.params as params
from TTS.model import GradTTS
from TTS.text import text_to_sequence, bndict
from TTS.text.symbols import symbols
from TTS.utils import intersperse

# For HiFi-GAN
import sys
sys.path.append('./TTS/hifi-gan/')
from env import AttrDict
from models import Generator as HiFiGAN

print("GPU", torch.cuda.is_available())
if torch.cuda.is_available():
    device = "cuda:0"
else:
    device = "cpu"

def load_acoustic_model(chkpt_path, lex_path):
    generator = GradTTS(len(symbols)+1, 1, params.spk_emb_dim,
                    params.n_enc_channels, params.filter_channels,
                    params.filter_channels_dp, params.n_heads, params.n_enc_layers,
                    params.enc_kernel, params.enc_dropout, params.window_size,
                    params.n_feats, params.dec_dim, params.beta_min, params.beta_max,
                    pe_scale=1000).to(device)
    generator.load_state_dict(torch.load(chkpt_path, map_location=lambda loc, storage: loc))
    _ = generator.eval()
    print(f'Number of parameters: {generator.nparams}')

    cmu = bndict.BNDict(lex_path)
    return generator, cmu


def load_vocoder(chkpt_path, config_path):
    with open(config_path) as f:
        h = AttrDict(json.load(f))
    hifigan = HiFiGAN(h).to(device)
    hifigan.load_state_dict(torch.load(chkpt_path, map_location=lambda loc, storage: loc)['generator'])
    _ = hifigan.eval()
    hifigan.remove_weight_norm()

    return hifigan


def infer(text, generator, dct):
    x = torch.LongTensor(intersperse(text_to_sequence(text, dictionary=dct), len(symbols))).to(device)[None]
    x_lengths = torch.LongTensor([x.shape[-1]]).to(device)

    _, y_dec, _ = generator.forward(x, x_lengths, n_timesteps=50, temperature=1.3,
                                        stoc=False, spk=None,
                                        length_scale=1.5)

    return y_dec

generator, dct = load_acoustic_model('./TTS/logs/bahnar_exp/grad_1344.pt', './TTS/data/bahnar_lexicon.txt')
generator_fm, dct_fm = load_acoustic_model('./TTS/logs/bahnar_female_exp/grad_1264.pt', './TTS/data/bahnar_lexicon.txt')

hifigan = load_vocoder('./TTS/checkpts/hifigan.pt', './TTS/checkpts/hifigan-config.json')
output_sampling_rate = 22050

if __name__ == '__main__':
    input_text = text = "trong glong tôjroh ameêm teh ñak"
    output_path = 'test.wav'

    y = infer(input_text, generator, dct)

    with torch.no_grad():
        audio = hifigan.forward(y).cpu().squeeze().clamp(-1, 1)

    sf.write(output_path, audio, output_sampling_rate)
