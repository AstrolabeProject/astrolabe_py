what:
	@echo "Make what? Try: clean"

clean:
	-find . -name '*.egg-info' -exec rm -rf {} ';'
	-find . -name '__pycache__' -exec rm -rf {} ';'
	-find . -name '*.pyc' -exec rm {} ';'
