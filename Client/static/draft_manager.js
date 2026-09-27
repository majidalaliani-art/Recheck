

const STORAGE_KEY = 'site_global_draft';

function saveFormData() {
    const form = document.querySelector('form');
    if (!form) return;

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}


function loadFormData() {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    const form = document.querySelector('form');
    if (!form || !saved) return;

    Object.keys(saved).forEach(key => {
        const input = form.elements[key];
        if (input) {
            if (input.type === 'radio') {
                const radio = form.querySelector(`input[name="${key}"][value="${saved[key]}"]`);
                if (radio) radio.checked = true;
            } else {
                input.value = saved[key];
            }
        }
    });
}


function initStorage() {
    loadFormData();

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('input', saveFormData);
    }
}
