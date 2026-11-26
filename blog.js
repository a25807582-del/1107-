/* 건강이야기 - 네이버 블로그 연동 설정
   BLOG_ID 에 네이버 블로그 아이디(blog.naver.com/아이디)를 넣으면
   건강이야기 페이지에 "네이버 블로그 바로가기" 버튼이 나타납니다.
   (글 목록은 tools/update_blog.py 로 갱신합니다.)
   예) window.BLOG_ID = 'myblogid'; */
window.BLOG_ID = 'ydj1075';

(function () {
  var id = window.BLOG_ID;
  if (!id) return;
  document.querySelectorAll('[data-blog]').forEach(function (a) {
    a.href = 'https://blog.naver.com/' + encodeURIComponent(id);
    a.target = '_blank'; a.rel = 'noopener'; a.hidden = false;
  });
})();
