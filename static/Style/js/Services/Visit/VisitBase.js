import { ajax_request, ajax_json, ajax_get } from "../../AJAX.js";
const visitId = document.getElementById("visit-id").value;


document.addEventListener("DOMContentLoaded", () => {

  const tabs = document.querySelectorAll(".report-tabs-bar .tab-item");
  const panels = document.querySelectorAll(".tab-panel");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const currentStep = parseInt(tab.getAttribute("data-step"));
      tabs.forEach((t) => {
        const tStep = parseInt(t.getAttribute("data-step"));

        if (tStep < currentStep) {
          t.classList.add("completed");
          t.classList.remove("active");
        } else if (tStep === currentStep) {
          t.classList.add("active");
          t.classList.remove("completed");
        } else {
          t.classList.remove("active");
          t.classList.remove("completed");
        }
      });
      panels.forEach((panel) => panel.classList.remove("active"));
      const targetPanel = document.getElementById(`panel-${currentStep}`);
      if (targetPanel) {
        targetPanel.classList.add("active");
      }
    });
  });
});

function switchToStep(stepNumber) {
  // 1. إخفاء كل البانلات وإزالة الكلاس active منها
  document.querySelectorAll(".tab-panel").forEach((panel) => {
    panel.classList.remove("active");
  });

  // 2. إظهار البانل المستهدف بناءً على رقمه
  const targetPanel = document.getElementById(`panel-${stepNumber}`);
  if (targetPanel) {
    targetPanel.classList.add("active");
  }

  // 3. تحديث الشريط العلوي (الخطوات / الـ Tabs Bar) بنفس منطقك تماماً
  const tabs = document.querySelectorAll(".report-tabs-bar .tab-item");
  tabs.forEach((t) => {
    const tStep = parseInt(t.getAttribute("data-step"));

    if (tStep < stepNumber) {
      t.classList.add("completed");
      t.classList.remove("active");
    } else if (tStep === stepNumber) {
      t.classList.add("active");
      t.classList.remove("completed");
    } else {
      t.classList.remove("active");
      t.classList.remove("completed");
    }
  });

  // 4. تحريك الصفحة لأعلى قليلاً ليرى المستخدم بداية النموذج الجديد
  window.scrollTo({ top: 0, behavior: "smooth" });
}

