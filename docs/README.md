# 📚 Pyrogram Docs

- Clone the repository: 
``` bash 
git clone https://github.com/pyrogram/pyrogram
```
- Generate the files to build the docs:
``` bash
python3 setup.py generate --api && python3 setup.py generate --docs
```
- Install Pandoc, then go into the docs folder and install the requirements: 
```bash
apt install pandoc && cd docs && pip install -r requirements.txt
```

- HTML Docs: 
```bash
make html
```
- PDF Docs:  
```bash
apt install latexmk && make latexpdf
```
