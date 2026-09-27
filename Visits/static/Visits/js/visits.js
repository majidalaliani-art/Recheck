////////////////////////////////////////////////////////////////////////////////
// let isRestoring = false;
// const storageKey = 'survey_data_' + visitId;
// let usedIndices = new Set();
// let maxIndex = 0;
// ////////////////////////////////////////////////////////////////////////////////

// function getNextAvailableIndex() {
//     let i = 1;
//     while (usedIndices.has(i)) {
//         i++;
//     }
//     return i;
// }

// document.addEventListener('DOMContentLoaded', async function() {
//     const savedStep = localStorage.getItem('lastStep') || 1;
//     goToStep(savedStep, false);

//     await loadInspectionData();
//     await loadFormData();
//     rebuildCardsFromData();
//     bindAllRatingSliders();


//     window.usedIndices = window.usedIndices || new Set();
//     window.maxIndex = window.maxIndex || 0;

//     document.querySelectorAll('.apartment-card').forEach(card => {
//         const idx = card.dataset.cardIndex;
//         if (idx) {
//             usedIndices.add(parseInt(idx));
//             maxIndex = Math.max(maxIndex, parseInt(idx));
//         }
//     });

//     const addPhotoBtn = document.getElementById('add-photo-btn');
//     if (addPhotoBtn) {
//         addPhotoBtn.addEventListener('click', addNewPhotoRow);
//     }

//     const addCardBtn = document.getElementById('add-apartment-card-btn');
//     if (addCardBtn) {
//         addCardBtn.addEventListener('click', function() {
//             const newIndex = getNextAvailableIndex();
//             usedIndices.add(newIndex);
//             if (newIndex > maxIndex) maxIndex = newIndex;
//             addNewCard(newIndex);
//         });
//     }

//     const container = document.getElementById('main-cards-container');
//     if (container.children.length === 0) {
//         const firstIndex = getNextAvailableIndex();
//         usedIndices.add(firstIndex);
//         maxIndex = Math.max(maxIndex, firstIndex);
//         addNewCard(firstIndex);
//     }

//     document.addEventListener('change', saveFormData);
//     document.addEventListener('input', saveFormData);

//     observer.observe(document.body, {childList: true,subtree: true});
// });

////////////////////////////////////////////////////////////////////////////////

// function removeElement(button, selector) {
//     const element = button.closest(selector);
//     if (!element) return;
//     if (selector === '.apartment-card') {
//         const cardIndex = element.dataset.cardIndex;
//         if (cardIndex) {
//             usedIndices.delete(parseInt(cardIndex));
//         }
//     }

//     element.remove();
//     saveFormData();
// }

// ==========================================
// NAVIGATION
// ==========================================



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// function toggleCardView(cardIndex, mode) {
//     const details = document.getElementById('details-view-' + cardIndex);
//     const reviews = document.getElementById('reviews-view-' + cardIndex);
//     if (mode === 'details') {
//         details.style.display = 'block';
//         reviews.style.display = 'none';
//     } else {
//         details.style.display = 'none';
//         reviews.style.display = 'block';
//     }

//     // حفظ التغيير عشان يتذكر أنت في أي صفحة
//     saveFormData();
// }

// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// let inspectionDatabase = {};
// async function loadInspectionData() {
//     try {
//         const response = await fetch(dataUrl);
//         if (!response.ok) {
//             throw new Error('Failed to load inspection data');
//         }
//         const data = await response.json();
//         inspectionDatabase = data.inspection_schema;
//     } catch (error) {
//         console.error('❌ Error loading JSON:', error);
//     }
// }

// function toggleItemMenu(cardIndex) {
//     const menu = document.getElementById('item-menu-' + cardIndex);
//     if (menu.style.display === 'none') {
//         menu.style.display = 'block';
//         if (menu.children.length === 0) {
//             loadItemsToMenu(cardIndex, menu);
//         }
//     } else {
//         menu.style.display = 'none';
//     }
// }

// function addItemToSections(card, itemData) {
//     const cardIndex = card.dataset.cardIndex;
//     if (!cardIndex) {
//         console.warn('cardIndex not found');
//         return;
//     }

