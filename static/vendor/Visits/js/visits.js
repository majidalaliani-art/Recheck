////////////////////////////////////////////////////////////////////////////////
let isRestoring = false;
const storageKey = 'survey_data_' + visitId;
let usedIndices = new Set();
let maxIndex = 0;
////////////////////////////////////////////////////////////////////////////////

function getNextAvailableIndex() {
    let i = 1;
    while (usedIndices.has(i)) {
        i++;
    }
    return i;
}

document.addEventListener('DOMContentLoaded', async function() {
    const savedStep = localStorage.getItem('lastStep') || 1;
    goToStep(savedStep, false);

    await loadInspectionData();
    await loadFormData();
    rebuildCardsFromData();
    bindAllRatingSliders();


    window.usedIndices = window.usedIndices || new Set();
    window.maxIndex = window.maxIndex || 0;

    document.querySelectorAll('.apartment-card').forEach(card => {
        const idx = card.dataset.cardIndex;
        if (idx) {
            usedIndices.add(parseInt(idx));
            maxIndex = Math.max(maxIndex, parseInt(idx));
        }
    });

    const addPhotoBtn = document.getElementById('add-photo-btn');
    if (addPhotoBtn) {
        addPhotoBtn.addEventListener('click', addNewPhotoRow);
    }

    const addCardBtn = document.getElementById('add-apartment-card-btn');
    if (addCardBtn) {
        addCardBtn.addEventListener('click', function() {
            const newIndex = getNextAvailableIndex();
            usedIndices.add(newIndex);
            if (newIndex > maxIndex) maxIndex = newIndex;
            addNewCard(newIndex);
        });
    }

    const container = document.getElementById('main-cards-container');
    if (container.children.length === 0) {
        const firstIndex = getNextAvailableIndex();
        usedIndices.add(firstIndex);
        maxIndex = Math.max(maxIndex, firstIndex);
        addNewCard(firstIndex);
    }

    document.addEventListener('change', saveFormData);
    document.addEventListener('input', saveFormData);

    observer.observe(document.body, {childList: true,subtree: true});
});

////////////////////////////////////////////////////////////////////////////////

function removeElement(button, selector) {
    const element = button.closest(selector);
    if (!element) return;
    if (selector === '.apartment-card') {
        const cardIndex = element.dataset.cardIndex;
        if (cardIndex) {
            usedIndices.delete(parseInt(cardIndex));
        }
    }

    element.remove();
    saveFormData();
}

// ==========================================
// NAVIGATION
// ==========================================


