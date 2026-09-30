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
  const clientMap = L.map("map").setView([23.8859, 45.0792], 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 19,
  }).addTo(clientMap);
  cities.forEach((city) => {
    if (!city.is_active || !city.lat || !city.lng || city.radius <= 0)  return;
    L.circle([city.lat, city.lng], {
      color: "#1a73e8",
      weight: 2,
      fillColor: "#1a73e8",
      fillOpacity: 0.2,
      radius: city.radius,
    })
      .addTo(clientMap)
      .bindPopup(city.name);
  });
};