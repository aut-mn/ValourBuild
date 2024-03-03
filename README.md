# ValourBuild
A simple Valour setup assistant built in python.

## Usage

1. Clone this repo and run `install.py`

```bash
git clone https://github.com/aut-mn/ValourBuild --DEPTH=1 && cd ValourBuild && sudo python3 install.py
```

2. If you're on MacOS, you need to run `install.py` as a standard user.

```bash
python3 install.py
```

3. Follow the prompts given

> ⚠️ This installer is BROKEN if you are wishing to use the configuration setup part of the utility. This will be resolved when [this pull request](https://github.com/Valour-Software/Valour/pull/1202) is merged. Simply enter 'n' when it asks for guided configuration.

## Supported Operating Systems
Supports MacOS and most Linux distros. 

Note for Windows support, you need Windows 11+ with `winget` and `sudo` installed in order for this installer to function.

Note for MacOS support, you need to have the `brew` package manager installed.
