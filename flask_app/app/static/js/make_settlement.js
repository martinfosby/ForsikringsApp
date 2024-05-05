const request = indexedDB.open('bodovision', 1);

request.onsuccess = function(event) {
    var db = event.target.result;
    var transaction = db.transaction(['insurance',], 'readonly');
    var insuranceStore = transaction.objectStore('insurance');

    insuranceStore.getAll().onsuccess = function(event) {
        // Assuming you have an array of values
        var insurances = event.target.result.map(function(insurance) {
            return insurance;
        });

        // Get the select element
        var selectElement = document.getElementById('insurance_label');

        // Clear previous options
        selectElement.innerHTML = '';

        // Loop through the array and create an option element for each value
        insurances.forEach(function(insurance) {
            var option = document.createElement('option');
            option.text = insurance.label;
            option.value = insurance.id; // Optionally, set the value attribute
            selectElement.appendChild(option);
        });
    };

    document.getElementById('submit').onclick = function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();
        var settlementTransaction = db.transaction(['settlement',], 'readwrite');
        var settlementStore = settlementTransaction.objectStore('settlement');

        var addRequest = settlementStore.add({
            insurance: document.getElementById('insurance_label').selectedOptions[0].textContent,
            description: document.getElementById('description').value,
            sum: parseInt(document.getElementById('sum').value),
        });

        // Redirect to settlements list page after successful addition
        addRequest.onsuccess = function(event) { 
            window.location.href = '/settlements';
        };

        addRequest.onerror = function(event) {
            console.error('Error adding data:', event.target.error);
        };
    };

};

request.onerror = function(event) {
    console.error('Error opening database:', event.target.error);
};