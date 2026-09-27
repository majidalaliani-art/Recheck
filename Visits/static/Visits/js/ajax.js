const visitIdAjax = document.getElementById("visit-id").value;
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

async function sendPostData(url, formData, errorMessage='Connection error:') {
  if (!csrftoken) {
    console.error("CSRF token not found!");
    return null;
  }

  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken,
      },
    });

    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      return await response.json();
    }
    return await response.text();
  } catch (err) {
    console.error(errorMessage, err);
    return null;
  }
}

async function uploadSingleFile(fileInput, Id, tableName, fileType, fileCategory, comment, fileId) {
  const file = fileInput.files[0];
  if (!file) return;
  if (fileId && fileCategory === "image") {
    fileId.src = URL.createObjectURL(file);
  }
  if (!csrftoken) {
    console.error("CSRF token missing");
    return;
  }
  const formData = new FormData();
  formData.append("file", file);
  formData.append("id", Id);
  formData.append("table", tableName);
  formData.append("type", fileType);
  formData.append("comment", comment);
  formData.append("category", fileCategory);
  sendPostData("/upload_single_file/", formData);
}

document.addEventListener("change", function (e) {
  const el = e.target;
  if (el.hasAttribute("data-file")) {
    const Id = el.getAttribute("data-file");
    const tableName = el.getAttribute("data-table");
    const fileType = el.getAttribute("data-type");
    const fileCategory = el.getAttribute("data-category");
    const container = el.getAttribute("img-id");
    const imgId = document.getElementById(container);

    if (
      typeof uploadSingleFile === "function" &&
      tableName &&
      Id &&
      fileType &&
      fileCategory &&
      imgId
    ) {
      uploadSingleFile(el, Id, tableName, fileType, fileCategory, imgId);
    } else {
      console.error("Error: Missing required data or container not found!");
    }
  }
});

async function createCard(tableName, Name, Id, containerId) {
  if (!visitIdAjax || !tableName || !Name || !containerId) return;
  const formData = new FormData();
  formData.append("table", tableName);
  formData.append("id", Id);
  formData.append("name", Name);
  formData.append("action", "add");
  try {
    const result = await sendPostData(`/visit/${visitIdAjax}/card/`, formData);
    if (!result) return;

    const cardValue = result.id || null;
    if (!cardValue) return;

    generateCardHTML({ cardValue, tableName, containerId });
  } catch (err) {
    console.error("Error creating card:", err);
  }
}

async function deleteCard(Id, tableName) {
  if (!Id || !tableName) return;
  const formData = new FormData();
  formData.append("table", tableName);
  formData.append("id", Id);
  formData.append("action", "delete");
  const result = await sendPostData("/create_card/", formData);
  if (!result) return;
  if (result.status === "success") {
    const cardEl = document.getElementById(`card-${Id}`);
    if (cardEl) cardEl.remove();
    //console.log(`Card ${Id} deleted successfully.`);
  } else {
    console.error("Error deleting card:", result.message || "Unknown error");
  }
}

function generateCardHTML({ cardValue, containerId }) {
  if (!cardValue || !containerId) return "";
  else if (containerId === "container-rooms") {
    const container = document.getElementById(containerId);
    if (!container) return;
    const parentCard = document.createElement("div");
    parentCard.className = "card";
    parentCard.id = `card-${cardValue}`;
    container.appendChild(parentCard);
    const template = document.getElementById("card-template-rooms");
    if (!template) return;
    const clone = template.content.cloneNode(true);
    const cardValueInputs = clone.querySelectorAll(".room-item-btn");
    if (cardValueInputs) {
      cardValueInputs.forEach((btn) => {
        btn.onclick = () => {
          const cardName = btn.getAttribute("data-name");
          createCard("roomItems", cardName, cardValue, "container-room-items");
        };
      });
    }

    const deleteBtn = clone.querySelector(".delete-btn");

    if (deleteBtn) {
      deleteBtn.onclick = () => deleteCard(cardValue, "room");
    }
    parentCard.appendChild(clone);
  } else if (containerId === "container-room-items") {
    const container = document.getElementById(containerId);

    if (!container) return;

    const parentCard = document.createElement("div");
    //console.log(`Card ${parentCard} deleted successfully.`);
    parentCard.className = "card";

    parentCard.id = `card-${cardValue}`;

    container.appendChild(parentCard);
    const template = document.getElementById("card-template-room-items");
    if (!template) return;
    const clone = template.content.cloneNode(true);
    const cardValueInputs = clone.querySelectorAll(".room-item-btn");
    if (cardValueInputs) {
      cardValueInputs.forEach((btn) => {
        btn.onclick = () => {
          const cardName = btn.getAttribute("data-name");
          createCard("roomItems", cardName, cardValue, "container-rooms-items");
        };
      });
    }

    const deleteBtn = clone.querySelector(".delete-btn");
    if (deleteBtn) {
      deleteBtn.onclick = () => deleteCard(cardValue, "room");
    }
    parentCard.appendChild(clone);
  } else {
    return "";
  }
}
