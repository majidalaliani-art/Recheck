document.addEventListener("DOMContentLoaded", function () {
  const fileInputs = document.querySelectorAll(".file-input");

  fileInputs.forEach(function (fileInput) {
    const wrapper = fileInput.closest(".card-body-wrapper");
    const uploadLabel = wrapper.querySelector(".upload-area");
    const uploadIcon = wrapper.querySelector(".upload-area-icon");
    const uploadText = wrapper.querySelector(".upload-area-text .main-text");
    const fileNameDisplay = wrapper.querySelector(".file-name-display");
    const errorBox = wrapper.parentElement.querySelector(".comment-display-box");
    const originalText = uploadText.innerHTML;

    fileInput.addEventListener("change", function () {
      if (this.files && this.files.length > 0) {
        const file = this.files[0];
        const fileName = file.name;

        if (fileName.toLowerCase().endsWith(".pdf")) {
          uploadIcon.innerHTML = "📄";
          uploadText.innerHTML = "تم رفع الملف بنجاح!";
          fileNameDisplay.innerHTML = `📄 اسم الملف: ${fileName}`;
          fileNameDisplay.style.color = "#28a745";
          fileNameDisplay.style.display = "block";

          uploadLabel.style.borderColor = "#28a745";
          uploadLabel.style.backgroundColor = "rgba(40, 167, 69, 0.05)";

          errorBox.innerHTML = "";
          errorBox.classList.add("d-none");
        } else {
          errorBox.innerHTML = "صيغة الملف غير مدعومة";
          errorBox.style.color = "#dc3545";
          errorBox.classList.remove("d-none");

          uploadLabel.style.borderColor = "#dc3545";
          uploadLabel.style.backgroundColor = "transparent";
          fileNameDisplay.style.display = "none";
        }
      }
    });
  });
});