//     const sections = ['details', 'reviews'];

//     sections.forEach(section => {
//         const sectionDiv = document.getElementById(`${section}-view-${cardIndex}`);
//         if (!sectionDiv) {
//             console.warn(`Section ${section}-view-${cardIndex} not found`);
//             return;
//         }

//         const container = sectionDiv.querySelector('.items-container');
//         if (!container) {
//             console.warn(`Items container not found in section ${section}-view-${cardIndex}`);
//             return;
//         }

//         let template = document.getElementById('item-template').innerHTML;
//         template = template.replace(/{itemUniqueId}/g, itemData.uniqueId)
//                            .replace(/{itemName}/g, itemData.name)
//                            .replace(/{itemType}/g, itemData.id);

//         container.insertAdjacentHTML('beforeend', template);

//         const newItem = container.lastElementChild;

//         const reportContent = newItem.querySelector('.item-report-content');
//         const evalContent = newItem.querySelector('.item-evaluation-content');

//         if (section === 'details') {
//             reportContent.style.display = 'block';
//             evalContent.style.display = 'none';
//         } else {
//             reportContent.style.display = 'none';
//             evalContent.style.display = 'block';
//         }

//         if (itemData.room) {
//             newItem.dataset.room = itemData.room;
//             newItem.dataset.roomDisplay = itemData.roomDisplay || '';
//         }
//     });

//     saveFormData();
// }

// function addNewCard(index) {
//     const container = document.getElementById('main-cards-container');
//     let template = document.getElementById('apartment-card-template').innerHTML;
//     template = template.replace(/{cardIndex}/g, index);
//     container.insertAdjacentHTML('beforeend', template);

//     if (inspectionType === 'standard') {
//         const menu = document.getElementById('item-menu-' + index);
//         if (menu) {
//             loadItemsToMenu(index, menu);
//         }
//     }

//     saveFormData();
// }



// function addItemToApartment(cardIndex, itemId, itemName) {
//     const card = document.querySelector(`.apartment-card[data-card-index="${cardIndex}"]`);
//     if (!card) return;

//     const isItemExist = card.querySelector(`.item-box[data-item-type="${itemId}"]`);
//     if (isItemExist) {
//         return;
//     }

//     const itemUniqueId = 'item_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
//     const itemData = {
//         uniqueId: itemUniqueId,
//         id: itemId,
//         name: itemName,
//         room: null,
//         roomDisplay: null
//     };

//     addItemToSections(card, itemData);

//     const menu = document.getElementById(`item-menu-${cardIndex}`);
//     if (menu) {
//         const btn = menu.querySelector(`button[data-item-id="${itemId}"]`);
//         if (btn) {
//             btn.disabled = true;
//             btn.style.opacity = '0.5';
//             btn.style.cursor = 'not-allowed';
//         }
//     }
// }

// function loadItemsToMenu(cardIndex, menu) {
//     const items = inspectionDatabase.standard;
//     if (!items) return;

//     const card = document.querySelector(`.apartment-card[data-card-index="${cardIndex}"]`);

//     items.forEach(item => {
//         const btn = document.createElement('button');
//         btn.textContent = item.name;
//         btn.classList.add('item-menu-btn');
//         btn.dataset.itemId = item.id;

//         const isAlreadyAdded = card && card.querySelector(`.item-box[data-item-type="${item.id}"]`);
//         if (isAlreadyAdded) {
//             btn.disabled = true;
//             btn.style.opacity = '0.5';
//             btn.style.cursor = 'not-allowed';
//         }

//         btn.onclick = function() {
//             addItemToApartment(cardIndex, item.id, item.name);
//             btn.disabled = true;
//             btn.style.opacity = '0.5';
//             btn.style.cursor = 'not-allowed';
//         };
//         menu.appendChild(btn);
//     });
// }

// function removeItem(itemUniqueId) {
//     const items = document.querySelectorAll(`[data-item-id="${itemUniqueId}"]`);
//     if (items.length === 0) return;

//     const firstItem = items[0];
//     const itemType = firstItem.dataset.itemType;
//     const card = firstItem.closest('.apartment-card');
//     const cardIndex = card ? card.dataset.cardIndex : null;

