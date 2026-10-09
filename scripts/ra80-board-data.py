import argparse
import functools
import hashlib
import json
import operator
import struct
from pathlib import Path


BOARD_BYTES = 131072
COMPATIBILITY_OFFSET = 0x45C
CHECKSUM_OFFSET = 0x0A
RADIOS = (
    (
        "bdwlan.b24",
        "IPQ5018/hw1.0",
        "078ed74c85aa62dc3dfbc189dbe40249589cd7df7542cc7978fa44c5eb794869",
        "e005e8f46695ac131527c8e2450a8e5cf9b8d36788fdc6cd940b7b07942fcd5a",
    ),
    (
        "qcn6122/bdwlan.b60",
        "QCN6122/hw1.0",
        "085e7e1db01031cee45b5170e6bdc3dc7d19ccefc00aefeeae77f2ee52aa3a7d",
        "5f9fbedeba1d63fa2baa66685fa91f771abc7204f894ddc9129f3343f2b0e29e",
    ),
)


def board_checksum(data):
    return functools.reduce(operator.xor, struct.unpack("<65536H", data), 0)


def prepare_radio(stock_directory, radio):
    source_name, firmware_directory, source_hash, result_hash = radio
    source_path = stock_directory / source_name
    with source_path.open("rb") as source_file:
        original = source_file.read(BOARD_BYTES + 1)
    if len(original) != BOARD_BYTES or hashlib.sha256(original).hexdigest() != source_hash:
        raise ValueError(f"{source_name} is not the expected Xiaomi RA80 1.0.46 board data.")
    if board_checksum(original) != 0xFFFF or original[COMPATIBILITY_OFFSET] != 3:
        raise ValueError(f"{source_name} has an unexpected checksum or compatibility byte.")
    adjusted = bytearray(original)
    adjusted[COMPATIBILITY_OFFSET] = 0
    struct.pack_into("<H", adjusted, CHECKSUM_OFFSET, 0)
    struct.pack_into("<H", adjusted, CHECKSUM_OFFSET, board_checksum(adjusted) ^ 0xFFFF)
    if board_checksum(adjusted) != 0xFFFF or hashlib.sha256(adjusted).hexdigest() != result_hash:
        raise ValueError(f"{source_name} did not produce the expected candidate data.")
    changed_offsets = [offset for offset, pair in enumerate(zip(original, adjusted)) if pair[0] != pair[1]]
    if changed_offsets != [CHECKSUM_OFFSET, COMPATIBILITY_OFFSET]:
        raise ValueError(f"{source_name} changed data outside the two permitted bytes.")
    return firmware_directory, adjusted, {
        "source": source_name,
        "source_sha256": source_hash,
        "candidate_sha256": result_hash,
        "changed_offsets": [hex(offset) for offset in changed_offsets],
        "bytes": len(adjusted),
    }


def main():
    parser = argparse.ArgumentParser(description="Prepare experimental RA80 board.bin files from Xiaomi stock board data.")
    parser.add_argument("--stock-directory", required=True, type=Path)
    parser.add_argument("--output-directory", required=True, type=Path, help="New rootfs overlay directory; existing directories are refused.")
    arguments = parser.parse_args()
    try:
        if arguments.output_directory.exists():
            raise ValueError("The output directory already exists and will not be overwritten.")
        prepared = [prepare_radio(arguments.stock_directory, radio) for radio in RADIOS]
        arguments.output_directory.mkdir(parents=True, exist_ok=False)
        report = []
        for firmware_directory, adjusted, metadata in prepared:
            output = arguments.output_directory / "lib/firmware/ath11k" / firmware_directory / "board.bin"
            output.parent.mkdir(parents=True, exist_ok=False)
            with output.open("xb") as output_file:
                output_file.write(adjusted)
            metadata["output"] = str(output.resolve())
            report.append(metadata)
        print(json.dumps({"status": "experimental_not_hardware_verified", "radios": report}, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
