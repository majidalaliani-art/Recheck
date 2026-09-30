const sendBtn = document.querySelector('button[value="send_otp"]');
const verifyBtn = document.querySelector('button[value="verify_otp"]');
const errorDiv = document.getElementById("error-msg");

if (!errorDiv) throw "";

if (sendBtn) {
  sendBtn.form.addEventListener("submit", function (event) {
    const phoneValue = document.getElementById("id_phone").value.trim();
    if (!/^\d+$/.test(phoneValue)) {
      event.preventDefault();
      errorDiv.textContent = "عذراً، يجب أن يحتوي رقم الهاتف على أرقام فقط";
      errorDiv.classList.remove("d-none");
      errorDiv.classList.add("d-block");
    } else if (phoneValue.length !== 10 || !phoneValue.startsWith("05")) {
      event.preventDefault();
      errorDiv.textContent = "عذراً، يجب أن يتكون رقم الهاتف من 10 أرقام ويبدأ بـ 05";
      errorDiv.classList.remove("d-none");
      errorDiv.classList.add("d-block");
    }
  });
}

if (verifyBtn) {
  verifyBtn.form.addEventListener("submit", function (event) {
    const otpValue = document.getElementById("id_otp").value.trim();
    if (!/^\d+$/.test(otpValue)) {
      event.preventDefault();
      if (!otpValue) return;
      errorDiv.textContent = "عذراً، يجب أن يحتوي رمز التحقق على أرقام فقط";
      errorDiv.classList.remove("d-none");
      errorDiv.classList.add("d-block");
    } else if (otpValue.length !== 4) {
      event.preventDefault();
      errorDiv.textContent = "عذراً، يجب أن يتكون رمز التحقق من 4 أرقام";
      errorDiv.classList.remove("d-none");
      errorDiv.classList.add("d-block");
    }
  });
}









document.addEventListener("DOMContentLoaded", function () {
  const resetBtn = document.getElementById("reset-btn");
  const countdownEl = document.getElementById("countdown");
  const countdown = document.getElementById("time-countdown");
  let timeLeft = window.djangoTimeLeft ;


  if (resetBtn && countdownEl) {

    resetBtn.disabled = true;
    resetBtn.style.opacity = "0.5";
    resetBtn.style.cursor = "not-allowed";

    // 2. تشغيل دالة العداد التنازلي كل ثانية
    const timer = setInterval(function () {
      timeLeft--;
      countdownEl.textContent = timeLeft;


      if (timeLeft <= 0) {
        clearInterval(timer);
        resetBtn.disabled = false;
        resetBtn.style.opacity = "1";
        resetBtn.style.cursor = "pointer";
        resetBtn.innerHTML = "إعادة إرسال الكود";
        countdown.classList.add("d-none");
      }
    }, 1000);
  }
});
