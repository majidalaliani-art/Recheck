fetch("../json/GoogleForms.json")
  .then((res) => res.json())
  .then((data) => {
    const texts = data[0];

    document.querySelectorAll("input").forEach((input) => {
      const key = input.getAttribute("value");
      if (texts[key]) {
        input.value = texts[key];
      }
    });
  });

function loadLang(lang) {
  fetch(`../json/languages/${lang}.json`)
    .then((res) => res.json())
    .then((data) => {
      const texts = data[0];

      document.querySelectorAll("[data-key]").forEach((el) => {
        const key = el.dataset.key;
        el.textContent = texts[key];
      });

      document.documentElement.lang = lang;
      document.body.dir = lang === "ar" ? "rtl" : "ltr";
    });
}

function changeLang(lang) {
  localStorage.setItem("lang", lang);
  loadLang(lang);
}

const savedLang = localStorage.getItem("lang") || "ar";
loadLang(savedLang);

/// =================== goToStep =================== ///

function goToStep(stepNumber, scroll = true) {
  const target = parseInt(stepNumber);

  for (let i = 1; i <= 6; i++) {
    const stepDiv = document.getElementById("step" + i);
    if (stepDiv) {
      stepDiv.style.display = "none";
    }

    const tabBtn = document.getElementById("tab" + i);
    if (tabBtn) {
      tabBtn.classList.remove("active", "completed");

      if (i < target) {
        tabBtn.classList.add("completed");
      } else if (i === target) {
        tabBtn.classList.add("active");
      }
    }
  }
  const currentDiv = document.getElementById("step" + target);
  if (currentDiv) {
    currentDiv.style.display = "flex";
  }
  localStorage.setItem("lastStep", target);

  if (scroll) {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

/// =================== checkRadioGroups =================== ///
function checkRadioGroups() {
  const missing = [];

  const radioGroups = ["1953222995", "339810482", "1599264128", "1294559095"];

  // div لعرض الخطوات الناقصة
  const missingDiv = document.getElementById("missingSteps");
  missingDiv.innerHTML = "";

  radioGroups.forEach((name) => {
    const radios = document.querySelectorAll(`input[name="entry.${name}"]`);
    if (!Array.from(radios).some((r) => r.checked)) {
      missing.push(name);
      const labelElement = document.querySelector(`label[data-key="field_location"]`);
      let labelText;
      if (name == "1953222995") {
        labelText = labelElement ? labelElement.textContent : "اختر الموقع الميداني";
      }
      const link = document.createElement("a");
      link.href = "#";
      link.textContent = labelText;
      link.classList.add("missing-step");

      link.addEventListener("click", (e) => {
        e.preventDefault();
        const targetDiv = document.getElementById(name);
        if (targetDiv) {
          targetDiv.scrollIntoView({ behavior: "smooth", block: "start" });

          targetDiv.classList.add("highlight-missing");
          setTimeout(() => {
            targetDiv.classList.remove("highlight-missing");
          }, 2000);
          setTimeout(() => {
            targetDiv.style.border = "";
          }, 2000);
        }
      });
      missingDiv.appendChild(link);
    }
  });

  const submitBtn = document.getElementById("submitBtn");
  submitBtn.style.display = missing.length === 0 ? "inline-block" : "none";
}

document.querySelectorAll('input[id^="search_"]').forEach((input) => {
  input.addEventListener("input", () => {
    const value = input.value.toLowerCase();
    const groupId = input.id.replace("search_", "");
    const groupDiv = document.getElementById(groupId);
    if (!groupDiv) return;
    const items = groupDiv.querySelectorAll(".radio-item");
    items.forEach((item) => {
      const label = item.querySelector("label");
      const text = label.textContent.toLowerCase();
      item.style.display = text.includes(value) ? "block" : "none";
    });
  });
});

// =================== startForm =================== //

function saveFields() {
  document.querySelectorAll("input, textarea").forEach((field) => {
    const eventType = field.type === "radio" || field.type === "checkbox" ? "change" : "input";
    field.addEventListener(eventType, () => {
      if (field.type === "radio") {
        if (field.checked) {
          localStorage.setItem(field.name, field.value);
        }
      } else if (field.type === "checkbox") {
        const checkedVals = Array.from(
          document.querySelectorAll(`input[name="${field.name}"]:checked`),
        )
          .map((i) => i.value)
          .join(",");
        localStorage.setItem(field.name, checkedVals);
      } else {
        if (field.id) {
          localStorage.setItem(field.id, field.value);
        }
      }
    });
  });
}

function loadFields() {
  document.querySelectorAll("input, textarea").forEach((field) => {
    if (field.type === "radio") {
      const saved = localStorage.getItem(field.name);
      if (saved !== null) {
        field.checked = field.value === saved;
      }
    } else if (field.type === "checkbox") {
      const saved = localStorage.getItem(field.name);
      if (saved) {
        field.checked = saved.split(",").includes(field.value);
      }
    } else {
      if (field.id) {
        const saved = localStorage.getItem(field.id);
        if (saved !== null) {
          field.value = saved;
        }
      }
    }
  });
}

window.addEventListener("load", () => {
  const savedStep = localStorage.getItem("lastStep") || 1;
  goToStep(savedStep, false);

  const observer = new MutationObserver((mutations, obs) => {
    const inputs = document.querySelectorAll('input[type="radio"]');
    if (inputs.length > 0) {
      loadFields();
      saveFields();
      obs.disconnect();
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });
});


window.addEventListener("load", () => {
  loadFields();
});


document.addEventListener("click", function (e) {
  const el = e.target;

  if (el.type === "radio") {
    const parts = el.id.split("_");
    const itemNumber = parts[parts.length - 1];
    const Id = parts[parts.length - 2];



    if (itemNumber === "1") {
      console.log("تم ضغط الزر الأول");
      goToStep(3);
    } else if (itemNumber === "2") {
      goToStep(4);
    } else if (itemNumber === "3") {

      goToStep(5);
    }
  }
});



function generateRadioButtons(containerId, totalItems, entryName, prefix) {
    const container = document.getElementById(containerId);
    if (!container) return;
    let htmlContent = '';


    for (let i = 1; i <= totalItems; i++) {
      const valueAttribute = `${prefix}${i}`;
      const elementId = `opt_${containerId}_${i}`;

      const isNext = prefix === "a" ? "nextBtn" : "";

      htmlContent += `
      <div class="radio-item">
        <input type="radio" name="${entryName}" value="${valueAttribute}" id="${elementId}" ${isNext} />
        <label for="${elementId}" data-key="${valueAttribute}"></label>
      </div>`;
    }


    container.innerHTML = htmlContent;
}












generateRadioButtons("1593134746", 3, "entry.1593134746", "a");
generateRadioButtons("11479402", 75, "entry.11479402", "q");
