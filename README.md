# The Passport of Mara Ilsen — Republic of Velloria

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/giandisruw/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/giandisruw/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

Built for the [make.fun](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318) bounty `the-passport-page-of-a-countr-2-20261121-0318` ("The Passport Page of a Country That Isn't There").

An open passport spread for a country that does not exist: the
Republic of Velloria, a lighthouse island republic in the Meridian
Sea, drawn by a Python program. The left page is the data page of
Mara Elena Ilsen, a lighthouse keeper from Port Liora; the right page
is her visa page, stamped with one voyage.

## The country

Velloria is an archipelago whose whole identity is light and sea:
its flag is navy, teal and white with a gold lighthouse, its coat of
arms carries a lighthouse over waves under a star, and its passports
are issued in Vellorian, English and French. The capital and only
passport office is Port Liora, on Meridian Quay.

## The holder

Mara Elena Ilsen, born 14 March 1988 at Port Liora General Hospital,
holds passport No. VL 4829176, issued 02 June 2025 at Port Liora and
valid until 01 June 2035. Her occupation is printed on the data page
— lighthouse keeper — and it is the thread that ties the whole spread
together: the portrait shows her in a keeper's uniform with gold
epaulettes, and Condition 4 on the visa page lets her embark at any
Vellorian port without a separate crew visa.

## The voyage — every date checks out

The stamps and the visa tell one trip, in order, all after the
passport was issued:

| Date | What happened |
|---|---|
| 02 JUN 2025 | Passport issued at Port Liora; fee of 40 VLR paid |
| 10 SEP 2025 | Greek visa GR-884120 issued in Lisbon (multiple entry, valid 20 SEP – 20 DEC 2025, 90 days, for a lighthouse conference) |
| 12 SEP 2025 | Entry stamp — Lisbon |
| 19 SEP 2025 | Departed Lisbon |
| 28 SEP 2025 | Entry stamp — Athens, inside the visa's validity |
| 09 OCT 2025 | Entry stamp — Istanbul |
| 16 OCT 2025 | Departed Istanbul |

A route map at the foot of the visa page plots the same four stops
in the same order, so the stamps, the visa and the map all agree.

The machine-readable zone at the foot of the data page is built with
real ICAO 9303 check digits (document number, birth date, expiry
date and the composite check), and the portrait is a drawn
illustration — no real person's photograph is used anywhere.

## How to run it

Requires Python 3.13 and Pillow, with the Liberation fonts installed
(the environment the bounty grader provides).

```sh
python3 main.py
```

That writes the passport spread to `/output/entry.png` (or to the
directory in `MAKEFUN_OUTPUT_DIR`). The image is a 1024×1024 PNG,
well under the 1 MiB limit. The program uses no network, no clock
and no randomness: running it twice writes byte-identical output.

To render the image into this directory instead, run:

```sh
python3 build_image.py
```

## Files

- `main.py` — the entrypoint: copies the bundled `entry.png` to `/output/entry.png` (stdlib only, no drawing at runtime)
- `build_image.py` — the drawing code and all passport text
- `entry.png` — the rendered passport spread
- `README.md` — this file
- `LICENSE` — MIT licence
