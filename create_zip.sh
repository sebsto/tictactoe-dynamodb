#!/bin/bash

zip -r ../tictactoe-app.zip . -x ".git/*" -x "*/__pycache__/*" -x ".venv/*"
