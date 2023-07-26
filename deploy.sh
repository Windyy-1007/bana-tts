#!/bin/bash
gunicorn -c gunicorn-cfg.py app_gpu:app

