

const visitsContainer = document.getElementById("visits-container");

const consultationContainer = document.getElementById("consultation-container");

document.getElementById("show-visits").addEventListener("click", () => {
  visitsContainer.classList.remove("d-none");
  document.getElementById("show-visits").classList.add("active");
  document.getElementById("show-consultations").classList.remove("active");
  consultationContainer.classList.add("d-none");
});

document.getElementById("show-consultations").addEventListener("click", () => {
  consultationContainer.classList.remove("d-none");
  document.getElementById("show-consultations").classList.add("active");
  document.getElementById("show-visits").classList.remove("active");
  visitsContainer.classList.add("d-none");
});
