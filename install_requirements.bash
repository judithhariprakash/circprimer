source ../venv/bin/activate
cat requirements.txt | xargs -n 1 -I@ pip install @