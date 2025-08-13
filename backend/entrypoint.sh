#!/bin/sh

set -e

echo "Aguardando o banco de dados iniciar..."
sleep 5

echo "Aplicando migrações do banco de dados..."
alembic upgrade head
echo "Migrações aplicadas com sucesso."

exec "$@"