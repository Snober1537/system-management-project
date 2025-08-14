const express = require('express');
const router = express.Router();
const { query } = require('../utils/db');
const logger = require('../utils/logger');

// Validation middleware
const validateItemData = (req, res, next) => {
    const { name, quantity } = req.body;
    
    if (!name || typeof name !== 'string' || !name.trim()) {
        return res.status(400).json({ error: 'Name is required and must be a non-empty string' });
    }
    
    if (typeof quantity !== 'number' || quantity <= 0) {
        return res.status(400).json({ error: 'Quantity must be a positive number' });
    }
    
    next();
};

const validateId = (req, res, next) => {
    const id = req.params.id;
    
    if (!id || isNaN(id) || parseInt(id) <= 0) {
        return res.status(400).json({ error: 'Invalid ID format' });
    }
    
    req.params.id = parseInt(id);
    next();
};

// Routes
router.get('/', async (req, res) => {
    try {
        const items = await query('SELECT * FROM inventory');
        logger.info('Items retrieved successfully');
        res.json(items);
    } catch (error) {
        logger.error('Error fetching items:', error);
        res.status(500).json({ error: 'Failed to fetch items' });
    }
});

router.post('/', validateItemData, async (req, res) => {
    try {
        const { name, quantity, description } = req.body;
        await query(
            'INSERT INTO inventory (name, quantity, description) VALUES (?, ?, ?)',
            [name, quantity, description || '']
        );
        logger.info(`Item added: ${name}`);
        res.status(201).json({ message: 'Item added successfully' });
    } catch (error) {
        logger.error('Error adding item:', error);
        res.status(500).json({ error: 'Failed to add item' });
    }
});

router.get('/:id', validateId, async (req, res) => {
    try {
        const item = await query(
            'SELECT * FROM inventory WHERE id = ?',
            [req.params.id]
        );
        
        if (!item.length) {
            return res.status(404).json({ error: 'Item not found' });
        }
        
        logger.info(`Item retrieved: ${req.params.id}`);
        res.json(item[0]);
    } catch (error) {
        logger.error('Error fetching item:', error);
        res.status(500).json({ error: 'Failed to fetch item' });
    }
});

router.put('/:id', [validateId, validateItemData], async (req, res) => {
    try {
        const { name, quantity, description } = req.body;
        const affectedRows = await query(
            'UPDATE inventory SET name = ?, quantity = ?, description = ? WHERE id = ?',
            [name, quantity, description || '', req.params.id]
        );
        
        if (affectedRows.affectedRows === 0) {
            return res.status(404).json({ error: 'Item not found' });
        }
        
        logger.info(`Item updated: ${req.params.id}`);
        res.json({ message: 'Item updated successfully' });
    } catch (error) {
        logger.error('Error updating item:', error);
        res.status(500).json({ error: 'Failed to update item' });
    }
});

router.delete('/:id', validateId, async (req, res) => {
    try {
        const affectedRows = await query(
            'DELETE FROM inventory WHERE id = ?',
            [req.params.id]
        );
        
        if (affectedRows.affectedRows === 0) {
            return res.status(404).json({ error: 'Item not found' });
        }
        
        logger.info(`Item deleted: ${req.params.id}`);
        res.json({ message: 'Item deleted successfully' });
    } catch (error) {
        logger.error('Error deleting item:', error);
        res.status(500).json({ error: 'Failed to delete item' });
    }
});

module.exports = router;
