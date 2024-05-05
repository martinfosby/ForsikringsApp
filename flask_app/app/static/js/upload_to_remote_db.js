// Open a connection to IndexedDB
var request = indexedDB.open('yourDBName', 1);

request.onsuccess = function(event) {
    var db = event.target.result;
    var transaction = db.transaction(['insurance'], 'readonly');
    var store = transaction.objectStore('insurance');
    var data = [];

    // Retrieve data from IndexedDB
    store.openCursor().onsuccess = function(event) {
        var cursor = event.target.result;
        if (cursor) {
            // Add each item to the data array
            data.push(cursor.value);
            cursor.continue();
        } else {
            // Format the data as needed (e.g., to JSON)
            var jsonData = JSON.stringify(data);

            // Send the data to your remote database
            fetch('/api/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: jsonData,
            }).then(response => {
                if (response.ok) {
                    console.log('Data uploaded successfully!');
                } else {
                    console.error('Error uploading data:', response.statusText);
                }
            }).catch(error => {
                console.error('Error uploading data:', error);
            });
        }
    };
};

request.onerror = function(event) {
    console.error('Error opening database:', event.target.error);
};
