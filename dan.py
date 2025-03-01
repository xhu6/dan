#!/usr/bin/python3

from argparse import ArgumentParser, Namespace
import subprocess

"""
Highly recommend reading the wiki:
- https://github.com/mviereck/x11docker/wiki
"""

OPTS = [
    ["-x", "--x11", "add X11 from host"],
    ["-w", "--wayland", "add Wayland from host"],
    ["-g", "--gpu", "enable GPU"],
    ["-a", "--audio", "enable audio via Pipewire"],
]


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="create a container")

    for opt, full_opt, desc in OPTS:
        create_parser.add_argument(opt, full_opt, help=desc, action="store_true")

    create_parser.add_argument("-p", "--ports", help="publish ports to localhost")
    create_parser.add_argument(
        "-v", "--volume", help="mount volume", nargs="?", const=""
    )
    create_parser.add_argument("-i", "--image", help="specify image", nargs=1)
    create_parser.add_argument("name", help="container name")

    enter_parser = subparsers.add_parser("enter", help="enter a container")
    enter_parser.add_argument("name", help="container name")

    return parser


def get_args() -> Namespace:
    return get_parser().parse_args()


def deduplicate(extra_args: str) -> str:
    unique_args = {arg.strip() for arg in extra_args.splitlines()}
    return " ".join(unique_args)


def process_create(args: Namespace) -> str:
    assert args.command == "create"

    extra_args = ""

    if args.x11:
        extra_args += """
            --security-opt label=type:container_runtime_t
            --userns keep-id:uid=1000,gid=1000
            -v /tmp/.X11-unix:/tmp/.X11-unix:ro
            -e DISPLAY
        """

    if args.wayland:
        extra_args += """
            --security-opt label=type:container_runtime_t
            --userns keep-id:uid=1000,gid=1000
            -e WAYLAND_DISPLAY
            -v "${XDG_RUNTIME_DIR}/${WAYLAND_DISPLAY}:/tmp/${WAYLAND_DISPLAY}:ro"
        """

    if args.gpu:
        extra_args += """
            --security-opt label=type:container_runtime_t
            --group-add video
            --group-add render
            --device /dev/dri
        """

    if args.audio:
        extra_args += """
            --security-opt label=type:container_runtime_t
            -v ${XDG_RUNTIME_DIR}/pipewire-0:/tmp/pipewire-0:ro
        """

    if args.ports:
        try:
            ports = list(map(int, args.ports.split(",")))
        except:
            print("dan: error: ports should be comma seperated integers")
            exit(1)

        extra_args += " ".join(f"-p localhost:{port}:{port}" for port in ports)

    if args.volume is not None:
        volume_name = args.volume or args.name
        extra_args += f"-v {volume_name}:/home/user/data"

    image_name = args.image or "base"
    extra_args = deduplicate(extra_args)

    command = f"""
        podman run -itd --stop-timeout=1
        --name {args.name}
        -e XDG_RUNTIME_DIR=/tmp
        {extra_args}
        {image_name} bash
    """

    # Removes duplicate whitespace
    return " ".join(command.split())


def process_enter(args: Namespace) -> str:
    assert args.command == "enter"

    return f"podman exec -it {args.name} bash"


def process_args(args: Namespace) -> str:
    match args.command:
        case "create":
            return process_create(args)
        case "enter":
            return process_enter(args)

    # This should be unreachable
    print(args)
    exit(1)


if __name__ == "__main__":
    args = get_args()
    command = process_args(args)

    print()
    print(command)
    print()

    if args.command == "create":
        if input("Continue? [y/N]").lower() != "y":
            print("Aborted.")
            exit()

    # Probably insecure but allows using environment vars
    subprocess.run(command, shell=True)