//     items.forEach(el => el.remove());

//     if (cardIndex && itemType) {
//         const menu = document.getElementById(`item-menu-${cardIndex}`);
//         if (menu) {
//             const btn = menu.querySelector(`button[data-item-id="${itemType}"]`);
//             if (btn) {
//                 btn.disabled = false;
//                 btn.style.opacity = '1';
//                 btn.style.cursor = 'pointer';
//             }
//         }
//     }

//     saveFormData();
// }

// function saveFormData() {
//     if (isRestoring) {
//         return;
//     }

//     const formData = {};
//     const itemsMap = new Map();

//     document.querySelectorAll('div[id^="details-view"] .item-box').forEach(item => {
//         const itemId = item.dataset.itemId;
//         if (!itemId) return;

//         if (itemsMap.has(itemId)) return;

//         const card = item.closest('.apartment-card');
//         const cardIndex = card ? card.dataset.cardIndex : null;
//         const itemType = item.dataset.itemType || item.querySelector('.item-type')?.value;
//         const itemNameElem = item.querySelector('.item-name');
//         const itemName = itemNameElem ? itemNameElem.textContent : null;
//         const room = item.dataset.room || null;
//         const reportText = item.querySelector('.item-report-content textarea')?.value || '';

//         itemsMap.set(itemId, {
//             uniqueId: itemId,
//             id: itemType,
//             name: itemName,
//             room: room,
//             report: reportText,
//             cardIndex: cardIndex
//         });
//     });

//     formData.items = Array.from(itemsMap.values());

//     const cards = [];
//     document.querySelectorAll('.apartment-card').forEach(card => {
//         const idx = card.dataset.cardIndex;
//         if (idx) {
//             const reviewsView = document.getElementById(`reviews-view-${idx}`);
//             const activeView = (reviewsView && reviewsView.style.display === 'block') ? 'reviews' : 'details';
//             cards.push({ index: parseInt(idx), activeView: activeView });
//         }
//     });
//     formData.cards = cards;

//     const inputs = document.querySelectorAll('input, textarea, select');
//     inputs.forEach(input => {
//         if (!input.name || input.type === 'file' || input.name.includes('csrfmiddlewaretoken')) return;
//         if (input.type === 'checkbox') {
//             formData[input.name] = input.checked;
//         } else if (input.type === 'radio') {
//             if (input.checked) formData[input.name] = input.value;
//         } else {
//             formData[input.name] = input.value;
//         }
//     });

//     localStorage.setItem(storageKey, JSON.stringify(formData));
// }

// async function loadFormData() {
//     const savedData = localStorage.getItem(storageKey);
//     if (savedData) {
//         const data = JSON.parse(savedData);
//         Object.keys(data).forEach(name => {
//             const inputs = document.querySelectorAll(`[name="${name}"]`);

//             inputs.forEach(input => {
//                 if (input.type === 'checkbox') {
//                     input.checked = data[name];
//                 } else if (input.type === 'radio') {
//                     if (input.value === data[name]) input.checked = true;
//                 } else {
//                     input.value = data[name];
//                 }
//             });
//         });
//     }
// }

// function clearSavedData() {
//     localStorage.removeItem(storageKey);
// }

// function rebuildCardsFromData() {
//     isRestoring = false;

//     const savedData = localStorage.getItem(storageKey);
//     if (!savedData) return;

//     const data = JSON.parse(savedData);
//     const container = document.getElementById('main-cards-container');
//     container.innerHTML = '';

//     if (data.cards && data.cards.length > 0) {
//         data.cards.forEach(cardData => {
//             const cardIndex = typeof cardData === 'object' ? cardData.index : cardData;
//             addNewCard(cardIndex);

//             if (typeof cardData === 'object' && cardData.activeView) {
//                 toggleCardView(cardIndex, cardData.activeView);
//             }
//         });
//     }

//     if (data.items && data.items.length > 0) {
//         data.items.forEach(itemData => {
//             const card = document.querySelector(`.apartment-card[data-card-index="${itemData.cardIndex}"]`);
//             if (!card) return;

