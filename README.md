# TI-84 Plus CE HTML5 Emulator

This is a standalone version of the official TI-84 Plus CE HTML5 emulator from Texas Instruments. The emulator assets are downloaded from `mn.testnav.com/client` and are not hosted on this repository.

To run the emulator, host a web server at this directory, then visit it in your browser.
```
$ python3 -m http.server
```

To bundle everything into a standalone HTML file, run the `inline.py` script. The resulting file will be located at `bundled.html`
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python3 inline.py
```

This repository is licensed under the MIT license. 