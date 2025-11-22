# hackerton-dswu
--2025 Duksung Hackerton Team Project--

**IT분야 적성 테스트 & 게시판 서비스 CONEXT**는 IT 분야 적성 테스트와 커뮤니티 기능을 결합한 플랫폼으로, IT 분야에 관심 있는 취업 준비생과 종사자들이 함께 소통하며 취업 정보와 경험을 공유할 수 있습니다.

## 주요 기능
### 1. IT 분야 적성 테스트
- 프론트엔드, 백엔드, AI, IoT 등 분야별 테스트 제공
- 10개의 질문을 통해 나에게 맞는 IT 분야 추천
### 2. 회원 시스템
- 회원가입 / 로그인
- JWT 및 세션 기반 인증
### 3. 게시판
- 직무별 Q&A 게시판
- 글 작성 / 수정 / 삭제
- 댓글 / 좋아요 / 스크랩
- 익명 작성 가능
- 인기글 / 스크랩한 글 / 내가 쓴 글 / 내가 쓴 댓글 보기

## 기술 스택
- Frontend: HTML, CSS, JavaScript
- Backend: Django, Django REST Framework
- Auth: 세션 / JWT
- DB: SQLite

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
## 프로젝트 구조
```
hackerton-dswu/
├── accounts/           # 회원 관리
│   ├── models.py      # User 모델
│   ├── views.py       # 회원가입, 로그인
│   └── serializers.py
├── board/             # 게시판
│   ├── models.py      # Post, Comment 모델
│   ├── views.py       # 게시글 CRUD
│   └── urls.py
├── it_test/           # IT 적성 테스트
│   ├── models.py      # Question, Field 모델
│   └── views.py       # 테스트 로직
├── templates/         # HTML 템플릿
├── static/           # CSS, JS, 이미지
└── manage.py
```

## 특징
- IT 직무 적성 테스트와 커뮤니티 기능을 결합한 플랫폼
- 직무 적성 테스트 결과 제공 -> 게시판 연결 -> 실시간 Q&A 가능
- 익명 게시글 작성 가능 → 자유로운 정보 공유
- JWT + 세션 기반 인증으로 보안 강화
- 좋아요 / 스크랩 기능으로 콘텐츠 큐레이션
- 내 활동 관리 (내 글, 내 댓글, 내 스크랩)
- 카테고리별 게시판 및 인기글 정렬
- RESTful API 제공 (Django REST Framework)


## API 명세
### 게시판
- `GET /api/board/` : 전체 게시글 목록
- `GET /api/board/<str:category>/` : 카테고리별 게시글 목록
- `POST /create/` : 게시글 작성
- `GET /<int:pk>/` : 게시글 상세
- `PUT /<int:pk>/edit/` : 게시글 수정
- `DELETE /<int:pk>/delete/` : 게시글 삭제
- `POST /<int:pk>/like-toggle/` : 좋아요 토글
- `POST /<int:pk>/scrap-toggle/` : 스크랩 토글

### 댓글
- `POST /<int:post_pk>/comment/create/` : 댓글 작성
- `POST /<int:post_pk>/comment/create/reply/<int:parent_pk>/` : 대댓글 작성
- `POST /comment/<int:pk>/like-toggle/` : 댓글 좋아요 토글
- `PUT /comment/edit/<int:pk>/` : 댓글 수정
- `DELETE /comment/delete/<int:pk>/` : 댓글 삭제

### 사용자 관련
- `GET /my-posts/` : 내가 쓴 글
- `GET /my-comments/` : 내가 쓴 댓글
- `GET /my-scraps/` : 내가 스크랩한 글

## 향후 개선 사항
- 프로필 세부 수정 페이지
- AI 도입 - 개개인 맞춤 공모전, 강연 및 대외활동 추천
- 투두리스트
- 검색 및 채팅 기능 구현

## 팀원
- 조채인 - 프론트 ([choin719-stack](https://github.com/choin719-stack))
- 명지민 - 프론트 ([jimin414](https://github.com/jimin414))
- 우서윤 - 백엔드 ([wooarling](https://github.com/wooarling))
- 윤주영 - 백엔드 ([YJY932](https://github.com/YJY932))
- 장유진 - 기획디자인 ([yujinonline](https://github.com/yujinonline))
