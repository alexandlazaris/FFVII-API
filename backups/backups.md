# Creating & restoring backups

## 1. Start app

Run the service using `docker compose up -d`

## 2. Backup data

Back up the db, exclude a table and store into local backup dir. Swap out `POSTGRES_USER` for the db username.

```
docker compose exec -T postgres pg_dump \
  -U POSTGRES_USER \
  -d ffvii \
  --data-only \
  --exclude-table-data=public.alembic_version \
  -Fc > "backups/ffvii_$(date +%Y%m%d_%H%M%S).dump"
```

## 3. Stop & rebuild whole service

Start with a clean slate.

```
docker compose down -v
docker compose up -d --build
```

## 4. Load backup

> [!WARNING]
> Restoring data snapshots on a pre-existing db can introduce data corruption, or negatively impact future db migrations. If all goes to hell, wipe the db volume using `docker volume rm ffvii-api_postgres_data` and resume from step 3 above.

Now you can populate your rebuilt db with the data snapshot taken back in step 2.

```
docker compose exec -T postgres pg_restore \
  -U POSTGRES_USER \
  -d ffvii \
  --data-only \
  --no-owner \
  < backups/ffvii_$(date +%Y%m%d_%H%M%S).dump
```

