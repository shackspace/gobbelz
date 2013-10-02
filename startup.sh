#!/bin/bash

tmux new-session -d -s gobbelz 
tmux send-keys -t gobbelz "/home/hohden/gobbelz/routes.py"$'\n'
sleep 2
