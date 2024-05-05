

document.addEventListener('DOMContentLoaded', function() {
    const myForm = document.getElementById('insuranceForm');
    const mySubmitButton = document.getElementById('submitButton');

    mySubmitButton.onclick = function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        const request = indexedDB.open('bodovision', 1);



        request.onsuccess = function(event) {
            var db = event.target.result;
            var transaction = db.transaction(['insurance'], 'readwrite');
            var insuranceStore = transaction.objectStore('insurance');

            // Add new data to the store
            var insuranceData = {
                label: document.getElementById('label').value,
                unit_type: document.getElementById('unit_type_id').selectedOptions[0].textContent,
                value: parseInt(document.getElementById('value').value),
                price: parseInt(document.getElementById('price').value),
                due_date: document.getElementById('due_date').value,
                company: document.getElementById('company_id').selectedOptions[0].textContent
            };

            var addRequest = insuranceStore.add(insuranceData);

            addRequest.onerror = function(event) {
                console.error('Error adding data:', event.target.error);
            };

            addRequest.onsuccess = function(event) {
                // Redirect to insurances list page after successful addition
                window.location.href = '/insurances';
            };
        };

        
        request.onerror = function(event) {
            console.error('Error opening database:', event.target.error);
        };
    };
});
