document.addEventListener("DOMContentLoaded", function () {
  const triggerBtn = document.getElementById("btn-trigger-modal");
  const modalElement = document.getElementById("addAreaModal");
  const cancelBtns = document.querySelectorAll(".force-close-modal");

  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement);


    if (triggerBtn) {
      triggerBtn.addEventListener("click", () => modal.show());
    }


    if (cancelBtns.length > 0) {
      cancelBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
          modal.hide();
        });
      });
    }
  }
});






document.addEventListener("DOMContentLoaded", function () {
  Fancybox.bind(document.body, {
    selector: "[data-fancybox^='group-']",
    groupAll: false,
    Hash: false,
    Toolbar: {
      display: {
        left: ["infobar"],
        right: ["zoom", "thumbs", "close"],
      },
    },
  });
});

// ==========================================
// 1. عرض الواجهات الرئيسية (Trigger / List / Details)
// ==========================================
function setMainViewDisplay(elements, targetView) {
  const { triggerBlock, listBlock, detailsBlock } = elements;

  // إخفاء جميع الواجهات
  if (triggerBlock) triggerBlock.classList.add("d-none");
  if (listBlock) listBlock.classList.add("d-none");
  if (detailsBlock) {
    detailsBlock.classList.add("d-none");
    detailsBlock.classList.remove("d-flex");
  }

  // إظهار الواجهة المستهدفة
  if (targetView === "trigger" && triggerBlock) {
    triggerBlock.classList.remove("d-none");
  } else if (targetView === "list" && listBlock) {
    listBlock.classList.remove("d-none");
  } else if (targetView === "details" && detailsBlock) {
    detailsBlock.classList.remove("d-none");
    detailsBlock.classList.add("d-flex");
  }
}

// ==========================================
// 2. عرض التبويبات الداخلية (Form / Evaluations)
// ==========================================
function setSubViewDisplay(elements, activeTab) {
  const { formBlock, evaluationsBlock, subViewButtons } = elements;
  const isForm = activeTab === "form";

  if (formBlock) {
    formBlock.classList.toggle("d-none", !isForm);
    formBlock.classList.toggle("d-flex", isForm);
  }

  if (evaluationsBlock) {
    evaluationsBlock.classList.toggle("d-none", isForm);
    evaluationsBlock.classList.toggle("d-flex", !isForm);
  }

  // تحديث حالة زر التبويب النشط (Active Class)
  subViewButtons.forEach((btn, index) => {
    btn.classList.toggle("active", (isForm && index === 0) || (!isForm && index === 1));
  });
}

// ==========================================
// 3. فلترة عرض كروت الرفع (Cards Filter Display)
// ==========================================
function filterUploadCardsDisplay(formBlock, itemKey) {
  if (!formBlock || !itemKey) return;


  const categoryWrappers = formBlock.querySelectorAll(".dynamic-upload-card");


  categoryWrappers.forEach((wrapper) => {
    const isMatch = wrapper.getAttribute("data-key") === itemKey;
    wrapper.classList.toggle("d-none", !isMatch);
  });
}

// ==========================================
// 4. الدالة الرئيسية لمنسق العرض (Main View Controller)
// ==========================================
function switchViews(areaId, targetView, itemId = null, itemKey = null, itemDisplay = null) {
  const detailsBlock = document.getElementById(`details-${areaId}`);

  const elements = {
    triggerBlock: document.getElementById(`trigger-${areaId}`),
    listBlock: document.getElementById(`list-${areaId}`),
    detailsBlock: detailsBlock,
    formBlock: document.getElementById(`form-${areaId}`),
    evaluationsBlock: document.getElementById(`evaluations-${areaId}`),
    subViewButtons: detailsBlock ? detailsBlock.querySelectorAll(".list-actions-wrapper button") : [],
  };

  // 1. التنقل بين الواجهات الرئيسية
  if (["trigger", "list", "details"].includes(targetView)) {
    setMainViewDisplay(elements, targetView);


    // عند فتح التفاصيل: يتم ضبط العرض على تبويب النموذج افتراضياً وتحديث عناصر العرض
    if (targetView === "details") {
      setSubViewDisplay(elements, "form");

      if (detailsBlock) {

        if (itemDisplay) {
          const titleElement = detailsBlock.querySelector(".details-title");
          if (titleElement) titleElement.textContent = itemDisplay;
        }
        if (itemId && itemKey) {
          const uploadBox = detailsBlock.querySelector(".uploadBox");
          if (uploadBox) {
            uploadBox.dataset.id = itemId;
            uploadBox.dataset.key = itemKey;
          }
        }
      }
    }
  }
  // 2. التنقل الداخلي بين (Form / Evaluations) فقط
  else if (["form", "evaluations"].includes(targetView)) {
    setSubViewDisplay(elements, targetView);
  }

  // 3. فلترة عرض كروت الرفع بناءً على المفتاح
  if (itemKey && elements.formBlock) {
    filterUploadCardsDisplay(elements.formBlock, itemKey);
  }
}


