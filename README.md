표 츄# 📒 Gist 기반 자동 블로그 발행 시스템 만들기 프로젝트

## 📌 프로젝트 개요

* **목표**: GitHub Gist에 마크다운 글을 작성하면 → GitHub Pages 블로그에 자동 발행되도록 구축.
* **핵심 아이디어**:

  * 글 관리 = GitHub Gist
  * 변환 & 배포 = GitHub Actions
  * 블로그 엔진 = Jekyll + GitHub Pages

* **구조**: GitHub Gist → GitHub Actions → Jekyll → GitHub Pages → 블로그 발행

* **핵심 코드**:

  * `_config.yml` : Jekyll 설정 (`jekyll-gist`, `jekyll-feed`, `jekyll-seo-tag`)
  * `pages.yml` : 정적 사이트 기본 배포
  * `gist-to-posts.yml` : Gist → `_posts` 변환 → Jekyll 빌드/배포 → (옵션) 외부 블로그 크로스포스트
---

## 🏗️ 주요 구성 요소

### 1. Jekyll 설정 (`_config.yml`)

* 블로그 기본 설정:

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
* **`jekyll-gist` 플러그인**: 블로그 글에서 Gist 임베드 가능.
* **`jekyll-feed`, `jekyll-seo-tag`**: RSS 피드와 SEO 메타 태그 자동 생성.

---

### 2. GitHub Actions 워크플로우

#### ✅ `pages.yml`

* 레포의 루트 파일을 **정적 사이트로 배포**.
* `actions/checkout`, `actions/upload-pages-artifact`, `actions/deploy-pages` 사용.
* 기본 Jekyll Pages 배포 담당.

#### ✅ `gist-to-posts.yml`

* 핵심 자동화: **Gist → `_posts` 변환** + **Jekyll 빌드 & 배포**.
* 동작 방식:

  1. 매일 00:07 UTC, 또는 `main` 브랜치 푸시, 또는 수동 실행 시 트리거됨.
  2. Python 스크립트 실행:

     * Gist API로 `songmac` 계정의 Gist 목록 가져옴.
     * `.md` 파일을 찾고, 제목/날짜/슬러그/Front Matter 생성.
     * `_posts/`에 Jekyll 포스트 파일로 저장.
  3. Jekyll 빌드 후 GitHub Pages에 배포.
  4. (선택) 네이버/티스토리 블로그에도 크로스 포스팅.

---

## ⚙️ 자동 포스팅 방법

1. **Gist에 글 작성**

   * 마크다운(`.md`) 파일 생성.
   * Gist 설명에 `[blog]` 태그를 달면 자동으로 포스트 변환됨.
   * 이미지 파일을 같이 업로드하면, 본문 내에서 자동으로 raw URL로 변환됨.

2. **GitHub Actions 실행**

   * 스케줄러(매일 00:07 UTC) 자동 실행.
   * 또는 레포에 push → 자동 실행.
   * 또는 수동으로 워크플로우 실행 가능.

3. **자동 변환 & 배포**

   * Gist 글 → `_posts/YYYY-MM-DD-title.md` 생성.
   * Jekyll 빌드 → `_site` 생성.
   * GitHub Pages에 자동 배포 → 블로그에 반영됨.

4. **(옵션) 외부 블로그 동기화**

   * 시크릿 토큰을 설정해 두면 네이버/티스토리에 최신 글 자동 업로드.

---

## 🚀 사용법 요약

1. **Gist에 글 작성** (Markdown)
   예:

   ```
   # 블로그 글 제목
   본문 내용...
   ```

   Gist 설명: `[blog] tags: python, tip`

2. **기다리면 자동 발행**

   * GitHub Actions가 돌면서 Jekyll 포스트 생성 & 배포.
   * [https://songmac.github.io](https://songmac.github.io) 에서 확인 가능.

---


## 📌 앞으로 할 일 (To-do / 리마인드)

### 수정 중인 사항

* [ ] **gitlog에 자동 포스팅 연동 실패** -> 이전 세팅으로 다시 되돌리고 연동 업데이트 시간도 변경해야함

### 🔧 기술적 개선

* [ ] **Gist 포스트 예쁘게 꾸미기** → Markdown 스타일, 이미지 관리, 태그/카테고리 정리
* [ ] **개인 서버 구축** → 포트폴리오 웹사이트 직접 호스팅, GitHub Pages와 연동 or 독립 배포
* [ ] **크로스포스팅 강화** → 티스토리/네이버 블로그 발행 로직 안정화

### 🌐 연결할 서비스

* [ ] **Notion 연동** → Notion 글 → Gist 자동 전송 파이프라인
* [ ] **Slack 알림** → 새 글 발행 시 Slack 채널 알림
* [ ] **메일 발송** → 발행 글 자동 뉴스레터 발송

### 📊 프로젝트 관리

* [ ] **칸반보드 정리** (GitHub Projects, Jira, Trello 중 선택)

  * To Do / In Progress / Done으로 관리
  * 블로그 글 주제 & 개발 태스크를 같이 관리

### 🚀 Publish 대상

* [ ] **GitHub Pages** (메인 블로그)
* [ ] **티스토리** (자동 포스팅)
* [ ] **네이버 블로그** (자동 포스팅)