function goToStep(stepNumber, scroll = true) {
    const target = parseInt(stepNumber);

    for (let i = 1; i <= 5; i++) {

        const stepDiv = document.getElementById('step' + i);
        if (stepDiv) {
            stepDiv.style.display = 'none';
        }

        const tabBtn = document.getElementById('tab' + i);
        if (tabBtn) {
            tabBtn.classList.remove('active', 'completed');

            if (i < target) {
                tabBtn.classList.add('completed');
            }
            else if (i === target) {

                tabBtn.classList.add('active');
            }
        }
    }
    const currentDiv = document.getElementById('step' + target);
    if (currentDiv) {
        currentDiv.style.display = 'block';
    }
    localStorage.setItem('lastStep', target);

    if (scroll) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function toggleCardView(cardIndex, mode) {
    const details = document.getElementById('details-view-' + cardIndex);
    const reviews = document.getElementById('reviews-view-' + cardIndex);
    if (mode === 'details') {
        details.style.display = 'block';
        reviews.style.display = 'none';
    } else {
        details.style.display = 'none';
        reviews.style.display = 'block';
    }

    // حفظ التغيير عشان يتذكر أنت في أي صفحة
    saveFormData();
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

let inspectionDatabase = {};
async function loadInspectionData() {
    try {
        const response = await fetch(dataUrl);
        if (!response.ok) {
            throw new Error('Failed to load inspection data');
        }
        const data = await response.json();
        inspectionDatabase = data.inspection_schema;
    } catch (error) {
        console.error('❌ Error loading JSON:', error);
    }
}

function toggleItemMenu(cardIndex) {
    const menu = document.getElementById('item-menu-' + cardIndex);
    if (menu.style.display === 'none') {
        menu.style.display = 'block';
        if (menu.children.length === 0) {
            loadItemsToMenu(cardIndex, menu);
        }
    } else {
        menu.style.display = 'none';
    }
}

function addItemToSections(card, itemData) {
    const cardIndex = card.dataset.cardIndex;
    if (!cardIndex) {
        console.warn('cardIndex not found');
        return;
    }

    const sections = ['details', 'reviews'];

    sections.forEach(section => {
        const sectionDiv = document.getElementById(`${section}-view-${cardIndex}`);
        if (!sectionDiv) {
            console.warn(`Section ${section}-view-${cardIndex} not found`);
            return;
        }

        const container = sectionDiv.querySelector('.items-container');
        if (!container) {
            console.warn(`Items container not found in section ${section}-view-${cardIndex}`);
            return;
        }

        let template = document.getElementById('item-template').innerHTML;
        template = template.replace(/{itemUniqueId}/g, itemData.uniqueId)
                           .replace(/{itemName}/g, itemData.name)
                           .replace(/{itemType}/g, itemData.id);

        container.insertAdjacentHTML('beforeend', template);

        const newItem = container.lastElementChild;

        const reportContent = newItem.querySelector('.item-report-content');
        const evalContent = newItem.querySelector('.item-evaluation-content');

        if (section === 'details') {
            reportContent.style.display = 'block';
            evalContent.style.display = 'none';
        } else {
            reportContent.style.display = 'none';
            evalContent.style.display = 'block';
        }

        if (itemData.room) {
            newItem.dataset.room = itemData.room;
            newItem.dataset.roomDisplay = itemData.roomDisplay || '';
        }
    });

    saveFormData();
}

function addNewCard(index) {
    const container = document.getElementById('main-cards-container');
    let template = document.getElementById('apartment-card-template').innerHTML;
    template = template.replace(/{cardIndex}/g, index);
    container.insertAdjacentHTML('beforeend', template);

    if (inspectionType === 'standard') {
        const menu = document.getElementById('item-menu-' + index);
        if (menu) {
            loadItemsToMenu(index, menu);
        }
    }

    saveFormData();
}

function addItemToApartment(cardIndex, itemId, itemName) {
    const card = document.querySelector(`.apartment-card[data-card-index="${cardIndex}"]`);
    if (!card) return;

    const isItemExist = card.querySelector(`.item-box[data-item-type="${itemId}"]`);
    if (isItemExist) {
        return;
    }

    const itemUniqueId = 'item_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    const itemData = {
        uniqueId: itemUniqueId,
        id: itemId,
        name: itemName,
        room: null,
        roomDisplay: null
    };

    addItemToSections(card, itemData);

    const menu = document.getElementById(`item-menu-${cardIndex}`);
    if (menu) {
        const btn = menu.querySelector(`button[data-item-id="${itemId}"]`);
        if (btn) {
            btn.disabled = true;
            btn.style.opacity = '0.5';
            btn.style.cursor = 'not-allowed';
        }
    }
}

function loadItemsToMenu(cardIndex, menu) {
    const items = inspectionDatabase.standard;
    if (!items) return;

    const card = document.querySelector(`.apartment-card[data-card-index="${cardIndex}"]`);

    items.forEach(item => {
        const btn = document.createElement('button');
        btn.textContent = item.name;
        btn.classList.add('item-menu-btn');
        btn.dataset.itemId = item.id;

        const isAlreadyAdded = card && card.querySelector(`.item-box[data-item-type="${item.id}"]`);
        if (isAlreadyAdded) {
            btn.disabled = true;
            btn.style.opacity = '0.5';
            btn.style.cursor = 'not-allowed';
        }

        btn.onclick = function() {
            addItemToApartment(cardIndex, item.id, item.name);
            btn.disabled = true;
            btn.style.opacity = '0.5';
            btn.style.cursor = 'not-allowed';
        };
        menu.appendChild(btn);
    });
}

function removeItem(itemUniqueId) {
    const items = document.querySelectorAll(`[data-item-id="${itemUniqueId}"]`);
    if (items.length === 0) return;

    const firstItem = items[0];
    const itemType = firstItem.dataset.itemType;
    const card = firstItem.closest('.apartment-card');
    const cardIndex = card ? card.dataset.cardIndex : null;

    items.forEach(el => el.remove());

    if (cardIndex && itemType) {
        const menu = document.getElementById(`item-menu-${cardIndex}`);
        if (menu) {
            const btn = menu.querySelector(`button[data-item-id="${itemType}"]`);
            if (btn) {
                btn.disabled = false;
                btn.style.opacity = '1';
                btn.style.cursor = 'pointer';
            }
        }
    }

    saveFormData();
}

function saveFormData() {
    if (isRestoring) {
        return;
    }

    const formData = {};
    const itemsMap = new Map();

    document.querySelectorAll('div[id^="details-view"] .item-box').forEach(item => {
        const itemId = item.dataset.itemId;
        if (!itemId) return;

        if (itemsMap.has(itemId)) return;

        const card = item.closest('.apartment-card');
        const cardIndex = card ? card.dataset.cardIndex : null;
        const itemType = item.dataset.itemType || item.querySelector('.item-type')?.value;
        const itemNameElem = item.querySelector('.item-name');
        const itemName = itemNameElem ? itemNameElem.textContent : null;
        const room = item.dataset.room || null;
        const reportText = item.querySelector('.item-report-content textarea')?.value || '';

        itemsMap.set(itemId, {
            uniqueId: itemId,
            id: itemType,
            name: itemName,
            room: room,
            report: reportText,
            cardIndex: cardIndex
        });
    });

    formData.items = Array.from(itemsMap.values());

    const cards = [];
    document.querySelectorAll('.apartment-card').forEach(card => {
        const idx = card.dataset.cardIndex;
        if (idx) {
            const reviewsView = document.getElementById(`reviews-view-${idx}`);
            const activeView = (reviewsView && reviewsView.style.display === 'block') ? 'reviews' : 'details';
            cards.push({ index: parseInt(idx), activeView: activeView });
        }
    });
    formData.cards = cards;

    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        if (!input.name || input.type === 'file' || input.name.includes('csrfmiddlewaretoken')) return;
        if (input.type === 'checkbox') {
            formData[input.name] = input.checked;
        } else if (input.type === 'radio') {
            if (input.checked) formData[input.name] = input.value;
        } else {
            formData[input.name] = input.value;
        }
    });

    localStorage.setItem(storageKey, JSON.stringify(formData));
}

