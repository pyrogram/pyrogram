# Pyrogram Docs

- Install requirements.
- Install `pandoc` and `latexmk`.
- HTML: `make html`
- PDF: `make latexpdf`

## Build Guide
- make a venv: `python3 -m venv virtualenv`
- active virtual environment: `source virtualenv/bin/activate`
- Install dependencies: `pip install -r requirements.txt && pip install tgcrypto`
- Install pyrogram from source: `python setup.py install --user`
- Change Directory to `docs` and install depenedencies: `cd docs && pip install -r requirements.txt`
- Run releases inside `scripts` directory: `cd scripts && python releases.py`
- Change back to project root and run `cd .. && cd .. && python setup.py generate --docs`
- Finally go to `docs` directory and run `make html` to build the docs: `cd docs && make html` / or you can run `make lhtml` to run to see your docs build in a live webserver

### Note
- Both builds will take a few minutes depending on your machine
- Ignore the Warning: `WARNING: html_static_path entry '_static' does not exist`
- If you face any errors or missing docs feel free to get help from our [Community](https://t.me/pyrogramchat)
