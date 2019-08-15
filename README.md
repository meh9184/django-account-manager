# django-account-manager

#### JWT 기반의 Django Auth REST API, Google Oauth2.0 로그인 가능한 React Client Web App

<kbd>
  <img src="./screenshots/test.gif" alt="system-configuration" width='100%'/>
</kbd>

<br/>
<br/>


## *Introduction*

### Summary

> - Project 소개
>   - 간단한 계좌관리 웹 어플리케이션입니다.
>   - 사용자당 최대 5개의 계좌를 계설할 수 있으며, 주 계좌를 설정/변경할 수 있습니다.
>   - 계좌의 종류는 총 3가지 (일반/급여/적금) 존재하며, 각각의 종류마다 출금 한도가 존재합니다. 
>   - 입금 한도는 없으며, 출금 한도는 다음과 같습니다. 일반: 1회 30만원, 1일 30만원 / 급여: 1회 1,000만원, 1일 1억원 / 적금: 출금 불가
>   - 계좌간 이체가 가능하며, 종류가 다른 계좌로의 이체시 수수료 500원이 부과됩니다. 
>   - 다른 종류의 계좌로 이체시 하루 3건까지는 수수료가 면제됩니다.
>  <br/>
> 
> - BACKEND (Djagno)
>   - Django를 이용하여 구현
>   - JWT를 이용한 OAuth 2.0 Auth 프로토콜 기반으로 Authentication 및 Authorization 구현 
>  <br/>
> 
> - FRONTEND (Djagno Template)
>   - Server-side templating engine인 Django Template을 이용하여 구현


### Requirements

> - BACKEND/FRONTEND (Djagno/Django Template)
>   - [Python 3.6](https://www.python.org/downloads/release/python-360/)
>   - [Django 2.2.4](https://docs.djangoproject.com/en/2.2/releases/2.2.4/)
>  <br/>
> 
> - Database
>   - [MySQL 5.6](https://dev.mysql.com/downloads/mysql/5.6.html)

### DataBase Models and Relations
> 
> **Database schema**
> 
> <img src="./screenshots/database_schema.png" alt="database-schema" width='40%'/>
> 
> 1. 하나의 사용자(User) 모델은 다수의 계좌(Account) 모델을 가질 수 있다.
> 
> 2. 하나의 계좌(Account) 모델은 다수의 입금(Deposit) 모델을 가질 수 있다.
> 
> 3. 하나의 계좌(Account) 모델은 다수의 출금(Withdraw) 모델을 가질 수 있다.
> 
> 4. 하나의 계좌(Account) 모델은 다수의 이체(Trnsfer) 모델을 가질 수 있다.
>

<br/>


## *Installation*

### Clone project
> 
> - Github repository를 clone
> ```bash
> $ git clone https://github.com/meh9184/django-account-manager.git
> ```

### Configure db connection
> 
> - `core/settings.py` 파일의
> - DATABASES 부분 USER, PASSWORD 입력
> 
> ```python
> # Database
> 
> DATABASES = {
>     'default': {
>         'ENGINE': 'django.db.backends.mysql',
>         'NAME': 'account_manager',
>         'USER': 'INSERT HERE',        # 여기에 입력
>         'PASSWORD': 'INSERT HERE',    # 여기에 입력
>         'HOST': '127.0.0.1',
>         'PORT': '3306'
>     }
> }
> ```

### Create mysql schema 
> 
> - MySQL CLI 상에서 `account_manager` 이름으로 스키마 생성
> ```bash
> mysql> create schema jwt_todo_demo;
> ```

### Install Dependencies
>
> - virtaulenv 설치 안됐다면 apt-get으로 설치하고,
> - virtaulenv 명령어로 현재 디렉터리에 가상환경 `venv` 생성 및 활성화
> - Python 버전은 3.6
> ```bash
> $ sudo apt-get install virtualenv
> $ virtualenv --python=python3.6 venv
> $ source venv/bin/activate
> ```
>
> - libmysqlclient 설치 안됐다면 설치하고,
> - 현재 가상 환경에 requirements.txt의 dependencies 설치
> ```bash
> $ sudo apt-get install libmysqlclient-dev
> $ pip install -r requirements.txt
> ```
>
> - makemigrations / migrate 명령어를 통해 MySQL에 Table 생성
> ```bash
> $ python manage.py makemigrations
> $ python manage.py migrate
> ```
>
> - migrate 작업 완료됐으면 서버 실행
> ```bash
> $ python manage.py runserver
> ```
>
> - 웹 브라우저로 접속
>   - [http://localhost:8000/](http://localhost:8000/)
