if (document.querySelector(".mySwiper")) {
  new Swiper(".mySwiper", {
    loop: true,
    autoplay: {
      delay: 2500,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });
}

new Swiper(".opinion-swiper", {
  loop: true,
  spaceBetween: 20,

  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },

  breakpoints: {
    320: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 2,
    },
  },
});

const toggle = document.querySelector(".menu-toggle");
const menu = document.querySelector(".side-menu");

toggle?.addEventListener("click", function () {
  menu.classList.toggle("active");
  this.classList.toggle("active");

  document.body.classList.toggle("no-scroll");
});

window.onload = function () {
  const clientMap = L.map("map").setView([24.2, 45.0], 6);
  L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
    attribution: '&copy; Esri, DeLorme, NAVTEQ',
    maxZoom: 18,
  }).addTo(clientMap);
  if (typeof cities !== "undefined" && Array.isArray(cities)) {
    cities.forEach((city) => {
      if (!city.is_active || !city.lat || !city.lng || city.radius <= 0) return;
      L.circle([city.lat, city.lng], {
        color: "#006870",
        weight: 2,
        fillColor: "#006870",
        fillOpacity: 0.18,
        radius: city.radius,
      })
        .addTo(clientMap)
        .bindPopup(`<strong>${city.name}</strong>`);
    });
  }
};