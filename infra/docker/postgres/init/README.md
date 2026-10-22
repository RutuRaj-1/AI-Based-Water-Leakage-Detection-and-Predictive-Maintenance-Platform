# PostgreSQL init scripts

Place `.sql` or `.sh` scripts here to run automatically when the PostgreSQL
container starts for the first time.

Example use cases:
- Enable the PostGIS extension
- Create additional schemas
- Insert minimal seed data

Files are executed in alphabetical order.

## Example: enable-postgis.sql

```sql
-- Uncomment and place in a .sql file here to auto-enable PostGIS
-- CREATE EXTENSION IF NOT EXISTS postgis;
-- CREATE EXTENSION IF NOT EXISTS postgis_topology;
```
