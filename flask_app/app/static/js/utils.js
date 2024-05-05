export function runRequest() {
    // Open a connection to the IndexedDB database
    var request = indexedDB.open('bodovision', 1);

    // Define the database schema and object stores
    request.onupgradeneeded = function(event) {
        var db = event.target.result;
        var insuranceStore = db.createObjectStore('insurance', { 
            keyPath: 'id', autoIncrement: true,
        }); 
        
        var settlementStore = db.createObjectStore('settlement', { keyPath: 'id', autoIncrement: true }); 
    };

    request.oncomplete = function(event) {
        event.target.result.close();
        console.log('Database opened successfully');
    };

    // Handle database opening error
    request.onerror = function(event) {
        console.error('Error opening database:', event.target.error);
    };

    return request;
}

