# 📒 Gist 기반 자동 블로그 발행 시스템 만들기 프로젝트

## 📌 프로젝트 개요

- **목표**: GitHub Gist에 마크다운 글을 작성하면 → GitHub Pages 블로그에 자동 발행되도록 구축.
- **핵심 아이디어**:

  - 글 관리 = GitHub Gist
  - 변환 & 배포 = GitHub Actions
  - 블로그 엔진 = Jekyll + GitHub Pages

- **구조**: GitHub Gist → GitHub Actions → Jekyll → GitHub Pages → 블로그 발행

- **핵심 코드**:

  - `_config.yml` : Jekyll 설정 (`jekyll-gist`, `jekyll-feed`, `jekyll-seo-tag`)
  - `gist-to-posts.yml` : Gist → `_posts` 변환 → Jekyll 빌드/배포 → (옵션) 외부 블로그 크로스포스트

---

## 🏗️ 주요 구성 요소

### 1. Jekyll 설정 (`_config.yml`)

- 블로그 기본 설정:

  ```yaml
  title: "songmac blog"
  description: "Gist-powered notes"
  url: "https://songmac.github.io"
  theme: minima
  plugins:
    - jekyll-feed
    - jekyll-seo-tag
    - jekyll-gist
  ```

- **`jekyll-gist` 플러그인**: 블로그 글에서 Gist 임베드 가능.
- **`jekyll-feed`, `jekyll-seo-tag`**: RSS 피드와 SEO 메타 태그 자동 생성.

---

### 2. GitHub Actions 워크플로우

#### ✅ `gist-to-posts.yml`

- 핵심 자동화: **Gist → `_posts` 변환** + **Jekyll 빌드 & 배포**.
- 동작 방식:

  1. 매일 00:07 UTC, 또는 `main` 브랜치 푸시, 또는 수동 실행 시 트리거됨.
  2. Python 스크립트 실행:

     - Gist API로 `songmac` 계정의 Gist 목록 가져옴.
     - `.md` 파일을 찾고, 제목/날짜/슬러그/Front Matter 생성.
     - `_posts/`에 Jekyll 포스트 파일로 저장.

  3. Jekyll 빌드 후 GitHub Pages에 배포.
  4. (선택) 네이버/티스토리 블로그에도 크로스 포스팅.

---

## ⚙️ 자동 포스팅 방법

1. **Gist에 글 작성**

   - 마크다운(`.md`) 파일 생성.

2. **GitHub Actions 실행**

   - 스케줄러(매일 00:07 UTC) 자동 실행.
   - 또는 레포에 push → 자동 실행.
   - 또는 수동으로 워크플로우 실행 가능.

3. **자동 변환 & 배포**

   - Gist 글 → `_posts/YYYY-MM-DD-title.md` 생성.
   - Jekyll 빌드 → `_site` 생성.
   - GitHub Pages에 자동 배포 → 블로그에 반영됨.

4. **(옵션) 외부 블로그 동기화**

   - 시크릿 토큰을 설정해 두면 네이버/티스토리에 최신 글 자동 업로드.

---

## 🚀 사용법 요약

1. **Gist에 글 작성** (Markdown)
   예:

   ```
   # 블로그 글 제목
   본문 내용...
   ```

   - 제목: (#) 인덱스를 이용해 글을 작성하면 제목은 자동으로 인식되어 입력됨
   - 설명: 현재는 해당 글에 대한 간략한 설명은 Gist에서 직접 입력
     - 마크다운으로 작성했을 때 요약 탭이 존재하도록 하고 그걸 설명에 임베딩 할 수 있도록 수정하는 방향 생각중

2. **기다리면 자동 발행**

   - GitHub Actions가 돌면서 Jekyll 포스트 생성 & 배포.
   - [https://songmac.github.io](https://songmac.github.io) 에서 확인 가능.

---

## 📌 앞으로 할 일

### 🔧 기술적 개선

- [ ] **Gist 포스트 예쁘게 꾸미기** → Markdown 스타일, 이미지 관리, 태그/카테고리 정리
- [ ] **AWS, Docker를 이용한 개인 서버 구축** → 포트폴리오 웹사이트 직접 호스팅, GitHub Pages와 연동 or 독립 배포 (조금 더 기술적 방법에 대해 구체화 필요)

### 🌐 연결할 플랫폼 / 서비스

- [ ] **티스토리/네이버 블로그 크로스포스팅** → 발행 로직 안정화
- [ ] **Notion 연동** → Notion 글 → Gist 자동 전송 파이프라인
- [ ] **Slack 알림** → 새 글 발행 시 Slack 채널 알림
- [ ] **메일 발송** → 발행 글 자동 뉴스레터 발송
