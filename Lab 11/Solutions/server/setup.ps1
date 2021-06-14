docker ps -a -q | %{
    Write-Host "Removing:" $_ -BackgroundColor Yellow -ForegroundColor Black
    docker stop $_
    docker rm $_
}
docker image rm my-server 

docker build -t my-server . 

docker-compose up --detach
# docker-compose up --detach  db 

# Start-Sleep -Seconds 10

# docker-compose up --detach adminer
# docker-compose up --detach server

cd ../client

npm start