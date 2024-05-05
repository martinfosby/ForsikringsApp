const request = indexedDB.open('bodovision', 1);

function displaySettlements(settlements) {
    const tableBody = document.getElementById('settlements');
    tableBody.innerHTML = '';

    settlements.forEach(function(settlement) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${settlement.insurance}</td>
            <td>${settlement.description}</td>
            <td>${settlement.sum}</td>
        `;
        tableBody.appendChild(row);
    });
}

request.onsuccess = function(event) {
    var db = event.target.result;
    var transaction = db.transaction(['settlement',], 'readonly');
    var settlementStore = transaction.objectStore('settlement');

    settlementStore.getAll().onsuccess = function(event) {
        displaySettlements(event.target.result);
    };
};

request.onerror = function(event) {
    console.error('Error opening database:', event.target.error);
};