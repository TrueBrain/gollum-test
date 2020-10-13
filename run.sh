if [ ! -e data ]; then
    mkdir -p data
    (
        cd data
        git init
    )
fi

docker run --rm --name gollum -v `pwd`/data:/wiki openttd-gollum &
sleep 1
docker run --rm --link gollum --volumes-from gollum:ro -p 127.0.0.1:5000:80 openttd-gollum-nginx
