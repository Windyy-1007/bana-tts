import json
import sys
import soundfile as sf
import torch

# For Grad-TTS
import TTS.params as params
from TTS.model import GradTTS
from TTS.praat_utils import change_gender
from TTS.text import text_to_sequence, bndict
from TTS.text.symbols import symbols
from TTS.utils import intersperse

# For HiFi-GAN
sys.path.append('./TTS/hifi-gan/')
from env import AttrDict
from models import Generator as HiFiGAN

print("GPU", torch.cuda.is_available())
if torch.cuda.is_available():
    device = "cuda:0"
else:
    device = "cpu"


def load_acoustic_model(chkpt_path, lex_path):
    generator = GradTTS(
        len(symbols) + 1,
        1,
        params.spk_emb_dim,
        params.n_enc_channels,
        params.filter_channels,
        params.filter_channels_dp,
        params.n_heads,
        params.n_enc_layers,
        params.enc_kernel,
        params.enc_dropout,
        params.window_size,
        params.n_feats,
        params.dec_dim,
        params.beta_min,
        params.beta_max,
        pe_scale=1000,
    ).to(device)
    generator.load_state_dict(
        torch.load(chkpt_path, map_location=lambda loc, storage: loc)
    )
    _ = generator.eval()
    print(f"Number of parameters: {generator.nparams}")

    cmu = bndict.BNDict(lex_path)
    return generator, cmu


def load_vocoder(chkpt_path, config_path):
    with open(config_path) as f:
        h = AttrDict(json.load(f))
    hifigan = HiFiGAN(h).to(device)
    hifigan.load_state_dict(
        torch.load(chkpt_path, map_location=lambda loc, storage: loc)["generator"]
    )
    _ = hifigan.eval()
    hifigan.remove_weight_norm()

    return hifigan


def infer(text, generator, dct):
    x = torch.LongTensor(
        intersperse(text_to_sequence(text, dictionary=dct), len(symbols))
    ).to(device)[None]
    x_lengths = torch.LongTensor([x.shape[-1]]).to(device)

    _, y_dec, _ = generator.forward(
        x,
        x_lengths,
        n_timesteps=50,
        temperature=1.3,
        stoc=False,
        spk=None,
        length_scale=1.1,
    )

    return y_dec


generator, dct = load_acoustic_model(
    "./TTS/logs/bahnar_exp/grad_1344.pt", "./TTS/data/bahnar_lexicon.txt"
)

# generator_fm, dct_fm = load_acoustic_model(
#     "./TTS/logs/bahnar_female_exp/grad_1264.pt", "./TTS/data/bahnar_lexicon.txt"
# )

hifigan = load_vocoder(
    "./TTS/checkpts/hifigan.pt", "./TTS/checkpts/hifigan-config.json"
)

class AudioConfig:
    def __init__(self):
        self.output_sampling_rate = 22050
        
        self._female = {
            "binhdinh": {
                "pitch_min": 75,
                "pitch_max": 600,
                "formant_shift_ratio": 1.27,
                "new_pitch_median": 196.0,
                "pitch_range_factor": 1.27,
                "duration_factor": 1.0
            },
            "gialai": {
                "pitch_min": 75,
                "pitch_max": 600,
                "formant_shift_ratio": 1.03,
                "new_pitch_median": 212.0,
                "pitch_range_factor": 1.03,
                "duration_factor": 1.0
            },
            "kontum": {
                "pitch_min": 75,
                "pitch_max": 600,
                "formant_shift_ratio": 1.2,
                "new_pitch_median": 199.0,
                "pitch_range_factor": 1.1,
                "duration_factor": 1.0
            }
        }
        self._male = {
            "binhdinh": {
                "pitch_min": 75,
                "pitch_max": 600,
                "formant_shift_ratio": 1.0,
                "new_pitch_median": 0.0,
                "pitch_range_factor": 1.0,
                "duration_factor": 1.0
            },
            "gialai": {
                "pitch_min": 75,
                "pitch_max": 600,
                "formant_shift_ratio": 1.0,
                "new_pitch_median": 180.0,
                "pitch_range_factor": 1.15,
                "duration_factor": 1.0
            },
            "kontum": {
                "pitch_min": 75,
                "pitch_max": 600,
                "formant_shift_ratio": 1.06,
                "new_pitch_median": 216.0,
                "pitch_range_factor": 1.09,
                "duration_factor": 1.0
            }
        }
        
    def get_config(self, gender="male", region="binhdinh"):
        if gender == "male":
            return self._male[region]
        elif gener == "female":
            return self._female[region]
        else:
            raise NotImplementedError

if __name__ == "__main__":
    input_text = text = "trong glong tôjroh ameêm teh ñak"
    output_path = "test.wav"
    
    config = AudioConfig()
    y = infer(input_text, generator, dct)

    with torch.no_grad():
        audio = hifigan.forward(y).cpu().squeeze().clamp(-1, 1)

    audio = change_gender(audio, config.output_sampling_rate, **config.female)
    sf.write(output_path, audio, config.output_sampling_rate)
