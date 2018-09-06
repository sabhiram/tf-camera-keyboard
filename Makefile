.PHONY: all

all: video

env:
	source env/bin/activate

video:
	python video.py

