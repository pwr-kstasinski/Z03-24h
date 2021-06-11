docker ps -a -q | %{
    Write-Host "Removing:" $_ -BackgroundColor Yellow -ForegroundColor Black
    docker stop $_
    docker rm $_
}
docker image rm my-server 

docker build -t my-server . 

docker-compose up db --detach 

Start-Sleep -Seconds 5

docker-compose up adminer --detach 
docker-compose up server --detach