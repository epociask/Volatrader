// Require taapi
const taapi = require("taapi");

// Setup server with authentication
const secret = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtcG9jaWFza0Bkb25zLnVzZmNhLmVkdSIsImlhdCI6MTU4MzMxNzYwNSwiZXhwIjo3ODkwNTE3NjA1fQ.hfTvshR4HJuCSJ4XJNEgb_xkWIuW0ixZXm7OthcwUFk"
const server = taapi.server(secret);

// Define port - Optional and defaults to 4101
// server.setServerPort(3000);

// Start the server
server.start();