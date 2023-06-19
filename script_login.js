const csvData = `Username,Password
john,password123
jane,letmein
alice,secret`;

const jsonData = Papa.parse(csvData, { header: true }).data;

function login(username, password) {
  const match = jsonData.find(entry => entry.Username === username && entry.Password === password);
  return Boolean(match);
}

// Example usage
const username = 'john';
const password = 'password123';

if (login(username, password)) {
  console.log('Login successful');
} else {
  console.log('Login failed');
}
