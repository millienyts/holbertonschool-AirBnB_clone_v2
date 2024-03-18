-- Initialize MySQL for HBNB Clone Project Testing Environment
-- This script performs the following actions:
--   * Establishes a test database named `hbnb_clone_test`.
--   * Sets up a dedicated test user `test_user` with a specified password for accessing the test database.
--   * Ensures `test_user` has comprehensive privileges over the `hbnb_clone_test` database for full testing capabilities.
--   * Allows `test_user` to execute SELECT queries on `performance_schema` for database performance insights.

-- Step 1: Create the test database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS hbnb_clone_test;

-- Step 2: Create a test user with a specific password for localhost access
CREATE USER
    IF NOT EXISTS 'test_user'@'localhost'
    IDENTIFIED BY 'secure_test_pwd';

-- Step 3: Grant full privileges to the test user on the test database
-- This enables the user to perform all CRUD operations necessary for thorough testing
GRANT ALL PRIVILEGES
   ON `hbnb_clone_test`.*
   TO 'test_user'@'localhost';

-- Step 4: Grant the test user permission to access `performance_schema`
-- Access to performance metrics can aid in identifying potential bottlenecks
GRANT SELECT
   ON `performance_schema`.*
   TO 'test_user'@'localhost';

-- Step 5: Apply all the privilege changes
FLUSH PRIVILEGES;