async function loadFormData() {
    const savedData = localStorage.getItem(storageKey);
    if (savedData) {
        const data = JSON.parse(savedData);
        Object.keys(data).forEach(name => {
            const inputs = document.querySelectorAll(`[name="${name}"]`);

            inputs.forEach(input => {
                if (input.type === 'checkbox') {
                    input.checked = data[name];
                } else if (input.type === 'radio') {
                    if (input.value === data[name]) input.checked = true;
                } else {
                    input.value = data[name];
                }
            });
        });
    }
}

function clearSavedData() {
    localStorage.removeItem(storageKey);
}

function rebuildCardsFromData() {
    isRestoring = false;

    const savedData = localStorage.getItem(storageKey);
    if (!savedData) return;

    const data = JSON.parse(savedData);
    const container = document.getElementById('main-cards-container');
    container.innerHTML = '';

    if (data.cards && data.cards.length > 0) {
        data.cards.forEach(cardData => {
            const cardIndex = typeof cardData === 'object' ? cardData.index : cardData;
            addNewCard(cardIndex);

            if (typeof cardData === 'object' && cardData.activeView) {
                toggleCardView(cardIndex, cardData.activeView);
            }
        });
    }

    if (data.items && data.items.length > 0) {
        data.items.forEach(itemData => {
            const card = document.querySelector(`.apartment-card[data-card-index="${itemData.cardIndex}"]`);
            if (!card) return;

            const restoredItemData = {
                uniqueId: itemData.uniqueId,
                id: itemData.id,
                name: itemData.name,
                room: itemData.room,
                roomDisplay: itemData.room
            };
            addItemToSections(card, restoredItemData);

            const itemElement = card.querySelector(`[data-item-id="${itemData.uniqueId}"]`);
            if (itemElement) {
                const textarea = itemElement.querySelector('.item-report-content textarea');
                if (textarea) textarea.value = itemData.report || '';
            }
        });
    }

    document.querySelectorAll('.apartment-card').forEach(card => {
        const cardIndex = card.dataset.cardIndex;
        const menu = document.getElementById(`item-menu-${cardIndex}`);
        if (menu) {
            card.querySelectorAll('.item-box').forEach(itemBox => {
                const itemId = itemBox.dataset.itemType;
                const btn = menu.querySelector(`button[data-item-id="${itemId}"]`);
                if (btn) {
                    btn.disabled = true;
                    btn.style.opacity = '0.5';
                    btn.style.cursor = 'not-allowed';
                }
            });
        }
    });
}
