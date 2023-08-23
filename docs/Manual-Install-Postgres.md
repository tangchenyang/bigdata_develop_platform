# Pull Postgres Image
```shell
docker pull postgres
```

# Start 
```shell
docker run --name pg -d -p 5432:5432 -e POSTGRES_PASSWORD=123456 postgres
```

# Enter 
```shell
docker exec -it mypostgres /bin/bash
```

# Connect DB
```shell
psql -U postgres -h localhost -d postgres
```

# Test Query
```sql
select * from pg_tables
```