//             const restoredItemData = {
//                 uniqueId: itemData.uniqueId,
//                 id: itemData.id,
//                 name: itemData.name,
//                 room: itemData.room,
//                 roomDisplay: itemData.room
//             };
//             addItemToSections(card, restoredItemData);

//             const itemElement = card.querySelector(`[data-item-id="${itemData.uniqueId}"]`);
//             if (itemElement) {
//                 const textarea = itemElement.querySelector('.item-report-content textarea');
//                 if (textarea) textarea.value = itemData.report || '';
//             }
//         });
//     }

//     document.querySelectorAll('.apartment-card').forEach(card => {
//         const cardIndex = card.dataset.cardIndex;
//         const menu = document.getElementById(`item-menu-${cardIndex}`);
//         if (menu) {
//             card.querySelectorAll('.item-box').forEach(itemBox => {
//                 const itemId = itemBox.dataset.itemType;
//                 const btn = menu.querySelector(`button[data-item-id="${itemId}"]`);
//                 if (btn) {
//                     btn.disabled = true;
//                     btn.style.opacity = '0.5';
//                     btn.style.cursor = 'not-allowed';
//                 }
//             });
//         }
//     });
// }



// function saveFormData() {
//     document.querySelectorAll('input, textarea, select').forEach(el => {
//         if (el.name && el.type !== 'file') {
//             if (el.type === 'checkbox') localStorage.setItem(el.name, el.checked);
//             else if (el.type === 'radio') { if (el.checked) localStorage.setItem(el.name, el.value); }
//             else localStorage.setItem(el.name, el.value);
//         }
//     });
// }

// function loadFormData() {
//     document.querySelectorAll('input, textarea, select').forEach(el => {
//         if (el.name && el.type !== 'file') {
//             const savedValue = localStorage.getItem(el.name);
//             if (savedValue !== null) {
//                 if (el.type === 'checkbox') el.checked = (savedValue === 'true');
//                 else if (el.type === 'radio') { if (el.value === savedValue) el.checked = true; }
//                 else el.value = savedValue;
//             }
//         }
//     });
// }

// document.addEventListener('DOMContentLoaded', function() {
//     const savedStep = localStorage.getItem('lastStep') || 1;


//     goToStep(savedStep);
//     loadFormData();

//     document.addEventListener('input', saveFormData);
// });




// function addNewCard(index) {
//     const container = document.getElementById('main-cards-container');

//     let template = document.getElementById('card-template').innerHTML;

//     template = template.replace(/{cardIndex}/g, index);
//     container.insertAdjacentHTML('beforeend', template);
//     if (inspectionType === 'standard') {
//         const menu = document.getElementById('item-menu-' + index);
//         if (menu) {
//             loadItemsToMenu(index, menu);
//         }
//     }
//     saveFormData();
// }











// function manageOpenCards(action) {
//     const container = document.getElementById('main-cards-container');
//     if (action === 'restore') {
//         const saved = JSON.parse(localStorage.getItem('openCards') || '[]');
//         saved.forEach(idx => {
//             let template = document.getElementById('card-template').innerHTML;
//             template = template.replace(/{cardIndex}/g, idx);
//             container.insertAdjacentHTML('beforeend', template);
//         });
//     } else if (action === 'save') {
//         const openCards = Array.from(document.querySelectorAll('.apartment-card'))
//                                .map(c => parseInt(c.dataset.cardIndex));
//         localStorage.setItem('openCards', JSON.stringify(openCards));
//     } else if (action === 'clear') {
//         container.innerHTML = '';
//         localStorage.removeItem('openCards');
//     }
// }

/// =================== goToStep =================== ///
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
///--------------------------------------------------///

