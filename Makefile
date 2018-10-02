what:
	@echo "Make what? Try: clean dist-clean"

clean:
	-find . -name '*.egg-info' -exec rm -rf {} ';'
	-find . -name '__pycache__' -exec rm -rf {} ';'
	-find . -name '*.pyc' -exec rm {} ';'

dist-clean: clean
	rm -rf dist
