CREATE ROLE deku_app WITH LOGIN PASSWORD 'deku-local-dev';
GRANT ALL PRIVILEGES ON DATABASE lumina TO deku_app;
GRANT ALL ON SCHEMA public TO deku_app;
