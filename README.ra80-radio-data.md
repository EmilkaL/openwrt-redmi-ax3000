# Experimental RA80 radio data

This branch removes the overlapping IPQ5018 firmware package and extracts both per-device ART calibration blocks. The composite IPQ5018/QCN6122 firmware does not include Xiaomi RA80 board data, so a local image also needs the two native BDF files. The following preparation is a candidate for testing; firmware compilation and 5 GHz AP operation on RA80 have not been verified.

Use only Xiaomi AX3000 RA80, with stock boot arguments selecting `cnss2.bdf_integrated=0x24` and `cnss2.bdf_pci0=0x60`. Confirm those values on the actual device before installing an image. This procedure does not establish support for RA80V2 or any AX3000T variant.

## Prepare local board data

Obtain [Xiaomi's RA80 1.0.46 image](https://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/ra80/miwifi_ra80_firmware_e7f84_1.0.46.bin), whose SHA256 is `d958712412e1948a34fbe33e587f74789ec39fe626e77c60cc257796f20df043`, and extract its root filesystem as data. Do not execute its programs or flash this stock image as part of the preparation.

The input directory must be `lib/firmware/IPQ5018/WIFI_FW` from that filesystem, containing `bdwlan.b24` and `qcn6122/bdwlan.b60`. The generator validates the exact payload hashes and both checksums before creating any output. From the OpenWrt source directory, with no existing `files` directory, run:

```sh
python3 scripts/ra80-board-data.py \
  --stock-directory /path/to/extracted/lib/firmware/IPQ5018/WIFI_FW \
  --output-directory files
```

The generated rootfs overlay contains:

```text
files/lib/firmware/ath11k/IPQ5018/hw1.0/board.bin
files/lib/firmware/ath11k/QCN6122/hw1.0/board.bin
```

Keep these vendor blobs local; this repository does not distribute them. If an overlay already exists, generate into a new directory and review how its two files should be added without replacing existing data. Build only the `xiaomi_ax3000` profile with this device-specific overlay.

## Scope and validation

Each 128 KiB payload changes only the compatibility byte at `0x45c` from `03` to `00` and the checksum byte at `0x0a`. All other bytes, including RF power and frequency tables, remain identical to Xiaomi's stock data. The resulting 16-bit little-endian XOR checksum is `0xffff`; the script verifies the complete output hashes.

[A first-hand QCN6102/QCN6122 report](https://memo205.hatenablog.jp/entry/2025/02/15/074907) documents this compatibility-byte change resolving a BDF probe crash with `WLAN.HK.2.7.0.1-01744-QCAHKSWPL_SILICONZ-1`. This is evidence for a candidate, not proof that it resolves RA80's missing AP beacons. The meaning of this byte has not been established from an official format specification.

The current [ath11k driver](https://github.com/gregkh/linux/blob/v6.18.7/drivers/net/wireless/ath/ath11k/core.c#L1739) supports raw `board.bin` as its API 1 fallback after API 2 board-data searches fail. The composite package supplies neither `board-2.bin` nor `board.bin` for these two radios, so this method does not invent QMI matching IDs. Before deployment, inspect the assembled root filesystem for any additional `board-2.bin` that could take priority over the candidate files.

The ART calibration remains specific to each router and is read by firmware hotplug from `0:ART` at `0x1000` and `0x26800`, with length `0x20000` each. Do not copy calibration or ART from another device.

Before flashing, verify the hardware revision, MTD layout, active boot slot, per-unit backup and recovery access. After a controlled boot, verify both radios probe without crashes, that the 5 GHz AP transmits beacons, and that a client can associate and transfer traffic; also check memory use with both radios enabled.