/// ================== manageForm ================== ///
async function manageForm(action) {
    if (action === 'save') {
        document.querySelectorAll('.item-box').forEach(item => {
            const itemId = item.dataset.itemId;
            if (itemId) {
                const textarea = item.querySelector('textarea');
                if (textarea) localStorage.setItem(`item_report_${itemId}`, textarea.value);
                const itemType = item.dataset.itemType || item.querySelector('.item-type')?.value;
                if (itemType) localStorage.setItem(`item_type_${itemId}`, itemType);
            }
        });

        document.querySelectorAll('.apartment-card').forEach(card => {
            const idx = card.dataset.cardIndex;
            if (idx) {
                const reviewsView = document.getElementById(`reviews-view-${idx}`);
                const activeView = (reviewsView && reviewsView.style.display === 'block') ? 'reviews' : 'details';
                localStorage.setItem(`card_view_${idx}`, activeView);
            }
        });

        document.querySelectorAll('input, textarea, select').forEach(el => {
            if (el.name && el.type !== 'file' && !el.name.includes('csrf')) {
                if (el.type === 'checkbox') localStorage.setItem(el.name, el.checked);
                else if (el.type === 'radio') { if (el.checked) localStorage.setItem(el.name, el.value); }
                else localStorage.setItem(el.name, el.value);
            }
        });

    } else if (action === 'load') {
        document.querySelectorAll('.item-box').forEach(item => {
            const itemId = item.dataset.itemId;
            if (itemId) {
                const savedReport = localStorage.getItem(`item_report_${itemId}`);
                const textarea = item.querySelector('textarea');
                if (savedReport !== null && textarea) textarea.value = savedReport;
            }
        });

        document.querySelectorAll('.apartment-card').forEach(card => {
            const idx = card.dataset.cardIndex;
            if (idx) {
                const savedView = localStorage.getItem(`card_view_${idx}`);
                if (savedView) {
                    const reviewsView = document.getElementById(`reviews-view-${idx}`);
                    const detailsView = document.getElementById(`details-view-${idx}`);
                    if (reviewsView && detailsView) {
                        reviewsView.style.display = (savedView === 'reviews') ? 'block' : 'none';
                        detailsView.style.display = (savedView === 'details') ? 'block' : 'none';
                    }
                }
            }
        });

        document.querySelectorAll('input, textarea, select').forEach(el => {
            if (el.name && el.type !== 'file') {
                const savedValue = localStorage.getItem(el.name);
                if (savedValue !== null) {
                    if (el.type === 'checkbox') el.checked = (savedValue === 'true');
                    else if (el.type === 'radio') { if (el.value === savedValue) el.checked = true; }
                    else el.value = savedValue;
                }
            }
        });

    } else if (action === 'clear' || action === 'silent') {
        localStorage.clear();
        if (action === 'clear') location.reload();
    }
}
/// ------------------------------------------------ ///


/// ================== initMap ================== ///

window.myMap = null;
window.myMarker = null;

