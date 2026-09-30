export function showError(containerId, message) {
  const box = document.getElementById(containerId);

  box.innerHTML = `
    <div class="alert alert-danger py-2 mt-2" style="font-size: 0.85rem">
      <i class="fas fa-exclamation-circle me-1"></i>
      <span>${message}</span>
    </div>
  `;
}