from tkinter import N
from espnet2.bin.tts_inference import Text2Speech
import torch
import time

# Load the model
origin = False
if origin:
    text2speech = Text2Speech(
        train_config="downloads/f3698edf589206588f58f5ec837fa516/exp/tts_train_vits_raw_phn_jaconv_pyopenjtalk_accent_with_pause/config.yaml",
        model_file="downloads/f3698edf589206588f58f5ec837fa516/exp/tts_train_vits_raw_phn_jaconv_pyopenjtalk_accent_with_pause/train.total_count.ave_10best.pth",
        device='cuda'
    )
else:
    text2speech = Text2Speech(
        train_config="exp/tts_amadeus_vits_finetune_from_jsut_32_sentence/config.yaml",
        model_file="exp/tts_amadeus_vits_finetune_from_jsut_32_sentence/train.total_count.ave.pth",
        device='cuda',
        speed_control_alpha=1.0,
    )
filepath = '/gds/jcao/code/espnet/egs2/amadeus/tts1/local/texts/text1.txt'
with open(filepath, 'r') as f:
    texts = f.readlines()
type='read'

# texts = [
#     '画面の前の皆さんこんにちは', 
#     'まきせくりすです...どうぞよろしく',
#     'ご覧のとおり、現在の人工知能技術を使用して音声システムを合成しているだけです',
#     '技術的およびデータセットの制限により、現在成熟していません',
#     '今は対話機能がありません',
#     '対話システムは、よりインテリジェントになることを期待して、フォローアップで導入されます',
#     '今回はここまで、また次回',
#     # '忘れないで，あなたはどの世界線にいてもひとりじゃない，私がいる',
#     'さようならみんな'
# ]
# type='introduction'



wavs = None

# synthesis
start = time.time()
with torch.no_grad():
    for text in texts:
        wav = text2speech(text)['wav']
        # print(wav.shape)
        if wavs is None:
            wavs = wav
        else:
            wavs = torch.cat((wavs, wav))
        silence = torch.zeros(int(text2speech.fs*0.1)).to(wavs.device)
        wavs = torch.cat((wavs, silence))
print(f"synthesis time: {time.time()-start}s")
print(f'wav time: {wavs.shape[0]/text2speech.fs}s')
# save
import soundfile as sf
if origin:
    sf.write(f'jsut_{type}.wav',wavs.cpu().numpy(), text2speech.fs,"PCM_16")
else:
    sf.write(f'amadeus_{type}.wav',wavs.cpu().numpy(), text2speech.fs,"PCM_16")
