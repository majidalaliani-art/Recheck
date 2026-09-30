
const orderSocket = new WebSocket(
  `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws/orders/`,
);

function updateFieldStatus(iconElement, status, errorElement, notes, iconName) {
  if (iconElement) {
    const statusClasses = {
      required: "fa-circle-exclamation exclamation-icon",
      pending: "fa-clock clock-icon",
      accepted: "fa-circle-check check-icon",
      rejected: "fa-circle-xmark xmark-icon",
    };

    const stateClass = statusClasses[status] || "fa-question";
    iconElement.className = `fa-solid ${stateClass} ${iconName}`;
      if (errorElement) {
        if (status === "required") {
          if (notes) {
            errorElement.innerHTML = notes;
            errorElement.classList.remove("d-none");
          } else {
            errorElement.innerHTML = "";
            errorElement.classList.add("d-none");
          }
        } else {
          errorElement.innerHTML = "";
          errorElement.classList.add("d-none");
        }
      }
  }

}


orderSocket.onmessage = function (event) {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case "order_status_updated":
      const payment_order = document.getElementById(`order-card-${data.id}`);
      if (payment_order) {
        const status = payment_order.querySelector(".status-orders");
        status.textContent = data.status_text;
        status.className = `status-orders status-orders-${data.status_class}`;
      }
      break;

    case "visit_status_new":
      if (document.getElementById(`order-card-${data.id}`)) return;
      const template = document.getElementById("visit-card-template");
      const clone = template.content.cloneNode(true);
      const visitOrder = clone.querySelector(".order-card");
      visitOrder.id = `order-card-${data.id}`;

      clone.querySelector(".order-number").textContent = data.id;
      const statusEl = clone.querySelector(".status-orders");
      statusEl.textContent = data.status_text;
      statusEl.classList.add(data.status);

      clone.querySelector(".city-neighborhood").textContent = data.neighborhood + ", " + data.city;
      clone.querySelector(".area-size").textContent = data.property_size;

      clone.querySelector(".property-type").textContent = data.property_type;
      clone.querySelector(".detail-tag").textContent = data.inspection_type;
      clone.querySelector(".amount").textContent = data.price;
      clone.querySelector(".day-date").textContent = data.day;
      clone.querySelector(".time").textContent = data.time_slot;

      clone.querySelector(".view-order").href = `/order/${data.id}/`;
      document.getElementById("visits-container")?.prepend(clone);
      break;

    case "consultation_status_new":
      if (document.getElementById(`order-card-${data.id}`)) return;
      const templateConsultation = document.getElementById("consultation-card-template");
      const cloneConsultation = templateConsultation.content.cloneNode(true);

      const consultationOrder = cloneConsultation.querySelector(".order-card");
      consultationOrder.id = `order-card-${data.id}`;
      cloneConsultation.querySelector(".order-number").textContent = data.id;
      const statusElConsultation = cloneConsultation.querySelector(".status-orders");
      statusElConsultation.textContent = data.status_text;
      statusElConsultation.className = `status-orders status-orders-${data.status_class}`;

      cloneConsultation.querySelector(".day-date").textContent = data.work_history;
      cloneConsultation.querySelector(".time").textContent = data.work_time;
      cloneConsultation.querySelector(".amount").textContent = data.price;

      cloneConsultation.querySelector(".view-order").href = `/order/${data.id}/`;
      document.getElementById("consultation-container").prepend(cloneConsultation);
      break;

    case "applicant_status_updated":
      const data = JSON.parse(event.data);
      const applicant = document.getElementById("applicant-status");
      const container = document.getElementById("status-container");
      if (!applicant && !container) return;

      if (data.status === "pending") {
        const template = document.getElementById("tmpl-pending");
        if (!template) return;
        const clone = template.content.cloneNode(true);
        container.innerHTML = "";
        container.appendChild(clone);
        
        const degree_error = document.querySelector(".degree_error");
        const degree_icon = document.querySelector(".degree-icon");
        updateFieldStatus(
          degree_icon,
          data.degree_status,
          degree_error,
          data.degree_notes,
          "degree-icon",
        );
        // 2
        const iban_icon = document.querySelector(".iban-icon");
        const iban_error = document.querySelector(".iban_error");
        updateFieldStatus(iban_icon, data.iban_status, iban_error, data.iban_notes, "iban-icon");
        // 3
        const sce_icon = document.querySelector(".sce-icon");
        const sce_error = document.querySelector(".sce_error");
        updateFieldStatus(sce_icon, data.sce_status, sce_error, data.sce_notes, "sce-icon");
        // 4
        const cv_icon = document.querySelector(".cv-icon");
        const cv_error = document.querySelector(".cv_error");
        updateFieldStatus(cv_icon, data.cv_status, cv_error, data.cv_notes, "cv-icon");
        // 5
        const equipment_icon = document.querySelector(".equipment-icon");
        const equipment_error = document.querySelector(".equipment_error");
        updateFieldStatus(
          equipment_icon,
          data.equipment_status,
          equipment_error,
          data.equipment_notes,
          "equipment-icon",
        );

      }else if (data.status === "rejected"){
          const template = document.getElementById("tmpl-rejected");
          if (!template) return;
          const clone = template.content.cloneNode(true);
          container.innerHTML = "";
          container.appendChild(clone);

      } else if (data.status === "accepted") {
        const template = document.getElementById("tmpl-accepted");
        if (!template) return;
        const clone = template.content.cloneNode(true);
        container.innerHTML = "";
        container.appendChild(clone);
      }


      break;

    default:
      console.warn("Unknown message type:", data.type);
  }
};

orderSocket.onerror = (error) => {
  console.error("WebSocket encountered an error:", error);
};
