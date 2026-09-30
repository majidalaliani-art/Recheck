import { ajax_get } from "../AJAX.js";
import { showError } from "../utils.js";
let weeklyRules = {};
function generateHours(start, end, selectedDate) {
  let slots = [];

  slots.push("...");

  let [sh] = start.split(":").map(Number);
  let [eh] = end.split(":").map(Number);

  const now = new Date();

  const isToday =
    selectedDate &&
    selectedDate.toDateString() === now.toDateString();

  function formatHour(h) {
    let period = "صباحًا";

    if (h === 12) period = "ظهرًا";
    else if (h > 12) period = "مساءً";

    let hour12 = h % 12;
    if (hour12 === 0) hour12 = 12;

    return `${hour12} ${period}`;
  }

  for (let h = sh; h < eh; h++) {
    let next = h + 1;

    if (isToday && h <= now.getHours()) {
      continue;
    }

    slots.push(`من ${formatHour(h)} إلى ${formatHour(next)}`);
  }

  return slots;
}


flatpickr("#calendar", {
  minDate: "today",

  onOpen: async function (selectedDates, dateStr, instance) {
    const data = await ajax_get("/consultation_day/", "Error loading consultation days:");

    if (!data || !Array.isArray(data)) return;

    weeklyRules = {};

    data.forEach((day) => {
      weeklyRules[day.num] = day;
    });

    instance.redraw();
  },

  disable: [
    function (date) {
      if (!weeklyRules) return false;

      const dayNum = date.getDay() + 1;

      return !(dayNum in weeklyRules);
    },
  ],

  onChange: function (selectedDates) {
    if (!selectedDates.length) return;

    const dayNum = selectedDates[0].getDay() + 1;
    const rule = weeklyRules[dayNum];

    if (!rule) return;

    document.getElementById("details_card").style.display = "block";
    document.getElementById("price_val").innerText = rule.price;
    document.getElementById("name_val").innerText = rule.name;

    const select = document.getElementById("time_select");
    select.disabled = false;
    select.innerHTML = "";

    const times = generateHours(rule.start_time, rule.end_time, selectedDates[0]);

    times.forEach((t) => {
      const option = document.createElement("option");
      option.value = t;
      option.textContent = t;
      select.appendChild(option);
    });
  },
});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const btn = form.querySelector("button[type=submit]");

  const calendarInput = document.getElementById("calendar");
  const timeSelect = document.getElementById("time_select");
  timeSelect.innerHTML = '<option value="">...</option>';

  const calendarError = document.getElementById("calendar_error");
  const timeError = document.getElementById("time_error");

  let locked = false;

  form.addEventListener("submit", function (e) {
    let valid = true;

    calendarError.innerHTML = "";
    timeError.innerHTML = "";

    if (!calendarInput.value) {
      showError("calendar_error", "هذا الحقل مطلوب");
      valid = false;
    }
    if (!timeSelect.value) {
      showError("time_error", "هذا الحقل مطلوب");
      valid = false;
    }
    if (timeSelect.value === "...") {
      showError("time_error", "يرجى اختيار وقت ساعه");
      valid = false;
    }

    if (!valid) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }

    if (locked) {
      e.preventDefault();
      return;
    }

    locked = true;
    btn.disabled = true;
  });
});
