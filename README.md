# hackerton-dswu
--2025 Duksung Hackerton Team Project--

**IT분야 적성 테스트 & 게시판 서비스**
CONEXT는 IT 분야에 관심 있는 여성들이 소통하고 정보를 공유할 수 있는 플랫폼입니다.

## 주요 기능
- IT 분야 적성 테스트(프론트엔드, 벡엔드, AI, 사물인터넷 등)
- 회원가입 / 로그인(JMT 인증)
- 게시판 CRUD(글 작성, 수정, 삭제, 댓글, 좋아요, 스크랩)
- 인기글 / 스크랩한 글 / 내가 쓴 글 / 내가 쓴 댓글

## 기술 스택
- Frontend: HTML, CSS, JavaScript
- Backend: Django, Django REST Framework
- Auth: 세션 / JWT
- DN: SQLite

## 설치 & 실행
```bash
1. 클론
git clone https://github.com/wooarling/hackerton-dswu.git
cd hackerton-dswu
2. 가상환경 생성/활성화
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate.bat   # Windows(CMD)
.\venv\Scripts\Activate.ps1   # Windows(PowerShell)
3. 패키지 설치
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
4. 마이그레이션/서버 실행
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 팀원
- 조채인 - 프론트 ([choin719-stack](https://github.com/choin719-stack))
- 명지민 - 프론트 ([jimin414](https://github.com/jimin414))
- 우서윤 - 백엔드 ([wooarling](https://github.com/wooarling))
- 윤주영 - 백엔드 ([YJY932](https://github.com/YJY932))
- 장유진 - 기획디자인 ([yujinonline](https://github.com/yujinonline))

## 스크린샷
(추가)
