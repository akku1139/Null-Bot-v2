cd `dirname $0`

export PYTHONPATH="`pwd`:$PYTHONPATH"

python src/main.py
