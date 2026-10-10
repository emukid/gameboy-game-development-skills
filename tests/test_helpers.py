"""Behavioral tests for asset conversion and malformed ROM rejection."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


tiles = module('tiles', 'skills/gameboy-build/scripts/tiles.py')
rom = module('rom', 'skills/gameboy-verify/scripts/check_rom.py')


def fix_checksums(data):
    data[0x14D] = (-sum(data[0x134:0x14D]) - 25) & 0xFF
    data[0x14E:0x150] = b'\0\0'
    data[0x14E:0x150] = (sum(data) & 0xFFFF).to_bytes(2, 'big')
    return data


def fixture():
    data = bytearray(32768)
    data[0x104:0x134] = rom.LOGO
    return fix_checksums(data)


class TilesTests(unittest.TestCase):
    def test_bitplanes_and_pixel_order(self):
        self.assertEqual(tiles.encode(('01230123\n' * 8)), bytes([0x55, 0x33] * 8))

    def test_tile_order(self):
        data = tiles.encode(('0000000011111111\n' * 8) + ('2222222233333333\n' * 8))
        self.assertEqual(data, bytes([0, 0] * 8 + [255, 0] * 8 + [0, 255] * 8 + [255, 255] * 8))

    def test_reject_bad_input(self):
        for text in ('', '0' * 7 + '\n', '44444444\n' * 8, '00000000\n' * 7 + '0\n'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                tiles.encode(text)

    def test_cli_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output = Path(folder) / 'art.txt', Path(folder) / 'art.c'
            source.write_text('01230123\n' * 8)
            cmd = [sys.executable, str(ROOT / 'skills/gameboy-build/scripts/tiles.py'), str(source), str(output), '--symbol', 'hero']
            first = subprocess.run(cmd, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = output.read_bytes()
            self.assertIn(b'const uint8_t hero[16]', original)
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual(output.read_bytes(), original)


class RomTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(rom.inspect(fixture())['errors'], [])

    def test_truncated(self):
        self.assertTrue(rom.inspect(b'bad')['errors'])
        self.assertTrue(rom.inspect(fixture()[:-1])['errors'])

    def test_corrupt_logo_and_checksums(self):
        for address, message in ((0x104, 'logo'), (0x134, 'header checksum'), (0x200, 'global checksum')):
            data = fixture()
            data[address] ^= 1
            self.assertTrue(any(message in e for e in rom.inspect(data)['errors']))

    def test_mapper_ram_mismatch(self):
        data = fixture()
        data[0x149] = 2
        self.assertTrue(rom.inspect(fix_checksums(data))['errors'])

    def test_mbc5_and_mbc2(self):
        data = fixture()
        data[0x147], data[0x149] = 0x1B, 3
        self.assertEqual(rom.inspect(fix_checksums(data))['errors'], [])
        data[0x147], data[0x149] = 6, 0
        self.assertEqual(rom.inspect(fix_checksums(data))['errors'], [])

    def test_mapper_capacity_and_unknown(self):
        data = fixture() + bytearray(32768)
        data[0x148] = 1
        self.assertTrue(any('capacity' in e for e in rom.inspect(fix_checksums(data))['errors']))
        data[0x147] = 0xFC
        self.assertTrue(any('unsupported' in e for e in rom.inspect(fix_checksums(data))['errors']))


class ScaffoldTests(unittest.TestCase):
    def test_create_then_refuse_existing(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'new game'
            cmd = [sys.executable, str(ROOT / 'skills/gameboy-build/scripts/new_project.py'), str(destination)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            source = destination / 'src/main.c'
            self.assertTrue(source.exists())
            source.write_text('user change')
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual(source.read_text(), 'user change')


if __name__ == '__main__':
    unittest.main()
