# TikTok Captcha Solver API
install Python
## Import $ install
pip install tiktok-captcha-solver --upgrade

cd tiktok_captcha_solver
pip install -r requires.txt

## ################################

selenium
webdriver-manager
pydantic
requests
pytest
pytest-asyncio
playwright
playwright-stealth
undetected_chromedriver
setuptools

## Copy .ex.env to .env
get api https://www.sadcaptcha.com/

## RUN

pytest new_object.py

## cài đặt fastAPI local
cd server
pip install fastapi uvicorn pymongo python-dotenv

run uvicorn main:app --reload to start swagger

npm i