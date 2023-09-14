touch .env

echo "building lago-api..."
docker-compose build
echo "building lago-api done!" 
echo "running docker-compose up.."
docker-compose up -d