function handleFileChange(fileInput) {
  const file = fileInput.files[0];
  if (!file) return;

  // 1. مسك العناصر الأب المباشرة والتأكد من وجودها
  const parentCard = fileInput.closest(".sub-view-section");
  const uploadBox = fileInput.closest(".uploadBox");

  if (!parentCard || !uploadBox) return;

  // 2. جلب الحاوية و ID البند والقالب
  const imagesContainer = parentCard.querySelector(".upload-cards-wrapper");
  const dataIdValue = uploadBox.dataset.id;
  const dataKeyValue = uploadBox.dataset.key;

  const template = document.getElementById("upload-file-card-template");

  if (!imagesContainer || !dataKeyValue || !dataIdValue || !template) return;

  // 3. استنساخ القالب وإنشاء رابط المعاينة
  const clone = template.content.cloneNode(true);
  const fileUrl = URL.createObjectURL(file);
  const cardElement = clone.querySelector(".dynamic-upload-card");

  // 4. تعبئة عناصر البطاقة
  const thumbImg = clone.querySelector("[data-file-thumb]");
  const thumbBox = clone.querySelector("a.thumb-box");
  const hiddenInput = clone.querySelector(".hidden-image-input");
  const saveBtn = clone.querySelector(".btn-save-file");
  const deleteBtn = clone.querySelector(".card-delete-btn");
  const deleteBtn2 = clone.querySelector(".btn-delete-card");



  if (!cardElement || !thumbImg || !thumbBox || !hiddenInput || !saveBtn || !deleteBtn) return;


  if (thumbImg) thumbImg.src = fileUrl;
  if (thumbBox) thumbBox.href = fileUrl;
  if (hiddenInput) hiddenInput.uploadedFile = file;
  if (saveBtn) saveBtn.dataset.id = dataIdValue;
  if (cardElement) cardElement.dataset.key = dataKeyValue;


  // 5. زر الحذف بلمسة حركة ناعمة وتنظيف الذاكرة
  if (deleteBtn && cardElement) {
      const handleDelete = (e) => {
        cardElement.style.transition = "all 0.3s ease";
        cardElement.style.opacity = "0";
        cardElement.style.transform = "scale(0.85)";

        setTimeout(() => {
          cardElement.remove();
          if (typeof fileUrl !== "undefined" && fileUrl) {
            URL.revokeObjectURL(fileUrl);
          }
        }, 300);
      };

      if (deleteBtn) deleteBtn.addEventListener("click", handleDelete);
      if (deleteBtn2) deleteBtn2.addEventListener("click", handleDelete);

  }

  // 6. حقن البطاقة وتفريغ مدخل الرفع
  imagesContainer.prepend(clone);
  fileInput.value = "";
}


document.addEventListener("DOMContentLoaded", function () {
  // دالة تحديث لون مسار السلايدر
 function updateSliderColor(slider) {
   const min = parseFloat(slider.min) || 0;
   const max = parseFloat(slider.max) || 100;
   const val = parseFloat(slider.value) || 0;
   const percentage = ((val - min) / (max - min)) * 100;

   // to left لأن البداية (0%) من اليمين في نظام RTL
   slider.style.background = `linear-gradient(to left, #136053 ${percentage}%, #e2e8f0 ${percentage}%)`;
 }

  // 1. تلوين كل السلايدرات عند فتح الصفحة أول مرة
  document.querySelectorAll(".eval-range").forEach(updateSliderColor);

  // 2. دالة التعامل مع تغيير حالة السويتش (تفعيل / تعطيل)
  document.addEventListener("change", function (e) {
    if (e.target && e.target.classList.contains("item-switch")) {
      const switchInput = e.target;
      const itemId = switchInput.id.replace("switch-", "");

      const wrapper = document.getElementById(`score-wrapper-${itemId}`);
      const rangeInput = document.getElementById(`range-${itemId}`);

      if (wrapper && rangeInput) {
        if (switchInput.checked) {
          wrapper.classList.remove("disabled-bar");
          wrapper.classList.add("active-bar");
          rangeInput.disabled = false;
        } else {
          wrapper.classList.remove("active-bar");
          wrapper.classList.add("disabled-bar");
          rangeInput.disabled = true;
        }
      }
    }
  });

  // 3. تحديث النسبة المئوية + تلوين السلايدر فوراً أثناء السحب
  document.addEventListener("input", function (e) {
    if (e.target && e.target.classList.contains("eval-range")) {
      const rangeInput = e.target;
      const itemId = rangeInput.id.replace("range-", "");
      const scoreValSpan = document.getElementById(`score-val-${itemId}`);

      // تحديث الرقم النصي
      if (scoreValSpan) {
        scoreValSpan.innerText = `%${rangeInput.value}`;
      }

      // تحديث اللون
      updateSliderColor(rangeInput);
    }
  });
});
