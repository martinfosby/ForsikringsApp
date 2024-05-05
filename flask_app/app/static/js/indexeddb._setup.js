// Open a connection to the IndexedDB database
const requestSetup = indexedDB.open('bodovision', 1);

// Define the database schema and object stores
requestSetup.onupgradeneeded = function(event) {
    var db = event.target.result;
    var insuranceStore = db.createObjectStore('insurance', { 
        keyPath: 'id', autoIncrement: true,
    }); 
    
    var settlementStore = db.createObjectStore('settlement', { keyPath: 'id', autoIncrement: true }); 
};

requestSetup.oncomplete = function(event) {
    event.target.result.close();
    console.log('Database opened successfully');
};

// Handle database opening error
requestSetup.onerror = function(event) {
    console.error('Error opening database:', event.target.error);
};