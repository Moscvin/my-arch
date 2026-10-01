#!/bin/sh
# Pune cele 2 monitoare unul langa altul: primul conectat = principal (stanga).
# Daca ai salvat un profil cu autorandr (vezi README), il foloseste pe acela.

if autorandr --change >/dev/null 2>&1; then
    exit 0
fi

outputs=$(xrandr --query | awk '/ connected/ {print $1}')
first=$(echo "$outputs" | sed -n 1p)
second=$(echo "$outputs" | sed -n 2p)

[ -z "$first" ] && exit 0

if [ -n "$second" ]; then
    xrandr --output "$first" --primary --auto --pos 0x0 \
           --output "$second" --auto --right-of "$first"
else
    xrandr --output "$first" --primary --auto
fi
