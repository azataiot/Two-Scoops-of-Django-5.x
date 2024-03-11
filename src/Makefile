.PHONY: help install dev-install requirements dev-requirements clean
.DEFAULT_GOAL := help

# -- global targets --
## This help screen
help:
	@echo "Available targets:"
	@awk '/^[a-zA-Z\-\_0-9%:\\ ]+/ { \
	  helpMessage = match(lastLine, /^## (.*)/); \
	  if (helpMessage) { \
	    helpCommand = $$1; \
	    helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
	    gsub("\\\\", "", helpCommand); \
	    gsub(":+$$", "", helpCommand); \
	    printf "  \x1b[32;01m%-35s\x1b[0m %s\n", helpCommand, helpMessage; \
	  } \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -u


# -- Dependencies --
## Install dependencies
install:
	@echo "Installing dependencies"
	@pip install -r requirements/requirements.txt

## Install development dependencies
dev-install:
	@echo "Installing development dependencies"
	@pip install -r requirements/dev-requirements.txt

## Make requirements
requirements:
	@echo "Pip-compile requirements"
	@python -m piptools compile --strip-extras requirements/requirements.in

## Make development requirements
dev-requirements:
	@echo "Pip-compile dev-requirements"
	@python -m piptools compile  --strip-extras requirements/dev-requirements.in


# -- Code Quality --
## Clean Python cache files
clean:
	@echo "Cleaning Python cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@echo "Done!"