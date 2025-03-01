#!/usr/bin/python3

from dan import get_parser, process_args
import unittest


def to_cmd(inp: str) -> str:
    parser = get_parser()
    args = parser.parse_args(inp.split())
    return process_args(args)


class TestCreate(unittest.TestCase):
    def test_empty(self):
        cmd = to_cmd("create test")
        self.assertNotIn("--userns", cmd)
        self.assertNotIn("-v", cmd)
        self.assertNotIn("-p", cmd)
        self.assertNotIn("--device", cmd)

    def test_deduped(self):
        cmd = to_cmd("create -x -w -g -a test")
        count = cmd.count("--security-opt label=type:container_runtime_t")
        self.assertEqual(count, 1)

    def test_missing_name(self):
        with self.assertRaises(SystemExit):
            to_cmd("create")

    def test_default_volume(self):
        cmd = to_cmd("create test -v")
        self.assertIn("-v test:/home/user/data", cmd)

    def test_specified_volume(self):
        cmd = to_cmd("create test -v vol")
        self.assertIn("-v vol:/home/user/data", cmd)

    def test_missing_ports(self):
        with self.assertRaises(SystemExit):
            to_cmd("create test -i")

    def test_ports(self):
        ports = [1, 2, 3, 4]
        cmd = to_cmd(f"create test -p {','.join(map(str, ports))}")

        for p in ports:
            self.assertIn(f"-p 127.0.0.1:{p}:{p}", cmd)

    def test_invalid_ports(self):
        with self.assertRaises(SystemExit):
            to_cmd("create -p not_some_numbers")

    def test_missing_image(self):
        with self.assertRaises(SystemExit):
            to_cmd("create test -i")


if __name__ == "__main__":
    unittest.main()
