.PHONY: help local build serve clean

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  local   Build and serve at http://localhost:8000"
	@echo "  build   Convert chapters to HTML in docs/"
	@echo "  serve   Serve existing docs/ without rebuilding"
	@echo "  clean   Remove docs/ and rebuild from scratch"

local: build serve

build:
	python build.py

serve:
	python -m http.server --directory docs

clean:
	python build.py --clean
