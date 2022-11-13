#!/bin/bash
cd ~/Documents/projects/WORK/tv/radio_frontend && npm run build 
cp -r dist/* ~/Documents/projects/WORK/tv/stream_server/static
cd ~/Documents/projects/WORK/tv/stream_server && py app.py
