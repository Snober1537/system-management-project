const mysql = require('mysql2/promise');
const logger = require('./logger');

const dbConfig = {
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'inventory_db',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
};

let pool;

const getPool = async () => {
    if (!pool) {
        try {
            pool = mysql.createPool(dbConfig);
            logger.info('Database connection pool created successfully');
        } catch (error) {
            logger.error('Error creating database connection pool:', error);
            throw error;
        }
    }
    return pool;
};

const query = async (sql, params = []) => {
    try {
        const connection = await getPool();
        const [rows] = await connection.query(sql, params);
        return rows;
    } catch (error) {
        logger.error('Database query error:', error);
        throw error;
    }
};

module.exports = {
    query,
    getPool
};
