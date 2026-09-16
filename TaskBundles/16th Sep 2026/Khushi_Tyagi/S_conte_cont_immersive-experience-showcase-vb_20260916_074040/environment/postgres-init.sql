CREATE ROLE deku_app WITH LOGIN PASSWORD 'deku-local-dev';
GRANT ALL PRIVILEGES ON DATABASE deku TO deku_app;
GRANT ALL ON SCHEMA public TO deku_app;
ALTER SCHEMA public OWNER TO deku_app;
