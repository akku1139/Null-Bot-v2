cd `dirname $0`

export PYTHONPATH="`pwd`:$PYTHONPATH"

while true; do
  git pull
  python src/main.py
  sleep 5
done
