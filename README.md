# dan
`dan` is my personal tool to quickly create and enter dev containers. 

It supports running X11 and Wayland apps with audio and gpu access. 

This is compatible with Fedora and uses Podman under the hood. 

## Important information

By default, `dan` tries to use the `base` image which has these requirements
- The user in the container has name `user` (for volumes)
- The user has UID and GID of 1000 (for graphics)
- Has the `render` group (for gpu access)
- `alsa-utils`, `pipewire` and `pipewire-alsa` are installed (for audio)

An example using Debian is provided. Feel free to customise the script and the image provided.

Special thanks to [the x11docker wiki](https://github.com/mviereck/x11docker/wiki)!

## Note on X11

If `--X11` is enabled, run the folowing to allow connections
```bash
xhost +SI:localuser:$USER
```

