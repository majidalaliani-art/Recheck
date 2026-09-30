document.addEventListener("DOMContentLoaded", function () {
  const timerContainer = document.getElementById("countdown-timer");
  if (!timerContainer) return;

  const secondsEl = document.getElementById("timer-seconds");
  const minutesEl = document.getElementById("timer-minutes");
  const hoursEl = document.getElementById("timer-hours");
  const daysEl = document.getElementById("timer-days");

  const deadlineStr = timerContainer.getAttribute("data-deadline");
  const deadlineTime = new Date(deadlineStr).getTime();

  const timerInterval = setInterval(function () {
    const now = new Date().getTime();
    const distance = deadlineTime - now;

    if (distance < 0) {
      clearInterval(timerInterval);
      if (secondsEl) secondsEl.innerText = "00";
      if (minutesEl) minutesEl.innerText = "00";
      if (hoursEl) hoursEl.innerText = "00";
      if (daysEl) daysEl.innerText = "00";
      timerContainer.classList.add("expired");
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    if (secondsEl) secondsEl.innerText = String(seconds).padStart(2, "0");
    if (minutesEl) minutesEl.innerText = String(minutes).padStart(2, "0");
    if (hoursEl) hoursEl.innerText = String(hours).padStart(2, "0");
    if (daysEl) daysEl.innerText = String(days).padStart(2, "0");
  }, 1000);
});
