# Makefile
SHELL := /bin/bash

# Default target executed when no arguments are given to make.
all: help

local: 
		poetry run uvicorn app.main:app --reload --env-file .env

docker:
		docker-compose up --build -d

docker-stop:
		docker-compose down

vm: 
		$(shell ./scripts/ssh-and-start-vm.sh)

vm-stop: 
		$(shell ./scripts/stop-vm.sh)

help:
	@echo '----'
	@echo 'make docker				- run LangChain on Docker, use `dry` to monitor containers'
	@echo 'make docker-stop			- stop all docker containers'
	@echo 'make vm					- Connect to VirtualBox via SSH and (if required) starts VirtualBox first'
	@echo 'make vm-stop				- Stops VirtualBox'
	@echo 'make local				- run LangChain locally with reload on code changes'