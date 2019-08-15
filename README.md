# django-account-manager

#### 계좌관리 및 거래 시뮬레이션 웹 어플리케이션

<kbd>
  <img src="./screenshots/main.gif" alt="main" width='100%'/>
</kbd>

<br/>
<br/>


## *Introduction*

### Summary

> - Project 소개
>   - 계좌관리 및 거래 시뮬레이션 웹 어플리케이션입니다.
>   - 사용자당 최대 5개의 계좌를 계설할 수 있으며, 주 계좌를 설정/변경할 수 있습니다.
>   - 계좌의 종류는 총 3가지 (일반/급여/적금) 존재하며, 각각의 종류마다 출금 한도가 존재합니다. 
>   - 입금 한도는 없으며, 출금 한도는 다음과 같습니다.
>     - 일반 : 1회 30만원 / 1일 30만원
>     - 급여: 1회 1,000만원 / 1일 1억원
>     - 적금: 출금 불가
> 
>   - 계좌간 이체가 가능하며, 종류가 다른 계좌로의 이체시 수수료 500원이 부과됩니다. 
>   - 다른 종류의 계좌로 이체시 하루 3건까지는 수수료가 면제됩니다.
>  <br/>
> 
> - BACKEND (Djagno)
>   - Django를 이용하여 구현
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
> <kbd>
>   <img src="./screenshots/database_schema.png" alt="database_schema" width='100%'/>
> </kbd>
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
> mysql> create schema account_manager;
> ```

### Install dependencies
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

### Generate data
>
> - Mysql DB 마이그레이션 또는 loaddata를 통한 시뮬레이션 데이터셋 제공 추가해야함
> 

## *Report implemented assignment*

### 회원 가입 / 로그인
> 
> <kbd>
>   <img src="./screenshots/login_signup.gif" alt="login_signup" width='100%'/>
> </kbd>
> 
> - Django 프레임워크의 django.contrib.auth.model 을 사용하여 CustomUser 모델을 생성했으며
> 
> - Django 프레임워크의 django.contrib.auth.forms 를 사용하여 회원가입/로그인 Form을 구현

### 계좌 개설
>
> <kbd>
>   <img src="./screenshots/create_account.gif" alt="create_account" width='100%'/>
> </kbd>
> 
> - 로그인후 우측 상단의 `계좌 생성` 버튼을 클릭하여 새로운 계정 생성
> 
> - 계좌번호, 초기 잔액, 은행, 계좌 형태, 주 계좌 여부를 입력하고 계정 생성

### 주 계좌 변경
>
> <kbd>
>   <img src="./screenshots/modify_main_account.gif" alt="modify_main_account" width='100%'/>
> </kbd>
> 
> - 주 계좌를 변경하기 위해 우측 상단의 `주 계좌 변경` 버튼 또는 현재 주 계좌의 `주 계좌` 버튼을 클릭
> 
> - 변경하고자 하는 계좌 하단의 `주 계좌로 선택` 버튼 또는 `은행 명` 클릭하여 변경

### 거래
>
> **입금 (Deposit)**
>
> <kbd>
>   <img src="./screenshots/deposit.gif" alt="deposit" width='100%'/>
> </kbd>
> 
> - 메인 페이지에서 입금 하고싶은 계좌 우측 하단의 `입금` 버튼 클릭
> 
> - 입금하고자 하는 금액 입력한 후 `Submit` 버튼 클릭
> 
> - 계좌의 잔액이 추가되고, 최근 거래 목록에 입금 기록이 생겼는지 확인
>
> <br>
> 
> **출금 (Withdraw)**
>
> <kbd>
>   <img src="./screenshots/withdraw.gif" alt="withdraw" width='100%'/>
> </kbd>
> 
> - 메인 페이지에서 출금 하고싶은 계좌 우측 하단의 `출금` 버튼 클릭
> 
> - 출금하고자 하는 금액 입력한 후 `Submit` 버튼 클릭
> 
> - 계좌의 잔액이 감소되고, 최근 거래 목록에 출금 기록이 생겼는지 확인
>
> <br>
> 
> **이체 (Transfer) - 자신의 계좌에 송금**
>
> <kbd>
>   <img src="./screenshots/transfer_me.gif" alt="transfer_me" width='100%'/>
> </kbd>
> 
> - 메인 페이지에서 이체 하고싶은 계좌 우측 하단의 `이체` 버튼 클릭
> 
> - 이체하고자 하는 계좌 정보와 금액 입력한 후 `Submit` 버튼 클릭
> 
> - 출금/입금 계좌의 잔액 변화와, 최근 거래 목록에 이체 기록이 생겼는지 확인
>
> <br>
> 
> **이체 (Transfer) - 타 새용자 계좌에 송금**
>
> <kbd>
>   <img src="./screenshots/transfer_you.gif" alt="transfer_you" width='100%'/>
> </kbd>
> 
> - 메인 페이지에서 이체 하고싶은 계좌 우측 하단의 `이체` 버튼 클릭
> 
> - 이체하고자 하는 계좌 정보와 금액 입력한 후 `Submit` 버튼 클릭
> 
> - 이체를 보낸 계좌의 잔액 감소와, 최근 거래 목록에 이체 기록이 생겼는지 확인
>
> - 로그아웃 -> 타 사용자 로그인 후
>
> - 이체 받은 계좌의 잔액 증가와, 최근 거래 목록에 이체 기록이 생겼는지 확인

### 제약 사항
>
> **계좌 개수 한도**
>
> <kbd>
>   <img src="./screenshots/limit_account.gif" alt="limit_account" width='100%'/>
> </kbd>
> 
> - `계좌 생성` 작업을 통해 계좌를 5개 이상으로 생성
> 
> - 6번째 계좌 생성시 생성된 에러 메시지 확인
>
> <br>
> 
> **출금 한도**
>
> <kbd>
>   <img src="./screenshots/limit_withdraw.gif" alt="limit_withdraw" width='100%'/>
> </kbd>
> 
> - 출금할 계좌의 `은행 이름` 버튼 클릭하여 상세정보 들어가서, `하루 출금 허용 잔여 금액` 확인
>
> - `하루 출금 허용 잔여 금액`만큼 출금한 후, 출금 버튼 비활성화 되는지 확인
> 
> - 해당 계좌의 상세정보 다시 들어가서, `하루 출금 허용 잔여 금액` 0 됐는지 확인
> 
> <br>
> 
> **이체 수수료**
>
> <kbd>
>   <img src="./screenshots/transfer_commission.gif" alt="transfer_commission" width='100%'/>
> </kbd>
> 
> - 이체할 계좌의 `은행 이름` 버튼 클릭하여 상세정보 들어가서, `하루 무료 계좌이체 잔여 횟수` 확인
> 
> - `하루 출금 허용 잔여 금액`만큼 이체한 후, 이체 버튼의 색깔이 변하는 확인
> 
> - 해당 계좌의 상세정보 다시 들어가서, `하루 무료 계좌이체 잔여 횟수` 0 됐는지 확인
>
> - 이후 다른 종류의 이체에서 수수료 500원이 붙는지 확인

### 내역 조회
>
> **특정 계좌 거래 내역 조회**
>
> <kbd>
>   <img src="./screenshots/account_history.gif" alt="account_history" width='100%'/>
> </kbd>
> 
> - 거래 내역을 확인하고 싶은 계좌의 `내역 조회` 버튼을 클릭하여 입금, 출금, 이체 내역 확인
> 
> - 모든 내역들이 최근 순으로 조회 되는지 확인
> 
> <br>
> 
> **모든 계좌 거래 내역 조회**
>
> <kbd>
>   <img src="./screenshots/account_history_all.gif" alt="account_history_all" width='100%'/>
> </kbd>
> 
> - 우측 상단의 `조회` 버튼을 클릭하여 소지하고 있는 계좌들의 내역 확인
> 
> - 모든 내역들이 최근 순으로 조회 되는지 확인
> 
> <br>
> 
> **타임라인**
>
> <kbd>
>   <img src="./screenshots/timeline.gif" alt="timeline" width='100%'/>
> </kbd>
> 
> - 우측 상단의 `타임라인` 버튼을 클릭하여 하루 단위로 분리 돼있는 거래 내역 확인
>
> - 해당 페이지에서 각 계좌의 `은행 명` 버튼 클릭시 해당 계좌의 상세정보 페이지로 이동

<br>

## *Addition Commentary*

### VCS
> 
> - 각 기능별 개발이 완료될 때 마다 적절히 git commit / push / pull 사용하며 진행했습니다.
> 
> - Github 저장소의 [Issue 등록 페이지](https://github.com/meh9184/django-account-manager/issues?q=is%3Aissue+is%3Aclosed)를 활용하여 개발 필요한 기능 정리해두고, 개발 완료시 close 하며 진행했습니다.
> 
> - 생성한 Issue 단위로 branch 생성하여 개발했고, 개발 완료시 master에서 merge 하며 진행했습니다.
> 

### Issues
> 
> - django-background-tasks를 사용하여 하루마다 이체 한도 숫자와 출금 한도량을 초기화하고 있지만, 백그라운드에서 실행되는 
> 
> - API timeout 및 이체 처리 시간 관련 작업은 제한된 시간안에 진행하지 못했습니다.
> 

### Tools for Windows OS Users
> - [WSL (Windows Subsystem for Linux)](https://docs.microsoft.com/ko-kr/windows/wsl/install-win10)
> - [VSCode](https://code.visualstudio.com/docs/?dv=win)
> - [Mysql Workbench](https://www.mysql.com/products/workbench/)
> - [Github](https://github.com/meh9184/django-account-manager/)
> 

<br/>

## *References*
> 
> - https://docs.djangoproject.com/ko/2.2/
> - https://docs.microsoft.com/ko-kr/windows/wsl/install-win10
