const globalSocket = new WebSocket(
  `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws/global/`,
);

function updateContactElements(data) {
  if (!data || !data.key) return;

  const key = data.key;
  if (data.is_active) {
    document.querySelectorAll(`.contact-${key}-is_active`).forEach((el) => {
      el.classList.remove("d-none");
    });

    document.querySelectorAll(`.contact-${key}-Link`).forEach((el) => {
      if (data.link) {
        el.href = data.link;
      }
    });

    document.querySelectorAll(`.contact-${key}-User`).forEach((el) => {
      if (data.user) {
        el.textContent = data.user;
      }
    });
  } else {
    document.querySelectorAll(`.contact-${key}-is_active`).forEach((el) => {
      el.classList.add("d-none");
    });
  }
}

function updatePaymentElements(data) {
  if (!data || !data.key) return;
  const key = data.key;
  if (data.is_active) {
    document.querySelectorAll(`.pay-${key}-is_active`).forEach((el) => {
      el.classList.remove("d-none");
    });
  } else {
    document.querySelectorAll(`.pay-${key}-is_active`).forEach((el) => {
      el.classList.add("d-none");
    });
  }
}

globalSocket.onmessage = function (event) {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case "client_visit_card":
      const prefix = data.key;
      Object.keys(data).forEach((key) => {
        const el = document.querySelector(`.${prefix}_${key}`);
        if (!el) return;
        if ("value" in el) {
          el.value = data[key];
        } else {
          el.textContent = data[key];
        }
      });

      break;

    case "client_consultation_card":
      const priceEl = document.getElementById("price-consultation");
      const durationEl = document.getElementById("duration-consultation");
      if (priceEl) priceEl.textContent = data.price;
      if (durationEl) durationEl.textContent = data.duration;
      break;

    case "contact_method":
      if (data.key === "contact_email") {
        updateContactElements(data);
      }
      if (data.key === "contact_number") {
        updateContactElements(data);
      }
      if (data.key === "WhatsApp") {
        updateContactElements(data);
      }
      if (data.key === "Instagram") {
        updateContactElements(data);
      }
      if (data.key === "TikTok") {
        updateContactElements(data);
      }
      if (data.key === "X") {
        updateContactElements(data);
      }

      break;

    case "payment_method":
      if (data.key === "Mada") {
        updatePaymentElements(data);
      }
      if (data.key === "Visa") {
        updatePaymentElements(data);
      }
      if (data.key === "Mastercard") {
        updatePaymentElements(data);
      }

      if (data.key === "Applepay") {
        updatePaymentElements(data);
      }

      if (data.key === "Tamara") {
        updatePaymentElements(data);
      }
      if (data.key === "Tabby") {
        updatePaymentElements(data);
      }

      break;

    case "city_toggle":
      const select = document.querySelector(".live-cities");
      const option = select.querySelector(`option[value="${data.code}"]`);

      if (option && !data.is_active) {
        option.remove();
      }

      if (option && option.textContent !== data.name) {
        option.textContent = data.name;
      }

      if (!option && data.is_active) {
        const newOption = document.createElement("option");
        newOption.value = data.code;
        newOption.textContent = data.name;
        select.appendChild(newOption);
      }

      break;
    default:
      console.warn("Unknown type:", data.type);
      break;
  }
};
