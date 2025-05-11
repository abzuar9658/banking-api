#! /bin/bash

set -o errexit
set -o pipefail
set -o nounset

python << END
import sys
import time
import psycopg2

suggest_unrecoverable_after=30
start=time.time()

while True:
    try:
        psycopg2.connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Database connection failed, retrying in 0.5s\n")
        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write("Database connection failed after {} seconds\n".format(suggest_unrecoverable_after))
            sys.stderr.write(error)
            time.sleep(0.5)
        
END

echo >&2 'PostgreSQL is available'

exec "$@"