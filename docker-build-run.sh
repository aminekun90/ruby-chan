docker build --tag ruby-chan .
docker run ruby-chan -v ${pwd}/server:/ruby-chan/server