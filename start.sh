cd `dirname $0`

export PYTHONPATH="`pwd`:$PYTHONPATH"

while true; do
  python src/main.py
  git pull
  sleep 5
done
