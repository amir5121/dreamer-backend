psql -U postgres -c "CREATE USER $XE_CURRENCY_DB_USER PASSWORD '$XE_CURRENCY_DB_PASS'"
psql -U postgres -c "CREATE DATABASE $XE_CURRENCY_DB_NAME OWNER $XE_CURRENCY_DB_USER"
