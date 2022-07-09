docker build --tag ruby-chan .
docker run -it -v "$(pwd)"/server:/ruby-chan/server ruby-chan