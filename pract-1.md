# Задача 1 

через команду greep ищем файл по шаблону _-v '^#'_ который говорит, все строки кроме тех, которые начинаются с _#_
команда cut режет текст в файле passwd на блоки разделяя их по знакам :, -f1 вытаскивает только первые столбцы.
команда sort сортирует)
```
slitock@fedora:/$ grep -v '^#' /etc/passwd | cut -d: -f1 | sort
abrt
adm
avahi
bin
chrony
clevis
colord
cosmic-greeter
daemon
dbus
dnsmasq
flatpak
ftp
games
geoclue
greetd
halt
lp
mail
newuser
nobody
ollama
operator
passim
pipewire
polkitd
root
rpc
rpcuser
rtkit
setroubleshoot
shutdown
slitock
sshd
sssd
sync
systemd-coredump
systemd-network
systemd-oom
systemd-resolve
systemd-timesync
tcpdump
tss
unbound
usbmuxd
vboxadd
wsdd
```

