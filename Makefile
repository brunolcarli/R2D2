install:
	pip install -r requirements.txt

run:
	python main.py

pipe:
	make install
	make run
