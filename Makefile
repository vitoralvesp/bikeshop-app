PYTHON ?= python3
PIP := $(PYTHON) -m pip
STREAMLIT := $(PYTHON) -m streamlit
APP := src/dashboard/app.py

.PHONY: help install run

help:
	@printf "Targets disponíveis:\n"
	@printf "  make install  Instala as dependências Python\n"
	@printf "  make run      Inicia o dashboard Streamlit\n"

install:
	$(PIP) install -r requirements.txt

run:
	$(STREAMLIT) run $(APP)
