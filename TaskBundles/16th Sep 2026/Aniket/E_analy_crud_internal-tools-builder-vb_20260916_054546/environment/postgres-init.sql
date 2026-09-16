CREATE ROLE deku_app WITH LOGIN PASSWORD 'girder-local-dev-71c4';

GRANT CONNECT ON DATABASE deku TO deku_app;
GRANT ALL PRIVILEGES ON SCHEMA public TO deku_app;

ALTER SCHEMA public OWNER TO deku_app;
