"""네이버 블로그 RSS를 읽어 건강이야기 페이지(pages/health.html)의 글 목록을 갱신합니다.

사용법 (저장소 맨 위 폴더에서):  python tools/update_blog.py
- 썸네일은 images/blog/ 에 내려받아 홈페이지에서 직접 제공합니다(네이버 이미지 외부 링크 차단 대비).
- pages/health.html 의 <!-- BLOG:START --> ~ <!-- BLOG:END --> 사이만 바꿉니다.
"""
import email.utils
import html
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET

BLOG_ID = "haniworkpro"
MAX_POSTS = 12
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "pages" / "health.html"
IMG_DIR = ROOT / "images" / "blog"
UA = {"User-Agent": "Mozilla/5.0"}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def main():
    root = ET.fromstring(fetch(f"https://rss.blog.naver.com/{BLOG_ID}.xml"))
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    cards = []
    for item in root.find("channel").findall("item")[:MAX_POSTS]:
        title = item.findtext("title").strip()
        link = item.findtext("link").split("?")[0]
        post_no = link.rstrip("/").split("/")[-1]
        date = email.utils.parsedate_to_datetime(item.findtext("pubDate")).strftime("%Y-%m-%d")
        desc = item.findtext("description") or ""
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(desc))).strip()
        summary = text[:90].rstrip() + ("…" if len(text) > 90 else "")

        img_html = '<div class="post-thumb post-thumb-empty" aria-hidden="true"></div>'
        srcs = re.findall(r'src="([^"]+)"', desc)
        if srcs:
            ext = ".jpg" if re.search(r"\.jpe?g", srcs[0], re.I) else ".png"
            local = IMG_DIR / f"{post_no}{ext}"
            if not local.exists():
                try:
                    local.write_bytes(fetch(srcs[0].split("?")[0] + "?type=w2"))
                except Exception as e:  # 썸네일 실패는 글 목록을 막지 않음
                    print("썸네일 실패:", link, e)
            if local.exists():
                img_html = f'<img class="post-thumb" src="../images/blog/{local.name}" alt="" loading="lazy">'

        cards.append(
            f'<a class="post" href="{html.escape(link)}" target="_blank" rel="noopener">'
            f"{img_html}"
            f'<div class="post-body"><time datetime="{date}">{date.replace("-", ".")}</time>'
            f"<h3>{html.escape(title)}</h3><p>{html.escape(summary)}</p></div></a>"
        )

    block = "\n".join(cards) or '<div class="posts-empty">글이 준비되는 대로 이곳에 표시됩니다.</div>'
    page = PAGE.read_text(encoding="utf-8")
    new, n = re.subn(r"(<!-- BLOG:START -->).*?(<!-- BLOG:END -->)",
                     lambda m: m.group(1) + "\n" + block + "\n" + m.group(2), page, flags=re.S)
    if n != 1:
        raise SystemExit("pages/health.html 에서 BLOG:START/END 표시를 찾지 못했습니다.")
    PAGE.write_text(new, encoding="utf-8")
    print(f"글 {len(cards)}개 반영")


if __name__ == "__main__":
    main()
