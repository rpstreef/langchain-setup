# Makefile
SHELL := /bin/bash

# Default target executed when no arguments are given to make.
all: 
		help

run: 
		poetry run uvicorn app.main:app --reload --env-file .env

start: 
		$(shell ./scripts/ssh-and-start-vm.sh)

stop: 
		$(shell ./scripts/stop-vm.sh)

help:
	@echo '----'
	@echo 'make start                        - Connect to VM via SSH and (if required) starts the VM first'
	@echo 'make stop                       	 - Stops the VM'
	@echo 'make run                          - run LangChain locally with reload on code changes'