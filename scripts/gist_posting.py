import os
import re
import yaml
import pathlib
import requests

# 환경 변수로부터 사용자 가져오기(GitHub Actions에서 주입)
USER = os.environ["GH_USER"]
TOKEN = os.environ.get("GH_TOKEN")

POSTS = pathlib.Path("_posts")
POSTS.mkdir(exist_ok=True)

HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def fetch(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r


page = 1
while True:
    # Gist 목록을 페이지 단위로 가져오기
    data = fetch(
        f"https://api.github.com/users/{USER}/gists",
        {"page": page, "per_page": 100},
    ).json()

    if not data:
        break

    for g in data:
        files = g.get("files") or {}

        # .md 파일 찾기
        md = next(
            (v for v in files.values() if v["filename"].lower().endswith(".md")),
            None
        )
        if not md:
            continue

        # Gist Raw text 가져오기
        raw = fetch(md["raw_url"]).text

        # 제목 추출 (# 제목)
        m = re.search(r"^#\s+(.+)$", raw, re.M)
        title = m.group(1).strip() if m else md["filename"].split(".")[0]

        # 작성일 = Gist created_at 날짜 사용 권장
        created = g["created_at"][:10]

        # slug 생성
        slug = re.sub(r"[^a-z0-9\-]+", "-", title.lower()).strip("-") or g["id"]

        # Front Matter 생성
        front_matter = {
            "layout": "post",
            "title": title,
            "gist_id": g["id"],
            "original_gist": f"https://gist.github.com/{USER}/{g['id']}"
        }

        # Jekyll용 파일 이름
        filename = f"{created}-{slug}.md"
        path = POSTS / filename

        # front-matter가 이미 있다면 그대로 사용
        if raw.lstrip().startswith("---"):
            content = raw
        else:
            content = (
                "---\n"
                + yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False)
                + "---\n\n"
                + raw
            )

        path.write_text(content, encoding="utf-8")

    page += 1
