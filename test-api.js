const axios = require('axios');
const logger = require('./src/utils/logger');

const API_URL = 'http://localhost:3000/api';

async function testEndpoints() {
    try {
        // Test health check endpoint
        logger.info('Testing health check endpoint...');
        const healthCheck = await axios.get('http://localhost:3000/');
        console.log('Health check:', healthCheck.data);

        // Test GET all items
        logger.info('Testing GET all items...');
        const items = await axios.get(`${API_URL}/items`);
        console.log('Items:', items.data);

        // Add a test item
        logger.info('Testing POST item...');
        const newItem = await axios.post(`${API_URL}/items`, {
            name: 'Test Item',
            quantity: 10,
            description: 'This is a test item'
        });
        console.log('Created item:', newItem.data);

        // Get the created item
        logger.info('Testing GET specific item...');
        const itemId = newItem.data.id;
        const item = await axios.get(`${API_URL}/items/${itemId}`);
        console.log('Retrieved item:', item.data);

        // Update the item
        logger.info('Testing PUT item...');
        const updatedItem = await axios.put(`${API_URL}/items/${itemId}`, {
            name: 'Updated Test Item',
            quantity: 20,
            description: 'This is an updated test item'
        });
        console.log('Updated item:', updatedItem.data);

        // Delete the item
        logger.info('Testing DELETE item...');
        await axios.delete(`${API_URL}/items/${itemId}`);
        console.log('Item deleted successfully');

        logger.info('All API tests completed successfully!');
    } catch (error) {
        logger.error('API test failed:', error.response?.data || error.message);
        throw error;
    }
}

testEndpoints().catch(error => {
    logger.error('Error in API tests:', error);
    process.exit(1);
});
