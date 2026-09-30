const visitId = document.getElementById("visit-id").value;
document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".report-tabs-nav .report-tab");
  const panels = document.querySelectorAll(".tab-panel");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => {
        t.classList.remove("active");
      });

      tab.classList.add("active");

      panels.forEach((panel) => {
        panel.classList.remove("active");
      });

      const currentStep = tab.getAttribute("data-step");
      const targetPanel = document.getElementById(`panel-${currentStep}`);

      if (targetPanel) {
        targetPanel.classList.add("active");
      }
    });
  });
});

Fancybox.bind("[data-fancybox]", {

});



document.addEventListener("DOMContentLoaded", function () {
  // جلب الإحداثيات من حقول الـ hidden
  const latInput = document.getElementById("latitude");
  const lngInput = document.getElementById("longitude");

  if (latInput && lngInput && latInput.value && lngInput.value) {
    const lat = parseFloat(latInput.value);
    const lng = parseFloat(lngInput.value);

    // التأكد من أن الإحداثيات أرقام صحيحة وليست فارغة
    if (!isNaN(lat) && !isNaN(lng)) {
      // 1. إنشاء الخريطة وتحديد المركز ومستوى التقريب (Zoom Level)
      const map = L.map("report-map").setView([lat, lng], 16);

      // 2. تحميل بلاطات الخريطة (OpenStreetMap)
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap",
      }).addTo(map);

      // 3. إضافة دبوس/مؤشر الموقع (Marker)
      L.marker([lat, lng]).addTo(map).bindPopup("موقع العقار").openPopup();

      // إعادة ضبط حجم الخريطة لتفادي مشكلة العرض الناقص عند التحميل
      setTimeout(() => {
        map.invalidateSize();
      }, 300);
    }
  }
});
