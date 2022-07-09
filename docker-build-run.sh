docker build --tag ruby-chan .
docker run ruby-chan -v ${PWD}/server:/ruby-chan/server