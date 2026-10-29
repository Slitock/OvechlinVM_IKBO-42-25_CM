#!/usr/bin/env bash

echo "=== Запуск с минимальной VFS ==="
./run.sh --vfs vfs_min.zip --script script.txt
echo -e "\n----------------------------------\n"

echo "=== Запуск с глубокой VFS ==="
./run.sh --vfs vfs_deep.zip --script script.txt
echo -e "\n----------------------------------\n"

echo "=== Запуск с основной VFS ==="
./run.sh --vfs vfs.zip --script script.txt
