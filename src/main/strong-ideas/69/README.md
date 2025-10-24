# How to run?

```shell
sudo apt-get update
sudo apt-get install nasm build-essential
nasm -felf64 source.asm -o app.o
gcc app.o -o app
gcc -no-pie app.o -o app
./app
```