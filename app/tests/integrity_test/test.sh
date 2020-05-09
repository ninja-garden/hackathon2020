#/bin/bash

python3 ../../cli.py --config config.json --image a.png --north 55.8305106504981 --south 55.8231743212821 --east 35.8119157103966 --west 35.7988817468766 &> /dev/null

if [ $? -eq 0 ]; then
    echo "Integrity test passed."
fi
