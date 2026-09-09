// Ô nhập OTP: gõ một số là nhảy sang ô kế, Backspace ở ô trống thì lùi lại,
// dán cả mã 6 số thì tự rải ra các ô. Gắn bằng event uỷ quyền trên document
// nên không phụ thuộc thời điểm runtime dựng xong DOM.
(function () {
  function boxes(el) {
    return Array.prototype.slice.call(
      el.parentNode.querySelectorAll('input.otp-box'));
  }

  document.addEventListener('input', function (e) {
    var el = e.target;
    if (!el.classList || !el.classList.contains('otp-box')) return;
    el.value = (el.value || '').replace(/\D/g, '').slice(0, 1);
    if (!el.value) return;
    var list = boxes(el), i = list.indexOf(el);
    if (i > -1 && i < list.length - 1) list[i + 1].focus();
  });

  document.addEventListener('keydown', function (e) {
    var el = e.target;
    if (!el.classList || !el.classList.contains('otp-box')) return;
    var list = boxes(el), i = list.indexOf(el);
    if (e.key === 'Backspace' && !el.value && i > 0) {
      e.preventDefault();
      list[i - 1].focus();
      list[i - 1].value = '';
    }
    if (e.key === 'ArrowLeft' && i > 0) { e.preventDefault(); list[i - 1].focus(); }
    if (e.key === 'ArrowRight' && i < list.length - 1) { e.preventDefault(); list[i + 1].focus(); }
  });

  document.addEventListener('paste', function (e) {
    var el = e.target;
    if (!el.classList || !el.classList.contains('otp-box')) return;
    var txt = (e.clipboardData || window.clipboardData).getData('text') || '';
    var digits = txt.replace(/\D/g, '');
    if (!digits) return;
    e.preventDefault();
    var list = boxes(el), i = list.indexOf(el);
    for (var k = 0; k < digits.length && i + k < list.length; k++) {
      list[i + k].value = digits[k];
    }
    list[Math.min(i + digits.length, list.length - 1)].focus();
  });
})();
