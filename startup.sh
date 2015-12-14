#!/bin/sh
cd "$(dirname "$(readlink -f "$0")")"
. bin/activate
python3 routes.py
