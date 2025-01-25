# VAWL - Vosk As Wakeword Listener
### A simple and powerful Wakeword Listener that requires zero training using Vosk

## Demo Video :
### [Watch it here](https://drive.google.com/file/d/1gHh2FO-KfbKWZtPlf0vYL6eB71dF67p3/view?usp=sharing)

## Introduction
[Vosk](https://alphacephei.com/vosk/) is an offline speech recognition toolkit created by alphacephei. Though it was popular choice for a STT (speech to text) during its initial release, with emergence of better models like [OpenAI's Whisper](https://openai.com/index/whisper/), it's usage as a STT has significantly declined. However, I noticed that Vosk supports fixed vocabulary inference from [this example](https://github.com/alphacep/vosk-api/blob/master/python/example/test_text.py) in the offcial repo and realised that this feature of Vosk can be used to repurpose it into a powerful wakeword listener !

## Features of Vawl
- No training required !!
- Extremely Simple Usage, Here is the code that you need to write to create a simple wakeword listening process, that listens and responds to the word "hello"
```python
from vawl.wl import WakeWordListnerProcess

def hello_callback():
    print("Hey there !")

try:
    my_wl = WakeWordListnerProcess()
    my_wl.register_wakeword('hello', hello_callback)
    my_wl.start()
except KeyboardInterrupt:
    my_wl.stop()
```
- Multiple wakewords supported, with ability to use different action/callback functions in a single instance
- Completely Offline
- Lightweight, will work even on a pi ! 
- Can be used with different models of vosk. (Default: Indian English Small)

## Supported Platforms
Refer to [Vosk Documentation](https://alphacephei.com/vosk/install) for supported platforms. VAWL should work in any platform where python PyPI package for Vosk is available.

## Tested On:
- Ubuntu 24.04 LTS (Python 3.12.3)

## Installation and Usage
1. Clone this repo.
2. Create a virtual environment and install the necessary dependencies.
```bash
python -m venv vawl_env
source vawl_env/bin/activate # For Linux Only !
pip install vosk sounddevice setproctitle
```
3. Download the required model from [vosk's models page](https://alphacephei.com/vosk/models). Default is Indian English Small Model.
4. Ensure that model and device parameters of WakeWordListnerProcess in example.py is proper and then Run the file !
```bash
python example.py
```

## Known Limitations
- Since the vocabulary of these models are fixed, vawl is not suitable for usecases with an uncommon word
