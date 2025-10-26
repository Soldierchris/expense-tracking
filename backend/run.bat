@echo off
call venv\Scripts\activate
uvicorn app.presentation.api.main:app --reload