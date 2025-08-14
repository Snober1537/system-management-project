const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Mock database connection for tests
jest.mock('../src/utils/db', () => ({
    query: jest.fn()
}));