async function initMap() {
    const latInput = document.getElementById('id_latitude') || document.querySelector('[name="latitude"]');
    const lngInput = document.getElementById('id_longitude') || document.querySelector('[name="longitude"]');
    const titleInput = document.getElementById('id_detailed_title') || document.querySelector('[name="detailed_title"]');
    const neighborhoodInput = document.getElementById('id_neighborhood') || document.querySelector('[name="neighborhood"]');


    const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');


    let startLat = parseFloat(localStorage.getItem('latitude')) || 21.5433;
    let startLng = parseFloat(localStorage.getItem('longitude')) || 39.1728;
    let startZoom = localStorage.getItem('latitude') ? 16 : 13;


    window.myMap = L.map('map_container', {
        layers: [localStorage.getItem('preferred_map_type') === 'Satellite map' ? satelliteLayer : streetLayer],
        minZoom: 2,
        worldCopyJump: true
    }).setView([startLat, startLng], startZoom);

    window.myMarker = L.marker([startLat, startLng], { draggable: true }).addTo(window.myMap);


    const ToggleControl = L.Control.extend({
        options: { position: 'topleft' },
        onAdd: function () {
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control-custom');
            container.innerHTML = '<a href="#"><i class="fa fa-layer-group"></i></a>';
            L.DomEvent.disableClickPropagation(container);
            container.onclick = function (e) {
                e.preventDefault();
                if (window.myMap.hasLayer(streetLayer)) {
                    window.myMap.removeLayer(streetLayer); window.myMap.addLayer(satelliteLayer);
                    localStorage.setItem('preferred_map_type', 'Satellite map');
                } else {
                    window.myMap.removeLayer(satelliteLayer); window.myMap.addLayer(streetLayer);
                    localStorage.setItem('preferred_map_type', 'Street map');
                }
            };
            return container;
        }
    });
    window.myMap.addControl(new ToggleControl());


    async function fetchAddress(lat, lng) {
        try {
            const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}&accept-language=ar`);
            const data = await res.json();
            if (data.address) {
                if (titleInput) titleInput.value = data.address.road || data.address.suburb || "";
                if (neighborhoodInput) neighborhoodInput.value = data.address.suburb || data.address.neighbourhood || "";
                [titleInput, neighborhoodInput].forEach(el => el && el.dispatchEvent(new Event('input', { bubbles: true })));
            }
        } catch (e) { }
    }


    function sync(lat, lng, updateAddress = true) {
        if (latInput) latInput.value = lat.toFixed(8);
        if (lngInput) lngInput.value = lng.toFixed(8);

        localStorage.setItem('latitude', lat.toFixed(8));
        localStorage.setItem('longitude', lng.toFixed(8));

        window.myMarker.setLatLng([lat, lng]);
        if (updateAddress) fetchAddress(lat, lng);

        [latInput, lngInput].forEach(el => el && el.dispatchEvent(new Event('input', { bubbles: true })));
    }


    window.myMap.on('click', e => sync(e.latlng.lat, e.latlng.lng));
    window.myMarker.on('dragend', () => sync(window.myMarker.getLatLng().lat, window.myMarker.getLatLng().lng));

    setTimeout(() => { window.myMap.invalidateSize(); }, 300);
}

/// --------------------------------------------- ///



/// ================== uploadPropertyImage ================== ///

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// async function uploadPropertyImage(file) {
//     if (!file) return;
//     const previewImg = document.getElementById('image-preview');
//     const wrapper = document.querySelector('.image-preview-wrapper');
//     const emptyText = document.getElementById('empty-image-text');
//     const reader = new FileReader();
//     reader.onload = (ev) => {
//         if (previewImg) {
//             previewImg.src = ev.target.result;
//             if (wrapper) wrapper.style.display = 'block';
//             if (emptyText) emptyText.style.display = 'none';
//         }
//     };
//     reader.readAsDataURL(file);
//     const formData = new FormData();
//     formData.append('entrance_image', file);
//     formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
//     formData.append('image_type', 'entrance');
//     const parentId = document.getElementById('order_id')?.value;
//     if (parentId) formData.append('order_id', parentId);
//     try {
//         const res = await fetch('/upload_image_ajax/', {
//             method: 'POST',
//             body: formData
//         });
//         const data = await res.json();
//         if (data.status === 'success' && data.url && previewImg) {
//             previewImg.src = data.url;
//         } else {
//             console.error('Failed to upload image');
//         }
//     } catch (err) {
//         console.log("Upload failed");
//     }
// }




/// -------------------------------------------------------- ///









function manageCard(action, cardSelectorOrId, button = null, containerId = null) {
    const container = containerId ? document.getElementById(containerId) : null;
    if (action === 'add' && cardSelectorOrId && container) {
        const templateElement = document.getElementById(cardSelectorOrId);
        if (templateElement && container) {
            const timestamp = Date.now();
            const randomNum = Math.floor(Math.random() * 1000000);
            const index = `${timestamp}${randomNum}`;
            let template = templateElement.innerHTML;
            template = template.replace(/{cardIndex}/g, index);
            container.insertAdjacentHTML('beforeend', template);
            saveCards(containerId);

        } else {
            console.error(`manageCard: "${cardSelectorOrId}" or "${containerId}" is not a valid ID!`);
        }

    } else if (action === 'remove' && cardSelectorOrId && button) {

        const parentCard = button.closest(cardSelectorOrId);
        if (parentCard) {
            const parentContainerId = parentCard.parentElement.id;
            parentCard.remove();
              // if (parentCard) {parentCard.remove();saveOpenCards(container);}

            if (parentContainerId) {
                saveCards(parentContainerId);
            }
        }
    }
}


function saveCards(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    localStorage.setItem(`savedCards_${containerId}`, container.innerHTML);

    localStorage.setItem(`cardCounter_${containerId}`, cardCounter);
}

function restoreCards(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const savedHTML = localStorage.getItem(`savedCards_${containerId}`);
    const savedCounter = localStorage.getItem(`cardCounter_${containerId}`);

    if (savedHTML) {
        container.innerHTML = savedHTML;
    }

    if (savedCounter) {
        cardCounter = parseInt(savedCounter);
    }
}













function initCards() {
    const container = document.getElementById('units-container');
    const addBtn = document.getElementById('add-unit-btn');


    if (addBtn) {
        addBtn.addEventListener('click', () => {
            manageCard('add', 'unit-template', null, 'units-container');
        });
    }

    if (container.children.length === 0) {
        manageCard('add','unit-template', null, 'units-container');
    } else {

    }
}










document.addEventListener('DOMContentLoaded', async function() {





      const savedStep = localStorage.getItem('lastStep') || 1;


    const imageInput = document.getElementById('id_entrance_image');
    if (imageInput) imageInput.onchange = (e) => uploadPropertyImage(e.target.files[0]);

    if (typeof goToStep === 'function') goToStep(savedStep);

    if (document.getElementById('map_container')) { await initMap(); }



    restoreCards('units-container');
    await manageForm('load');
    initCards();







    setTimeout(() => {
        document.addEventListener('input', () => manageForm('save'));
        document.addEventListener('change', () => manageForm('save'));
    }, 500);

});









async function manageCardDB(action, cardSelectorOrId, button = null, containerId = null) {
    const formData = new FormData();
    formData.append('action', action);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken')); // تأكد إن دالة getCookie موجودة عندك

    if (action === 'add' && cardSelectorOrId && containerId) {
        const container = document.getElementById(containerId);
        const templateElement = document.getElementById(cardSelectorOrId);

        // جلب رقم الزيارة (لازم يكون عندك input مخفي في الصفحة يحمل رقم الزيارة)
        const visitId = document.getElementById('visit_id')?.value;

        if (templateElement && container) {
            formData.append('visit_id', visitId);

            try {
                // نكلم السيرفر عشان يسوي الجدول في القاعدة
                const response = await fetch('/manage_unit_ajax/', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.status === 'success') {
                    // السيرفر أنشأ السجل ورجع لنا الـ ID الحقيقي (مثلاً: 1712210345)
                    const realId = data.unit_id;

                    // نأخذ التمبلت حقك ونبدل {cardIndex} بالرقم اللي جاء من القاعدة
                    let template = templateElement.innerHTML;
                    template = template.replace(/{cardIndex}/g, realId);

                    container.insertAdjacentHTML('beforeend', template);
                    console.log("تم إنشاء الجدول في القاعدة بنجاح برقم:", realId);

                    // شلنا saveCards لأن القاعدة صارت هي المخزن الأساسي!
                } else {
                    alert("خطأ من السيرفر: " + data.message);
                }
            } catch (error) {
                console.error("فشل الاتصال بالسيرفر:", error);
            }
        } else {
            console.error(`manageCardDB: "${cardSelectorOrId}" or "${containerId}" is not a valid ID!`);
        }

    // ==========================================
    // 2. الحذف (مسح من القاعدة ثم من الشاشة)
    // ==========================================
    } else if (action === 'remove' && cardSelectorOrId && button) {
        const parentCard = button.closest(cardSelectorOrId);

        if (parentCard) {
            // نأخذ الـ ID من الكرت عشان نعلم السيرفر مين يحذف
            const unitId = parentCard.getAttribute('data-card-index');

            // إذا المستخدم ما وافق على الحذف، نوقف الدالة
            if (!confirm("هل أنت متأكد من حذف هذا الجدول وكل بياناته من القاعدة نهائياً؟")) return;

            formData.append('unit_id', unitId);

            try {
                // نكلم السيرفر يمسح الجدول
                const response = await fetch('/manage_unit_ajax/', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.status === 'success') {
                    // إذا انحذف من القاعدة، نشيله من قدامك في المتصفح
                    parentCard.remove();
                    console.log("تم حذف الجدول من القاعدة بنجاح");
                } else {
                    alert("فشل الحذف: " + data.message);
                }
            } catch (error) {
                console.error("فشل الاتصال بالسيرفر:", error);
            }
        }
    }
}
