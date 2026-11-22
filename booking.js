/* 네이버 예약 연결 설정
   아래 BOOKING_URL 에 네이버 예약 주소를 한 번만 넣으면
   모든 페이지의 "네이버 예약하기" 버튼과 메뉴 "예약문의"가 자동으로 그 주소로 연결됩니다.
   (비워 두면 예약 버튼은 숨겨지고, 메뉴 "예약문의"는 '오시는 길'로 이동합니다.)
   예) window.BOOKING_URL = 'https://booking.naver.com/booking/13/bizes/000000';  */
window.BOOKING_URL = '';

(function () {
  var u = window.BOOKING_URL;
  if (!u) return;
  document.querySelectorAll('[data-booking]').forEach(function (a) {
    a.href = u; a.target = '_blank'; a.rel = 'noopener'; a.hidden = false;
  });
})();
