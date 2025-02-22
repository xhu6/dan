# dan
`dan` is my personal tool to quickly create and enter dev containers.

This is compatible with Fedora and uses Podman under the hood.

By default, `dan` tries to use the `base` image.

Requirements for `base` image
- The user in the container has name `user`
- The user has UID and GID of 1000
- Has render group

An example using debian is provided. Feel free to customise the script and the image to your liking.

If `--X11` is enabled, run the folowing to allow connections
```bash
xhost +SI:localuser:$USER
```

Special thanks to [the x11docker wiki](https://github.com/mviereck/x11docker/wiki)!
