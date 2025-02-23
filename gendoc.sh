#! /usr/bin/bash

set -o posix

FILES='config.py database.py beolingus.py beolingus-tk.py'

case $1 in
    gen)  pdoc --force --html $FILES ;;
    serv) pdoc --http localhost:$2  --force --html $FILES ;;
    *) echo "options: [gen | serv <port>]" ;;
esac




