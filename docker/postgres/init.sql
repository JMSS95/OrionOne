-- OrionOne - PostgreSQL Initialization Script

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For full-text search

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE orionone TO laravel;

-- Log
SELECT 'OrionOne database initialized successfully!' AS status;
