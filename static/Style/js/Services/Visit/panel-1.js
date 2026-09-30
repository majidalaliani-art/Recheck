if (status === "in_progress") {
  document.addEventListener("DOMContentLoaded", function () {
    const cityElement = document.getElementById("map-data-visit");
    const cityName = cityElement ? cityElement.dataset.city : "Riyadh";

    const latField =
      document.getElementById("id_latitude") || document.querySelector('[name="latitude"]');
    const lngField =
      document.getElementById("id_longitude") || document.querySelector('[name="longitude"]');

    const streets = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
    });

    const satellite = L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      {
        attribution: "Esri Satellite",
      },
    );

    // 2. إنشاء الخريطة
    const map = L.map("property-map-visit", {
      center: [24.7136, 46.6753], // الرياض افتراضي
      zoom: 11,
      layers: [streets],
    });

    // 3. زر التبديل (Toggle)
    const ToggleControl = L.Control.extend({
      onAdd: function (map) {
        const btn = L.DomUtil.create(
          "button",
          "leaflet-bar leaflet-control leaflet-control-custom",
        );
        btn.type = "button";
        btn.innerHTML = "🛰️ Satellite";
        btn.style.backgroundColor = "white";
        btn.style.padding = "5px 10px";
        btn.style.cursor = "pointer";
        btn.style.fontWeight = "bold";
        btn.style.borderRadius = "5px";
        btn.style.border = "2px solid #d4af37";
        btn.style.zIndex = "1000";
        L.DomEvent.disableClickPropagation(btn);

        btn.onclick = function () {
          if (map.hasLayer(satellite)) {
            map.removeLayer(satellite);
            map.addLayer(streets);
            btn.innerHTML = "🛰️ Satellite";
          } else {
            map.removeLayer(streets);
            map.addLayer(satellite);
            btn.innerHTML = "🗺️ Streets";
          }
        };
        return btn;
      },
    });
    map.addControl(new ToggleControl({ position: "topright" }));

    // 4. المنطق الذكي: هل توجد إحداثيات مخزنة؟
    let marker;
    const savedLat = latField ? parseFloat(latField.value) : null;
    const savedLng = lngField ? parseFloat(lngField.value) : null;

    if (savedLat && savedLng) {
      // حالة: الموقع موجود (تعديل عقار)
      map.setView([savedLat, savedLng], 16); // زووم قريب جداً للموقع المخزن
      marker = L.marker([savedLat, savedLng]).addTo(map);
    } else {
      // حالة: موقع جديد (البحث عن المدينة)
      const geocodeUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(cityName + ", Saudi Arabia")}&format=json&limit=1`;
      fetch(geocodeUrl)
        .then((response) => response.json())
        .then((data) => {
          if (data && data.length > 0) {
            map.setView([parseFloat(data[0].lat), parseFloat(data[0].lon)], 13);
          }
        })
        .catch((err) => console.log("Error fetching location:", err));
    }

    // 5. التعامل مع الضغط في الخريطة لتغيير الموقع
    map.on("click", function (e) {
      const lat = e.latlng.lat.toFixed(6);
      const lng = e.latlng.lng.toFixed(6);

      if (marker) {
        marker.setLatLng(e.latlng);
      } else {
        marker = L.marker(e.latlng).addTo(map);
      }

      if (latField && lngField) {
        latField.value = lat;
        lngField.value = lng;
      }
    });

    setTimeout(function () {
      map.invalidateSize();
    }, 300);
  });

  document.addEventListener("DOMContentLoaded", function () {
    // 1. تحديد العناصر (تأكد أن الـ input له نفس الاسم في ملف الـ HTML)
    const fileInput = document.querySelector('input[name="property_image"]');
    const uploadBox = document.querySelector(".upload-box");

    if (fileInput) {
      fileInput.addEventListener("change", function () {
        const file = this.files[0];

        if (file) {
          const reader = new FileReader();

          reader.onload = function (e) {
            const imageUrl = e.target.result;

            // 2. البحث عن الصورة وزر المعاينة (Fancybox)
            let imgPreview = document.getElementById("img-preview");
            let previewTrigger = document.getElementById("preview-image-trigger");
            const placeholder = document.querySelector(".upload-placeholder");

            // --- تحديث أو إنشاء الصورة داخل صندوق الرفع ---
            if (imgPreview) {
              imgPreview.src = imageUrl;
            } else {
              // إنشاء عنصر صورة جديد إذا لم يكن موجوداً (في حال كانت الحالة الأساسية فارغة)
              imgPreview = document.createElement("img");
              imgPreview.src = imageUrl;
              imgPreview.id = "img-preview";
              imgPreview.className = "preview-image img-fluid";
              uploadBox.appendChild(imgPreview);
            }

            // --- تحديث أو إنشاء زر المعاينة (العين) ليعمل مع الصورة الجديدة ---
            if (previewTrigger) {
              previewTrigger.href = imageUrl; // تحديث رابط العرض للـ Fancybox
            } else {
              // إذا لم يكن زر المعاينة موجوداً أصلاً (لأن العقار جديد بلا صورة قديمة)، نقوم بإنشائه وإضافته
              const goldUploadCard = document.querySelector(".gold-upload-card");
              if (goldUploadCard) {
                const newTrigger = document.createElement("a");
                newTrigger.href = imageUrl;
                newTrigger.className = "view-image-btn";
                newTrigger.id = "preview-image-trigger";
                newTrigger.setAttribute("data-fancybox", "property-gallery");
                newTrigger.title = "عرض الصورة كاملة";
                newTrigger.innerHTML = '<i class="fa-solid fa-eye"></i>';
                goldUploadCard.prepend(newTrigger); // إضافته داخل الكارد
              }
            }

            // 3. إخفاء الـ Placeholder (الأيقونة والنص) إن وجدت
            if (placeholder) {
              placeholder.style.display = "none";
            }
          };

          reader.readAsDataURL(file);
        }
      });
    }
  });
} else {
  document.addEventListener("DOMContentLoaded", function () {
    const cityElement = document.getElementById("map-data-visit");
    const cityName = cityElement ? cityElement.dataset.city : "Riyadh";

    const latField =
      document.getElementById("id_latitude") || document.querySelector('[name="latitude"]');
    const lngField =
      document.getElementById("id_longitude") || document.querySelector('[name="longitude"]');

    const streets = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
    });

    const satellite = L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      {
        attribution: "Esri Satellite",
      },
    );

    // 1. إنشاء خريطة ثابتة بالكامل (Read-Only)
    const map = L.map("property-map-visit", {
      center: [24.7136, 46.6753],
      zoom: 15,
      layers: [streets],
      zoomControl: false, // إلغاء أزرار التكبير والتصغير
      dragging: false, // منع سحب الخريطة بالماوس
      scrollWheelZoom: false, // منع التكبير بسكرول الماوس
      doubleClickZoom: false, // منع التكبير بالضغط المزدوج
      boxZoom: false, // منع التكبير بالتحديد
      keyboard: false, // منع التحكم بالأسهم
      touchZoom: false, // منع التكبير باللمس
    });

    // 2. زر التبديل بين الخريطة والقمر الصناعي (اختياري، يمكنك حذفه إن لم تحتاجه)
    const ToggleControl = L.Control.extend({
      onAdd: function (map) {
        const btn = L.DomUtil.create(
          "button",
          "leaflet-bar leaflet-control leaflet-control-custom",
        );
        btn.type = "button";
        btn.innerHTML = "🛰️ Satellite";
        btn.style.backgroundColor = "white";
        btn.style.padding = "5px 10px";
        btn.style.cursor = "pointer";
        btn.style.fontWeight = "bold";
        btn.style.borderRadius = "5px";
        btn.style.border = "2px solid #d4af37";
        btn.style.zIndex = "1000";
        L.DomEvent.disableClickPropagation(btn);

        btn.onclick = function () {
          if (map.hasLayer(satellite)) {
            map.removeLayer(satellite);
            map.addLayer(streets);
            btn.innerHTML = "🛰️ Satellite";
          } else {
            map.removeLayer(streets);
            map.addLayer(satellite);
            btn.innerHTML = "🗺️ Streets";
          }
        };
        return btn;
      },
    });
    map.addControl(new ToggleControl({ position: "topright" }));

    // 3. قراءة الإحداثيات وتثبيت الـ Marker فقط
    const savedLat = latField ? parseFloat(latField.value) : null;
    const savedLng = lngField ? parseFloat(lngField.value) : null;

    if (savedLat && savedLng) {
      map.setView([savedLat, savedLng], 16);
      L.marker([savedLat, savedLng]).addTo(map);
    } else {
      // في حال عدم وجود إحداثيات، يتم الانتقال للمدينة افتراضياً
      const geocodeUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(cityName + ", Saudi Arabia")}&format=json&limit=1`;
      fetch(geocodeUrl)
        .then((response) => response.json())
        .then((data) => {
          if (data && data.length > 0) {
            const lat = parseFloat(data[0].lat);
            const lon = parseFloat(data[0].lon);
            map.setView([lat, lon], 13);
            L.marker([lat, lon]).addTo(map);
          }
        })
        .catch((err) => console.log("Error fetching location:", err));
    }

    setTimeout(function () {
      map.invalidateSize();
    }, 300);
  });
}
