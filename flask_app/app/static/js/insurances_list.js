

function displayInsurances(insuranceData) {
    insuranceData.forEach(function(insurance) {
        var tableBody = document.getElementById('insuranceTableBody');
        var row = document.createElement('tr');
        row.innerHTML = `
            <td>${insurance.label}</td>
            <td>${insurance.unit_type}</td>
            <td>${insurance.value}</td>
            <td>${insurance.price}</td>
            <td>${insurance.due_date}</td>
            <td>${insurance.company}</td>
        `;
        tableBody.appendChild(row);
    });
}

function displayInsurance(insuranceData) {
    var tableBody = document.getElementById('insuranceTableBody');
    var row = document.createElement('tr');
    row.innerHTML = `
        <td>${insuranceData.label}</td>
        <td>${insuranceData.unit_type}</td>
        <td>${insuranceData.value}</td>
        <td>${insuranceData.price}</td>
        <td>${insuranceData.due_date}</td>
        <td>${insuranceData.company}</td>
    `;
    tableBody.appendChild(row);
}

function emptyTable() {
    var tableBody = document.getElementById('insuranceTableBody');
    // Remove all child nodes
    while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
    }
}


function runInsuranceTransaction(db) {
    console.log('Running transaction...');
    var transaction = db.transaction(['insurance'], 'readonly');
    var insuranceStore = transaction.objectStore('insurance');            
    
    return insuranceStore
}

const request = indexedDB.open('bodovision', 1);


request.onsuccess = function(event) {
    // Get the current date
    var currentDate = new Date().toISOString().slice(0, 10);
    var db = event.target.result;
    
    let filterClicked = false
    
    const filter = document.getElementById('filter').onclick = function(event) {
        event.preventDefault();
        filterClicked = true
        const filterValue = document.getElementById('insuranceStatus');
        if (filterValue.value === 'insured') {
            emptyTable();
            insuranceStore = runInsuranceTransaction(db);
            insuranceStore.openCursor().onsuccess = function(event) {
                const cursor = event.target.result;
                if (cursor) {
                    if (cursor.value.due_date > currentDate && (cursor.value.price !== null && cursor.value.price !== 0)) {
                        displayInsurance(cursor.value);
                    }
                    cursor.continue();
                }
            }
        } else if (filterValue.value === 'uninsured') {
            emptyTable();
            insuranceStore = runInsuranceTransaction(db);
            insuranceStore.openCursor().onsuccess = function(event) {
                const cursor = event.target.result;
                if (cursor) {
                    if (cursor.value.due_date < currentDate || cursor.value.price === 0 || cursor.value.price === null) {
                        displayInsurance(cursor.value);
                    }
                    cursor.continue();
                }
            }
        } else if (filterValue.value === 'all') {
            emptyTable();
            insuranceStore = runInsuranceTransaction(db);
            insuranceStore.getAll().onsuccess = function(event) {
                displayInsurances(event.target.result);
            }
        }
    };

    if (!filterClicked) {
        emptyTable();
        insuranceStore = runInsuranceTransaction(db);
        insuranceStore.getAll().onsuccess = function(event) {
            displayInsurances(event.target.result);
        }
    }
    
};

// Handle database opening error
request.onerror = function(event) {
    console.error('Error opening database:', event.target.error);
};