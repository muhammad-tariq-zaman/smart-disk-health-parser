# smart-disk-health-parser

Parse saved `smartctl -a` output and summarise it: model, serial,
overall-health result, reallocated and pending sectors, power-on hours
and temperature, with a simple OK / WARNING / FAIL verdict.

## How to run

```bash
smartctl -a /dev/sda > smart.txt
python3 main.py smart.txt
```

## Example output

```text
model: TESTDISK 1000
serial: SN123
health: PASSED
reallocated_sectors: 0
pending_sectors: 0
power_on_hours: 1234
temperature_celsius: 34
verdict: OK
```

Standard library only. It parses a file you supply; it does not run
smartctl itself.
