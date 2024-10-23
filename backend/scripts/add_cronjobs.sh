#!/bin/bash

workdir=$(realpath $(dirname $0))
cronjob_path=$workdir/lifehub_cronjobs
python_bin=$workdir/../venv/bin/python
tmp_file=/tmp/lifehub-cronjobs

# Execute the fetch command with the venv python binary
# and escape the slashes in the path
fetch_run="${python_bin//\//\\/} -m lifehub.app.fetch"

crontab -l > $tmp_file
# Remove existing LIFEHUB cronjobs
sed -i '/^.* # LIFEHUB/d' $tmp_file
# Add LIFEHUB cronjobs with a # LIFEHUB comment
sed "s/\(.*\)FETCH\(.*\)/\1${fetch_run}\2 # LIFEHUB/" $cronjob_path |
# Clear comments
sed '/^#.*$/d' >> $tmp_file

crontab $tmp_file