document.addEventListener("DOMContentLoaded", function () {
  if (!visitId || !SAVE_VISIT_URL || !SAVE_INSPECTION_URL) return;
  const saveBtns = document.querySelectorAll("button.save-btn[data-panel]");
  const backBtns = document.querySelectorAll("button.back-btn[data-prev]");

  if (saveBtns) {
    saveBtns.forEach((saveBtn) => {
      const currentPanel = saveBtn.dataset.panel;
      const nextPanel = saveBtn.dataset.next;
      const form = document.getElementById(`panel-${currentPanel}`);
      if (!currentPanel || !nextPanel || !form) return;

      saveBtn.addEventListener("click", async function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        formData.append("model_name", "VisitReport");
        formData.append("id", visitId);
        formData.append("panel", currentPanel);

        // تغيير شكل الزر أثناء التحميل
        //const originalText = saveBtn.innerHTML;
        saveBtn.disabled = true;

        const data = await ajax_request(
          SAVE_VISIT_URL,
          formData,
          `خطأ أثناء حفظ بيانات البانل ${currentPanel}:`,
        );

        saveBtn.disabled = false;
        //saveBtn.innerHTML = originalText;

        if (data) {
          if (nextPanel) {
            switchToStep(parseInt(nextPanel));
          }
        }
      });
    });
  }
  if (backBtns) {
    backBtns.forEach((backBtn) => {
      const prevPanel = backBtn.dataset.prev;

      if (!prevPanel) return;

      backBtn.addEventListener("click", function (e) {
        e.preventDefault();
        switchToStep(parseInt(prevPanel));
      });
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const previewContainer = document.getElementById("areas-preview-container");
  const cardTemplate = document.getElementById("area-card-template");
  const addAreaModal = document.getElementById("addAreaModal");
  if (!previewContainer || !visitId || !cardTemplate || !addAreaModal) return;
  const publicAreaButton = document.getElementById("add-public-area-btn");
  const triggerModalBtn = document.getElementById("btn-trigger-modal");

  if (publicAreaButton) {
    publicAreaButton.addEventListener("click", handler);
  } else if (triggerModalBtn) {
    addAreaModal.addEventListener("click", handler);
  } 

  async function handler(e) {
    const createAreaBtn = e.target.closest(".add-area-btn");
    if (!createAreaBtn) return;
    const key = createAreaBtn.dataset.key;
    if (!key) return;
    const payload = { id: visitId, name: "InspectionArea", action: "add", items: key };
    const result = await ajax_json(SAVE_INSPECTION_URL, payload, "خطأ أثناء إنشاء المنطقة:");

    if (result?.status !== "success") return;

    const html = cardTemplate.innerHTML
      .replaceAll("TEMP_ID", result.id)
      .replaceAll("TEMP_DISPLAY", result.address)
      .replaceAll("TEMP_NAME", result.address);

    previewContainer.insertAdjacentHTML("beforeend", html);
  }

  previewContainer.addEventListener("click", async function (e) {
    // -------------------------------------------------
    // 1. منطق التكبير والتصغير (Collapse & Expand)
    // -------------------------------------------------
    const collapseBtn = e.target.closest(".btn-collapse-toggle");
    if (collapseBtn) {
      collapseBtn.closest(".area-card")?.classList.toggle("collapsed-card");
      return;
    }

    // -------------------------------------------------
    // 2. اضافه منطقه جديده
    // -------------------------------------------------

    // -------------------------------------------------
    // 3. منطق حذف المنطقة (بنفس طريقتك المعتمدة)
    // -------------------------------------------------
    const deleteAreaBtn = e.target.closest(".dynamic-delete-btn");
    if (deleteAreaBtn) {
      const areaId = deleteAreaBtn.getAttribute("data-id");
      const areaName = deleteAreaBtn.getAttribute("data-name");

      if (!areaId || !areaName) return;

      const isConfirmed = await showConfirmModal("هل انت متاكد من حذف ", areaName);
      if (!isConfirmed) return;

      const payload = {
        id: areaId,
        name: "InspectionArea",
        action: "Delete the motherboard",
      };

      const result = await ajax_json(SAVE_INSPECTION_URL, payload, "خطأ أثناء حذف المنطقة:");

      if (result?.status === "success") {
        const targetElement = document.querySelector(deleteAreaBtn.getAttribute("data-target"));
        if (targetElement) {
          targetElement.style.transition = "all 0.2s ease";
          targetElement.style.opacity = "0";
          targetElement.style.transform = "scale(0.95)";
          setTimeout(() => targetElement.remove(), 200);
        }
      }
      return;
    }

    // -------------------------------------------------
    // 4. تحديث العنوان المنطقه
    // -------------------------------------------------
    const saveTitleBtn = e.target.closest(".btn-save-title");
    if (saveTitleBtn) {
      const wrapper = saveTitleBtn.closest(".custom-title-wrapper");
      const input = wrapper?.querySelector(".area-custom-input");
      if (!input) return;
      const areaId = saveTitleBtn.getAttribute("data-id");
      const newValue = input.value.trim();
      const header = saveTitleBtn.closest(".area-card-header");
      const deleteAreaBtn = header.querySelector(".dynamic-delete-btn");
      if (!wrapper || !areaId || !newValue) return;

      saveTitleBtn.disabled = true;
      saveTitleBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

      const payload = {
        id: areaId,
        name: "InspectionArea",
        action: "update_title",
        items: newValue,
      };

      const result = await ajax_json(
        SAVE_INSPECTION_URL,
        payload,
        "خطأ أثناء حفظ اسم المنطقة:",
      );

      await new Promise((resolve) => setTimeout(resolve, 1000));

      if (result?.status === "success") {
        input.setAttribute("data-original-value", newValue);
        deleteAreaBtn.setAttribute("data-name", newValue);

        saveTitleBtn.classList.add("save-success");
        saveTitleBtn.innerHTML = '<i class="fa-solid fa-check"></i>';

        setTimeout(() => {
          saveTitleBtn.classList.remove("show", "save-success");
          saveTitleBtn.disabled = false;
          saveTitleBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i>';
        }, 1500);
      } else {
        saveTitleBtn.classList.add("save-error");
        saveTitleBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';

        setTimeout(() => {
          saveTitleBtn.classList.remove("save-error");
          saveTitleBtn.disabled = false;
          saveTitleBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i>';
        }, 1500);
      }
    }
  });

  // -------------------------------------------------
  // 4. مراقبة كتابة المهندس للتحكم بظهور زر الحفظ (UI)
  // -------------------------------------------------
  previewContainer.addEventListener("input", (e) => {
    if (e.target.classList.contains("area-custom-input")) {
      const input = e.target;
      const saveBtn = input.closest(".custom-title-wrapper")?.querySelector(".btn-save-title");
      if (!saveBtn) return;

      const isChanged = input.value.trim() !== (input.getAttribute("data-original-value") || "");
      saveBtn.classList.toggle("show", isChanged && input.value.trim() !== "");
    }
  });

  // -------------------------------------------------
  // مراقبة رفع الصور العامة فوراً عند اختيارها وحقنها في نفس اللحظة
  // -------------------------------------------------

  previewContainer.addEventListener("change", async function (e) {
    const input = e.target.closest(".general-images-input");

    if (input) {
      const areaId = input.getAttribute("data-area-id");
      const files = input.files;

      if (!files || files.length === 0) return;

      const formData = new FormData();

      formData.append("id", areaId);
      formData.append("model_name", "AreaImage");
      formData.append("action", "save");
      formData.append("images", files[0]);

      const result = await ajax_request(SAVE_VISIT_URL, formData, "خطأ أثناء رفع الصور:");

      if (result?.status === "success" && result.url) {
        const template = document.getElementById("image-preview-template");

        if (template) {
          let imgHtml = template.innerHTML
            .replace(/TEMP_ID/g, result.id)
            .replace(/TEMP_URL/g, result.url);

          const rowContainer = input.closest(".images-horizontal-row");

          if (rowContainer) {
            rowContainer.insertAdjacentHTML("beforeend", imgHtml);

            const newImage = rowContainer.lastElementChild;

            if (newImage) {
              newImage.style.opacity = "0";
              newImage.style.transform = "translateY(20px) scale(0.9)";
              newImage.style.transition = "all 0.35s ease";

              requestAnimationFrame(() => {
                newImage.style.opacity = "1";
                newImage.style.transform = "translateY(0) scale(1)";
              });
            }
          }
        }

        input.value = "";
      }
    }
  });

  previewContainer.addEventListener("click", async function (e) {
    const deleteBtn = e.target.closest(".delete-img-btn");

    if (deleteBtn) {
      const imgId = deleteBtn.getAttribute("data-id");
      if (!imgId) return;

      const wrapper = document.getElementById(`img-wrapper-${imgId}`);
      if (!wrapper) return;

      const formData = new FormData();
      formData.append("id", imgId);
      formData.append("model_name", "AreaImage");
      formData.append("action", "delete");

      const result = await ajax_request(SAVE_VISIT_URL, formData, "خطأ أثناء حذف الصورة:");

      if (result?.status === "success" || result?.success) {
        wrapper.style.height = wrapper.offsetHeight + "px";
        wrapper.style.overflow = "hidden";
        wrapper.style.transition = "all 0.35s ease";

        requestAnimationFrame(() => {
          wrapper.style.opacity = "0";
          wrapper.style.transform = "scale(0.85)";
          wrapper.style.height = "0";
          wrapper.style.margin = "0";
          wrapper.style.padding = "0";
        });

        setTimeout(() => {
          wrapper.remove();
        }, 350);
      }
    }
  });

  previewContainer.addEventListener("click", async (event) => {
    const saveBtn = event.target.closest(".submit-inspection-btn");

    if (saveBtn) {
      const areaId = saveBtn.getAttribute("data-area-id");
      if (!areaId) return;
      const checkedBoxes = document.querySelectorAll(`#list-${areaId} .item-checkbox:checked`);
      const selectedSlugs = Array.from(checkedBoxes).map((cb) => cb.value);
      if (selectedSlugs.length === 0) return;
      const evalTemplate = document.getElementById("evaluation-card-template");
      const evaluationsContainer = document.getElementById(`evaluations-${areaId}`);

      if (!evalTemplate || !evaluationsContainer) return;


      const payload = {
        id: areaId,
        items: selectedSlugs,
        name: "InspectionArea",
        action: "create",
      };

      saveBtn.disabled = true;
      const result = await ajax_json(
        SAVE_INSPECTION_URL,
        payload,
        "خطأ أثناء حفظ بنود الفحص:",
      );
      saveBtn.disabled = false;

      if (result && result.created_items) {
        const template = document.getElementById("badge-template");
        const triggerContainer = document.getElementById(`trigger-${areaId}`);

        if (template && triggerContainer) {
          const addButtonCol = triggerContainer
            .querySelector(".btn-add-item")
            ?.closest(".add-item-wrapper");

          for (const item of result.created_items) {
            let html = template.innerHTML
              .replaceAll("TEMP_KEY", item.key)
              .replaceAll("TEMP_TITLE", item.name)
              .replaceAll("TEMP_ID", item.id)
              .replaceAll("AREAE_ID", areaId);

            if (addButtonCol) {
              addButtonCol.insertAdjacentHTML("beforebegin", html);
            }
          }
        }

        if (evalTemplate && evaluationsContainer) {
          const saveButtonCol = evaluationsContainer
            .querySelector(".btn-save-evaluations")
            ?.closest(".col-12");

          for (const item of result.created_items) {
            let html = evalTemplate.innerHTML
              .replaceAll("TEMP_KEY", item.key)
              .replaceAll("TEMP_TITLE", item.name)
              .replaceAll("TEMP_ID", item.id)
              .replaceAll("AREAE_ID", areaId)
              .replaceAll("TEMP_SCORE", item.score || 0);

            if (saveButtonCol) {
              saveButtonCol.insertAdjacentHTML("beforebegin", html);
            }
          }
        }

        checkedBoxes.forEach((cb) => (cb.checked = false));
        switchViews(areaId, "trigger");
      }
    }

    const deleteBtn = event.target.closest(".delete-icon");
    if (deleteBtn) {
      const itemId = deleteBtn.getAttribute("data-id");
      const itemName = deleteBtn.getAttribute("data-name");
      const card = deleteBtn.closest(".badge-card");

      if (!itemId || !card || !itemName) return;

      const evaluationElement = document.getElementById(`evaluation-${itemId}`);
      if (!evaluationElement) return;

      const isConfirmed = await showConfirmModal("هل أنت متأكد من حذف البند", itemName);
      if (!isConfirmed) return;

      const payload = { id: itemId, action: "delete", name: "InspectionArea" };

      const result = await ajax_json(SAVE_INSPECTION_URL, payload, "خطأ أثناء حذف البند:");

      if (result) {
        // 1. حذف عنصر التقييم مباشرة
        evaluationElement.remove();

        // 2. تطبيق تأثير الاختفاء الناعم للكرت (Smooth Fade & Collapse)
        card.style.maxHeight = card.offsetHeight + "px";
        card.style.overflow = "hidden";
        card.style.transition = "all 0.35s cubic-bezier(0.4, 0, 0.2, 1)";

        requestAnimationFrame(() => {
          card.style.opacity = "0";
          card.style.transform = "translateY(15px) scale(0.9)";
          card.style.maxHeight = "0";
          card.style.paddingTop = "0";
          card.style.paddingBottom = "0";
          card.style.marginTop = "0";
          card.style.marginBottom = "0";
        });

        setTimeout(() => card.remove(), 350);
      }
    }

    const saveEvaluationsBtn = event.target.closest(".btn-save-evaluations");
    if (saveEvaluationsBtn) {
      const wrapper = saveEvaluationsBtn.closest(".evaluations-wrapper");
      if (!wrapper) return;

      const itemsPayload = [];
      const cards = wrapper.querySelectorAll(".evaluation-card");

      cards.forEach((card) => {
        const itemId = card.id.replace("evaluation-", "");

        const switchEl = card.querySelector(".item-switch");
        const rangeEl = card.querySelector(".eval-range");

        if (!itemId || !switchEl || !rangeEl) return;

        const isAvailable = switchEl.checked;
        const score = isAvailable ? parseInt(rangeEl.value, 10) : 0;

        itemsPayload.push({ id: itemId, is_available: isAvailable, score: score });
      });

      if (itemsPayload.length === 0) return;

      const payload = { items: itemsPayload, action: "update", name: "InspectionArea" };

      const originalHTML = saveEvaluationsBtn.innerHTML;
      const originalBg = saveEvaluationsBtn.style.backgroundColor;
      const originalColor = saveEvaluationsBtn.style.color;

      saveEvaluationsBtn.disabled = true;
      saveEvaluationsBtn.style.opacity = "0.7";
      saveEvaluationsBtn.innerHTML = "جاري الحفظ...";

      try {
        const minDelay = new Promise((resolve) => setTimeout(resolve, 500));

        const [result] = await Promise.all([
          ajax_json(SAVE_INSPECTION_URL, payload, "خطأ أثناء حفظ التقييمات:"),
          minDelay,
        ]);

        if (result) {
          saveEvaluationsBtn.style.opacity = "1";
          saveEvaluationsBtn.style.backgroundColor = "#198754";
          saveEvaluationsBtn.style.color = "#ffffff";
          saveEvaluationsBtn.innerHTML = "تم الحفظ ✓";

          setTimeout(() => {
            saveEvaluationsBtn.innerHTML = originalHTML;
            saveEvaluationsBtn.style.backgroundColor = originalBg;
            saveEvaluationsBtn.style.color = originalColor;
            saveEvaluationsBtn.disabled = false;
          }, 1500);
        } else {
          saveEvaluationsBtn.style.opacity = "1";
          saveEvaluationsBtn.style.backgroundColor = "#dc3545";
          saveEvaluationsBtn.style.color = "#ffffff";
          saveEvaluationsBtn.innerHTML = "فشل الحفظ ✕";

          setTimeout(() => {
            saveEvaluationsBtn.innerHTML = originalHTML;
            saveEvaluationsBtn.style.backgroundColor = originalBg;
            saveEvaluationsBtn.style.color = originalColor;
            saveEvaluationsBtn.disabled = false;
          }, 1500);
        }
      } catch (error) {
        saveEvaluationsBtn.style.opacity = "1";
        saveEvaluationsBtn.style.backgroundColor = "#dc3545";
        saveEvaluationsBtn.style.color = "#ffffff";
        saveEvaluationsBtn.innerHTML = "فشل الحفظ ✕";

        setTimeout(() => {
          saveEvaluationsBtn.innerHTML = originalHTML;
          saveEvaluationsBtn.style.backgroundColor = originalBg;
          saveEvaluationsBtn.style.color = originalColor;
          saveEvaluationsBtn.disabled = false;
        }, 1500);
      }
    }
  });

  previewContainer.addEventListener("click", async function (e) {
    // ==========================================
    // 1. زر التعديل (Save)
    // ==========================================

    const saveBtn = e.target.closest(".btn-save-file");
    if (saveBtn) {
      if (saveBtn.disabled) return;

      const itemId = saveBtn.dataset.id;
      const card = saveBtn.closest(".dynamic-upload-card");
      if (!card || !itemId) return;

      const commentInput = card.querySelector(".comment-input");
      const hiddenInput = card.querySelector(".hidden-image-input");
      const uploadedFile = hiddenInput ? hiddenInput.uploadedFile : null;

      if (!commentInput || !uploadedFile) return;

      const commentText = commentInput.value.trim();

      // فحص النص
      if (!commentText) {
        commentInput.classList.add("comment-error");
        return;
      }
      commentInput.classList.remove("comment-error");

      const originalHTML = saveBtn.innerHTML;
      const originalBg = saveBtn.style.backgroundColor;
      const originalColor = saveBtn.style.color;

      saveBtn.disabled = true;
      saveBtn.style.opacity = "0.7";
      saveBtn.innerHTML = `جاري الحفظ...`;

      const formData = new FormData();
      formData.append("id", itemId);
      formData.append("model_name", "InspectionItemImage");
      formData.append("comment", commentText);
      formData.append("image", uploadedFile);
      formData.append("action", "save");

      try {
        const minDelay = new Promise((resolve) => setTimeout(resolve, 500));
        const [response] = await Promise.all([
          ajax_request(SAVE_VISIT_URL, formData, "حدث خطأ أثناء حفظ البطاقة:"),
          minDelay,
        ]);

        if (response && response.status === "success") {
          saveBtn.style.opacity = "1";
          saveBtn.style.backgroundColor = "#198754";
          saveBtn.style.color = "#ffffff";
          saveBtn.innerHTML = `تم الحفظ ✓`;

          const djangoImageId = response.id; // الـ ID القادم من جانجو
          card.dataset.key = response.key;
          card.id = `dynamic-upload-card-${djangoImageId}`;
          //data-key

          setTimeout(() => {
            // 1. حذف زر الحفظ نهائياً من DOM (تنزل قيمته وتروح تماماً)
            saveBtn.remove();
            const deleteBtn = card.querySelector(".btn-delete-file");
            if (deleteBtn) deleteBtn.remove();

            const localDeleteBtn = card.querySelector(".card-delete-btn");

            if (localDeleteBtn && djangoImageId) {
              const newDeleteBtn = localDeleteBtn.cloneNode(true);
              newDeleteBtn.classList.remove("card-delete-btn");
              newDeleteBtn.classList.add("btn-delete-file");
              newDeleteBtn.dataset.id = djangoImageId;
              localDeleteBtn.replaceWith(newDeleteBtn);
            }

            const updateBtn = card.querySelector(".btn-update-file");
            if (updateBtn && djangoImageId) {
              updateBtn.dataset.id = djangoImageId;
              updateBtn.classList.remove("d-none");
            }
          }, 1000);
        } else {
          const isImageError = response && response.error_type === "image";

          if (isImageError) {
            saveBtn.remove();
            const updateBtn = card.querySelector(".btn-update-file");
            updateBtn.remove();

            const deleteBtn = card.querySelector(".btn-delete-card");
            if (deleteBtn) {
              deleteBtn.classList.remove("d-none");
            }
          } else {
            // خطأ عام (نص / شبكة) -> إعادة الزر لحالته الأصلية ليعيد المحاولة
            saveBtn.style.opacity = "1";
            saveBtn.style.backgroundColor = "#dc3545";
            saveBtn.style.color = "#ffffff";
            saveBtn.innerHTML = `فشل الحفظ ✕`;

            setTimeout(() => {
              saveBtn.innerHTML = originalHTML;
              saveBtn.style.backgroundColor = originalBg;
              saveBtn.style.color = originalColor;
              saveBtn.disabled = false;
            }, 1500);
          }
        }
      } catch (error) {
        saveBtn.style.opacity = "1";
        saveBtn.style.backgroundColor = "#dc3545";
        saveBtn.style.color = "#ffffff";
        saveBtn.innerHTML = `فشل الحفظ ✕`;

        setTimeout(() => {
          saveBtn.innerHTML = originalHTML;
          saveBtn.style.backgroundColor = originalBg;
          saveBtn.style.color = originalColor;
          saveBtn.disabled = false;
        }, 1500);
      }
      return;
    }

    // ==========================================
    // 2. زر التعديل (Update)
    // ==========================================
    const updateBtn = e.target.closest(".btn-update-file");
    if (updateBtn) {
      if (updateBtn.disabled) return;

      const imageId = updateBtn.dataset.id;
      const card = updateBtn.closest(".dynamic-upload-card");
      if (!card || !imageId) return;

      const commentInput = card.querySelector(".comment-input");
      if (!commentInput) return;
      const commentText = commentInput.value.trim();

      // فحص النص
      if (!commentText) {
        commentInput.classList.add("comment-error");
        return;
      }
      commentInput.classList.remove("comment-error");

      // حفظ القيم والألوان الأصلية
      const originalHTML = updateBtn.innerHTML;
      const originalBg = updateBtn.style.backgroundColor;
      const originalColor = updateBtn.style.color;

      updateBtn.disabled = true;
      updateBtn.style.opacity = "0.7";
      updateBtn.innerHTML = `جاري الحفظ...`;

      const formData = new FormData();
      formData.append("id", imageId);
      formData.append("model_name", "InspectionItemImage");
      formData.append("comment", commentText);
      formData.append("action", "update");

      try {
        const minDelay = new Promise((resolve) => setTimeout(resolve, 500));
        const [response] = await Promise.all([
          ajax_request(SAVE_VISIT_URL, formData, "حدث خطأ أثناء تعديل التعليق:"),
          minDelay,
        ]);

        if (response && response.status === "success") {
          updateBtn.style.opacity = "1";
          updateBtn.style.backgroundColor = "#198754"; // green
          updateBtn.style.color = "#ffffff";
          updateBtn.innerHTML = `تم الحفظ ✓`;

          setTimeout(() => {
            updateBtn.innerHTML = originalHTML;
            updateBtn.style.backgroundColor = originalBg;
            updateBtn.style.color = originalColor;
            updateBtn.disabled = false;
          }, 1500);
        } else {
          updateBtn.style.opacity = "1";
          updateBtn.style.backgroundColor = "#dc3545"; // red
          updateBtn.style.color = "#ffffff";
          updateBtn.innerHTML = `فشل الحفظ ✕`;

          setTimeout(() => {
            updateBtn.innerHTML = originalHTML;
            updateBtn.style.backgroundColor = originalBg;
            updateBtn.style.color = originalColor;
            updateBtn.disabled = false;
          }, 1500);
        }
      } catch (error) {
        updateBtn.style.opacity = "1";
        updateBtn.style.backgroundColor = "#dc3545";
        updateBtn.style.color = "#ffffff";
        updateBtn.innerHTML = `فشل الحفظ ✕`;

        setTimeout(() => {
          updateBtn.innerHTML = originalHTML;
          updateBtn.style.backgroundColor = originalBg;
          updateBtn.style.color = originalColor;
          updateBtn.disabled = false;
        }, 1500);
      }
      return; // إنهاء التنفيذ لأن الضغطة كانت لزر التعديل
    }

    // ==========================================
    // 2. زر الحذف (Delete)
    // ==========================================
    const deleteBtn = e.target.closest(".btn-delete-file");
    if (deleteBtn) {
      if (deleteBtn.disabled) return;
      const imageId = deleteBtn.dataset.id;
      const card = deleteBtn.closest(".dynamic-upload-card");
      if (!card || !imageId) return;

      const isConfirmed = await showConfirmModal("هل أنت متأكد من حذف هذه", "البطاقة");
      if (!isConfirmed) return;

      const originalHTML = deleteBtn.innerHTML;

      // حالة التحميل (Spinner)
      deleteBtn.disabled = true;
      deleteBtn.style.opacity = "0.6";
      deleteBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i>`;

      const formData = new FormData();
      formData.append("id", imageId);
      formData.append("model_name", "InspectionItemImage");
      formData.append("action", "delete");

      try {
        const minDelay = new Promise((resolve) => setTimeout(resolve, 500));
        const [response] = await Promise.all([
          ajax_request(SAVE_VISIT_URL, formData, "حدث خطأ أثناء حذف البطاقة:"),
          minDelay,
        ]);

        if (response && response.status === "success") {
          // تأثير اختفاء وتصغير سلس قبل إزالة البطاقة نهائياً من DOM
          card.style.transition = "all 0.3s ease";
          card.style.opacity = "0";
          card.style.transform = "scale(0.9)";

          setTimeout(() => {
            card.remove();
          }, 300);
        } else {
          deleteBtn.innerHTML = originalHTML;
          deleteBtn.disabled = false;
          deleteBtn.style.opacity = "1";
        }
      } catch (error) {
        deleteBtn.innerHTML = originalHTML;
        deleteBtn.disabled = false;
        deleteBtn.style.opacity = "1";
      }
      return;
    }
  });
});

function showConfirmModal(messageText, itemName) {
  return new Promise((resolve) => {
    const template = document.getElementById("confirm-modal-template");

    if (!messageText || !itemName || !template) {
      resolve(false);
      return;
    }

    const clone = template.content.cloneNode(true);
    const overlay = clone.querySelector(".custom-modal-overlay");

    overlay.querySelector(".modal-text").textContent = messageText;
    overlay.querySelector(".item-name").textContent = itemName;

    overlay.querySelector(".btn-cancel").onclick = () => {
      overlay.remove();
      resolve(false);
    };

    overlay.querySelector(".btn-confirm").onclick = () => {
      overlay.remove();
      resolve(true);
    };

    document.body.appendChild(overlay);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("recommendationsContainer");
  const template = document.getElementById("recommendationCardTemplate");
  const panel = document.getElementById("recommendation-wrapper");
  if (!container || !panel || !template) return;


  panel.addEventListener("click", async function (e) {
    const saveBtn = e.target.closest("#addRecommendationBtn");
    // إكمال فتح قوس الـ if لضمان تنفيذ الطلب فقط عند النقر على الزر
    if (saveBtn) {
      const payload = {
        id: visitId, // تأكد أن visitId معرف في النطاق (Scope) الأعلى
        name: "ReportRecommendation",
        action: "save",
      };

      const result = await ajax_json(SAVE_INSPECTION_URL, payload);

      if (result && result.status === "success") {
        const realId = result.id;
        const realNumber = result.number;
        // 1. تجهيز الـ HTML وإضافته للـ DOM
        let cardHtml = template.innerHTML
          .replaceAll("__ID__", result.id)
          .replaceAll("__NUMBER__", result.number);

        container.insertAdjacentHTML("beforeend", cardHtml);

        // 2. جلب البطاقة وتجهيز حالة البدء (نفس أرقام حركة الحذف المكسورة)
        const newCard = container.lastElementChild;
        newCard.style.opacity = "0";
        newCard.style.transform = "scale(0.9)";
        newCard.style.transition = "all 0.3s ease-in-out";

        // 3. تشغيل الحركة فوراً لتظهر بنعومة (Fade + Scale-up)
        setTimeout(() => {
          newCard.style.opacity = "1";
          newCard.style.transform = "scale(1)";
        }, 50);
      }


    }
  });

  // مراقبة كتابة التوصيات لإظهار أو إخفاء زر الحفظ
  container.addEventListener("input", (e) => {
    if (e.target.classList.contains("rec-text")) {
      const input = e.target;

      // ابحث عن زر الحفظ المرتبط بهذه التوصية
      const saveBtn = input.closest(".recommendation-card")?.querySelector(".btn-save-rec");
      if (!saveBtn) return;

      // قارن النص الحالي بالنص الأصلي المخزن
      const originalValue = input.getAttribute("data-original-value") || "";
      const currentValue = input.value.trim();

      const isChanged = currentValue !== originalValue && currentValue !== "";

      // أظهر أو ائخفِ زر الحفظ باستخدام كلاس show
      saveBtn.classList.toggle("show", isChanged);
    }
  });

  container.addEventListener("click", async function (e) {
    const deleteBtn = e.target.closest(".btn-delete-rec");


    if (deleteBtn) {
      const recId = deleteBtn.dataset.id;

      if (!recId) return;

      const payload = {
        id: recId,
        name: "ReportRecommendation",
        action: "delete",
      };

      const result = await ajax_json(SAVE_INSPECTION_URL, payload, "خطأ أثناء حذف التوصية:");

      if (result && result.status === "success") {
        const cardElement = document.getElementById(`rec-card-${recId}`);

        if (cardElement) {
          cardElement.style.transition = "all 0.3s ease-in-out";
          cardElement.style.opacity = "0";
          cardElement.style.transform = "scale(0.9)";

          setTimeout(() => {
            cardElement.remove();

            updateCardNumbers();
          }, 300);
        }
      }


      function updateCardNumbers() {
        const remainingCards = document.querySelectorAll(".recommendation-card");
        remainingCards.forEach((card, index) => {
          const numberElement = card.querySelector(".rec-number");
          if (numberElement) {
            numberElement.textContent = index + 1;
          }
        });
      }
    }

    // -------------------------------------------------
    const saveRecBtn = e.target.closest(".btn-save-rec");
    if (saveRecBtn) {
      const card = saveRecBtn.closest(".recommendation-card");
      if (!card) return;

      const textarea = card?.querySelector(".rec-text");
      if (!textarea) return;
      const recId = saveRecBtn.getAttribute("data-id");
      const newValue = textarea.value.trim();
      if (!recId || !newValue) return;

      saveRecBtn.disabled = true;
      saveRecBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

      const payload = {
        id: recId,
        name: "ReportRecommendation",
        action: "update",
        text: newValue,
      };

      const result = await ajax_json(SAVE_INSPECTION_URL, payload, "خطأ أثناء حفظ التوصية:");

      await new Promise((resolve) => setTimeout(resolve, 1000));

      if (result?.status === "success") {
        textarea.setAttribute("data-original-value", newValue);

        saveRecBtn.classList.add("save-success");
        saveRecBtn.innerHTML = '<i class="fa-solid fa-check"></i>';

        setTimeout(() => {
          saveRecBtn.classList.remove("show", "save-success");
          saveRecBtn.disabled = false;
          saveRecBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i>';
        }, 1500);
      } else {
        saveRecBtn.classList.add("save-error");
        saveRecBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';

        setTimeout(() => {
          saveRecBtn.classList.remove("save-error");
          saveRecBtn.disabled = false;
          saveRecBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i>';
        }, 1500);
      }
    }
  });
});






const addBtn = document.getElementById("inspectVisitBtn");
if (addBtn) {
  addBtn.addEventListener("click", async function () {
    const container = document.getElementById("eport-submit-error");
    const template = document.getElementById("report-submit-template");
    const reportBtn = document.getElementById("show-report-btn");
    const reportMsg = document.getElementById("report-success-msg");
    if (!template || !container || !reportBtn || !reportMsg) return;
    addBtn.disabled = true;
    reportBtn.disabled = true;


    const data = await ajax_get(`/visit/inspection/${visitId}/`);
    if (data && data.status === "success") {
      container.innerHTML = "";
      reportBtn.classList.remove("d-none");
      reportMsg.classList.remove("d-none");
      addBtn.disabled = false;
      reportBtn.disabled = false;
      reportBtn.type = "submit";
    } else if (data && data.status === "error") {
      reportBtn.classList.add("d-none");
      reportMsg.classList.add("d-none");
      container.innerHTML = "";
      if (Array.isArray(data.items)) {
        data.items.forEach(function (item) {
          const clone = template.content.cloneNode(true);
          clone.querySelector(".alert-error").textContent = item.message;
          container.appendChild(clone);
        });
      }
    }
  });
}
