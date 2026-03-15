---
name: databases
description: "Design schemas, write queries for MongoDB and PostgreSQL. Use for database design, SQL/NoSQL queries, aggregation pipelines, indexes, migrations, replication, performance optimization, psql CLI."
argument-hint: "[query or schema task]"
license: MIT
---

# Databases Skill

Unified guide for working with MongoDB (document-oriented) and PostgreSQL (relational) databases. Choose the right database for your use case and master both systems.

## When to Use This Skill

Use when:

- Designing database schemas and data models
- Writing queries (SQL or MongoDB query language)
- Building aggregation pipelines or complex joins
- Optimizing indexes and query performance
- Implementing database migrations
- Setting up replication, sharding, or clustering
- Configuring backups and disaster recovery
- Managing database users and permissions
- Analyzing slow queries and performance issues
- Administering production database deployments

## Reference Navigation

### Database Design

- **db-design** — Activate when user requests: Database/table design for transactional (OLTP), analytics (OLAP), create or extend schema, design fact/dimension tables, analyze/review CSV/JSON/SQL files to create tables, or need advice on data storage structure.

### MongoDB References

- **mongodb-crud** — CRUD operations, query operators, atomic updates
- **mongodb-aggregation** — Aggregation pipeline, stages, operators, patterns
- **mongodb-indexing** — Index types, compound indexes, performance optimization
- **mongodb-atlas** — Atlas cloud setup, clusters, monitoring, search

### PostgreSQL References

- **postgresql-queries** — SELECT, JOINs, subqueries, CTEs, window functions
- **postgresql-psql-cli** — psql commands, meta-commands, scripting
- **postgresql-performance** — EXPLAIN, query optimization, vacuum, indexes
- **postgresql-administration** — User management, backups, replication, maintenance

## CLI Administration

Use `psql` CLI for PostgreSQL administration and `mongosh` for MongoDB.

```bash
# PostgreSQL — connect and run query
psql -U postgres -d mydb -c "SELECT * FROM users LIMIT 5;"

# PostgreSQL — run migration file
psql -U postgres -d mydb -f migration.sql

# PostgreSQL — dump and restore
pg_dump -U postgres mydb > backup.sql
psql -U postgres mydb < backup.sql

# MongoDB — connect shell
mongosh "mongodb://localhost:27017/mydb"

# MongoDB — export/import
mongodump --db mydb --out /backups/
mongorestore --db mydb /backups/mydb/
```

## Best Practices

**MongoDB:**

- Use embedded documents for 1-to-few relationships
- Reference documents for 1-to-many or many-to-many
- Index frequently queried fields
- Use aggregation pipeline for complex transformations
- Enable authentication and TLS in production
- Use Atlas for managed hosting

**PostgreSQL:**

- Normalize schema to 3NF, denormalize for performance
- Use foreign keys for referential integrity
- Index foreign keys and frequently filtered columns
- Use EXPLAIN ANALYZE to optimize queries
- Regular VACUUM and ANALYZE maintenance
- Connection pooling (pgBouncer) for web apps

## Resources

- MongoDB: https://www.mongodb.com/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- MongoDB University: https://learn.mongodb.com/
- PostgreSQL Tutorial: https://www.postgresqltutorial.com/
