// Open a connection to the IndexedDB database
const request = indexedDB.open('bodovision', 1);

// Define the database schema and object stores
request.onupgradeneeded = function(event) {
    var db = event.target.result;
    var insuranceStore = db.createObjectStore('insurance', { 
        keyPath: 'id', autoIncrement: true,
    }); 
    
    var settlementStore = db.createObjectStore('settlement', { keyPath: 'id', autoIncrement: true }); 
};


// Handle database opening error
request.onerror = function(event) {
    console.error('Error opening database:', event.target.error);
};

