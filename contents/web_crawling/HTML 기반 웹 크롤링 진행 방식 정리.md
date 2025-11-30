# 웹 크롤링 전략 전체 흐름 정리

## 1. 웹페이지 데이터 로딩 구조 이해

### 1-1. HTML 기반 렌더링

- 서버가 HTML 문서를 생성하여 클라이언트에 전달하는 방식임.
- HTML 요소(Element 탭)에 원하는 데이터가 즉시 보임.
- BeautifulSoup으로 바로 파싱 가능함.

### 1-2. HTML 내부 inline JSON 기반 렌더링

- HTML 파일 내부에 **JSON 데이터가 스크립트 태그 또는 data-\* 속성 형태로 포함되는 방식**임.
- 예시

  ```html
  <script>
    window.__DATA__ = { name: "selena" };
  </script>

  <script type="application/json" id="config">
    { "page": 1, "items": [1, 2, 3] }
  </script>

  <div data-info='{"a":1}'></div>
  ```

- 이 경우 **별도의 JSON 파일은 존재하지 않음**.
- BeautifulSoup으로 HTML을 파싱하여 JSON 문자열만 추출하면 됨.

### 1-3. 비동기(API 기반) 렌더링

- HTML에는 데이터가 없음.
- JS가 페이지 로드 후 서버에 별도 요청을 보내 JSON을 가져오고 이를 DOM에 삽입함.
- 이때 사용되는 요청 방식이 **Fetch/XHR**임.

  - Fetch/XHR: 자바스크립트에서 서버에 비동기 요청을 보내 JSON 데이터를 가져오는 기술임.
  - 예: `fetch()`, `axios.get()`, `XMLHttpRequest`

- HTML Response에는 데이터가 없고, **Network → Fetch/XHR 탭에 JSON API 요청이 나타남**.
- API endpoint를 직접 호출하여 크롤링할 수 있음.

---

## 2. 데이터의 출처 판별 절차

### 2-1. Element(DOM) 확인

- 여기에서 데이터가 보이면 단순 HTML 기반임.

### 2-2. HTML Response 확인

- Network → Doc → Response 탭
- HTML 내부에 JSON이 존재하면 inline JSON 기반임.
- 없다면 비동기 요청을 통해 가져오는 구조임.

#### 2-2-1. inline JSON 크롤링 방법

- BeautifulSoup으로 HTML 파싱
- script 태그나 data-\* 속성에서 JSON 문자열 추출 후 `json.loads()`로 구조화
- 별도 JSON 파일 존재하지 않음 → HTML 파일이 곧 데이터 원본임.

### 2-3. Fetch/XHR 요청 확인

- Network → Fetch/XHR 필터에서 JSON 응답 확인
- JSON이 있다면 비동기로 로드된 데이터임
- API URL을 직접 호출해 크롤링하면 됨.

> 참고. 네트워크 탭 필터 정리 (표)

| 필터명        | 의미                   | 상세 설명                                                                           |
| ------------- | ---------------------- | ----------------------------------------------------------------------------------- |
| **Fetch/XHR** | 비동기 요청(AJAX)      | JS가 서버와 통신해 데이터를 가져오는 fetch/axios/XHR 요청이며 크롤링 시 가장 중요함 |
| **Doc**       | HTML 문서 요청         | 페이지의 기본 문서 요청을 보여줌                                                    |
| **CSS**       | 스타일시트 요청        | `.css` 관련 리소스를 보여줌                                                         |
| **JS**        | 자바스크립트 파일 요청 | `.js` 로드 상태 확인 가능함                                                         |
| ...           | ...                    | ...                                                                                 |
| **Other**     | 기타 요청              | 분류되지 않은 리소스                                                                |

#### 2-3-1. 비동기(JSON/API) 크롤링 방법

- Fetch/XHR에서 API endpoint를 찾음
- 해당 URL을 requests 등으로 직접 호출
- JSON을 그대로 수집 가능함
- 특히 SPA 사이트에서 거의 필수 전략임
  - SPA(Single Page Application)f 란?
    - 웹사이트 전체가 하나의 HTML 기반으로 동작함
    - 화면 전환은 JS가 DOM을 교체해 수행함
    - 모든 데이터는 **Fetch/XHR API 요청**으로 불러옴
    - React/Vue/Angular 기반 웹사이트의 기본 구조임
    - 이 때문에 SPA 크롤링은 **API 크롤링이 핵심**임

---

## 3. 네트워크 흐름 구조도

```
 ┌──────────────────────────┐
 │     웹페이지 접속          │
 └────────────┬─────────────┘
              ▼
 ┌──────────────────────────┐
 │ DOM(Element) 확인         │
 └───────┬──────────────────┘
   데이터 존재? ───────► HTML 직접 파싱
              │
              ▼
 ┌──────────────────────────┐
 │ HTML Response 확인        │
 │ (inline JSON 존재 여부)   │
 └───────┬──────────────────┘
   inline JSON? ──────────► BeautifulSoup으로 JSON 추출
              │
              ▼
 ┌──────────────────────────┐
 │ Fetch/XHR 요청 확인       │
 │ (비동기 JSON/API)         │
 └───────┬──────────────────┘
   API 발견? ────────────► API 직접 요청하여 JSON 크롤링
              │
              ▼
 ┌──────────────────────────┐
 │ JS 렌더링 엔진 사용        │
 │ (Selenium / Playwright)  │
 │  자바스크립트 실행 기반     │
 └──────────────────────────┘
```

> 참고. JS 렌더링 엔진(Selenium/Playwright)

- 실제 브라우저처럼 동작하여 **자바스크립트를 실행하고 최종 DOM을 구성해주는 자동화 엔진**
  - 웹사이트가 JS 실행 후 DOM을 동적으로 구성하는 경우(대표적으로 SPA) requests + BeautifulSoup 방식으로는 데이터를 받을 수 없음.
  - 이때 Selenium/Playwright는 브라우저를 실제로 켬 → JS 로직을 실행함 → 렌더링된 최종 DOM을 제공.
- 따라서 Selenium/Playwright JS로 렌더링되는 데이터를 크롤링할 때 필수적임.
