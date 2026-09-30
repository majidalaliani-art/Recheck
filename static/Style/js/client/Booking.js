import { ajax_json } from "../AJAX.js";
import { showError } from "../utils.js";



function handleUrlParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const propertyType = urlParams.get("property");
  if (propertyType) {
    const targetInput = document.getElementById(propertyType);

    if (targetInput) {
      targetInput.checked = true;

      if (typeof calculate === "function") {
        calculate();
      }
    }
  }
}

document.addEventListener("DOMContentLoaded", handleUrlParams);

async function calculate() {
  let size = Number(document.getElementById("property_size").value);
  if (!size) return;
  let villa = document.getElementById("villa").checked;
  let apartment = document.getElementById("apartment").checked;
  let type = villa ? "villa" : apartment ? "apartment" : null;
  if (!type) return;
  let data = { type: type, size: size };
  let result = await ajax_json("/visit_price/", data, "network issue");
  if (result) {
    document.getElementById("normal_price").innerText = result.normal_price;
    document.getElementById("full_price").innerText = result.full_price;
  }
}





function updateUI() {
  const cards = document.querySelectorAll(".service-card");
  cards.forEach((card) => {
    const input = card.querySelector('input[type="radio"]');

    if (input && input.checked) {
      card.classList.add("selected-card");
    } else {
      card.classList.remove("selected-card");
    }
  });
}

window.addEventListener("DOMContentLoaded", function () {
  updateUI();
});

function goToStep(stepNumber) {
  const sizeInput = document.getElementById("property_size");
  const size = parseFloat(sizeInput.value);

  if (stepNumber === 2) {
    if (!size || size <= 10) {
      sizeInput.style.borderColor = "#dc3545";
      sizeInput.focus();
      return;
    }
    let villa = document.getElementById("villa").checked;
    let apartment = document.getElementById("apartment").checked;
    let errorBox = document.getElementById("property_type_error");
    if (!villa && !apartment) {
      showError("property_type_error", "يرجى اختيار نوع العقار");
      errorBox.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
      return;
    }

    let inspection_1 = document.getElementById("inspection_1").checked;
    let inspection_2 = document.getElementById("inspection_2").checked;
    if (!inspection_1 && !inspection_2) {
      showError("inspection_type_error", "يرجى اختيار نوع الخدمة");
      return;
    }

    document.getElementById("step-1").classList.add("d-none");
    document.getElementById("step-2").classList.remove("d-none");

    calculate();
  } else {
    document.getElementById("step-2").classList.add("d-none");
    document.getElementById("step-1").classList.remove("d-none");
  }
}

document.querySelectorAll("[data-step]").forEach((el) => {
  el.addEventListener("click", () => {
    goToStep(Number(el.dataset.step));
  });
});

document.querySelectorAll(".service-card").forEach((el) => {
  el.addEventListener("click", updateUI);
});

let timeout;
document.getElementById("property_size").addEventListener("input", () => {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    calculate();
  }, 500);
});

document.querySelectorAll(".property-item").forEach((el) => {
  el.addEventListener("click", calculate);
});


// navigator.geolocation.getCurrentPosition(async (pos) => {
//   let lat = pos.coords.latitude;
//   let lng = pos.coords.longitude;

//   getCityFromCoords(lat, lng);
// });


// async function getCityFromCoords(lat, lng) {
//   let res = await fetch(
//     `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lng}&localityLanguage=en`,
//   );

//   let data = await res.json();

//   let city = data.city || data.locality;
//   document.getElementById("id_city").value = city;
// }

flatpickr("#visit-day", {
  minDate: "today",
  dateFormat: "Y-m-d",
  onChange: function () {
    document.getElementById("time-slots-select").disabled = false;
  },
});


document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const btn = form.querySelector("button[type=submit]");

  const dayInput = document.getElementById("visit-day");
  const timeSelect = document.getElementById("time-slots-select");

  const dayError = document.getElementById("day-error");
  const timeError = document.getElementById("time-error");

  let locked = false;

  form.addEventListener("submit", function (e) {
    let valid = true;

    dayError.innerHTML = "";
    timeError.innerHTML = "";

    if (!dayInput.value) {
      showError("day-error", "هذا الحقل مطلوب");
      valid = false;
    }

    if (!timeSelect.value) {
      showError("time-error", "هذا الحقل مطلوب");
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
