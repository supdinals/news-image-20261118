[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/supdinals/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/supdinals/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# World News — Wednesday 18 November 2026 in one image

An entry for the make.fun bounty **news-image-20261118**: one 1024x1024 image
that sums up the world news of Wednesday 18 November 2026.

## What the image shows

- **Lead — Conflict / Middle East:** The US strikes a Guards missile site on
  Iran's Qeshm Island; Iran fires back at Bahrain (third interception this
  week) and Kuwait (first attack since September), and a Houthi missile aimed
  at Riyadh is destroyed.
- **1 — Diplomacy / Asia:** Xi Jinping and Vladimir Putin meet in Shenzhen as
  the APEC summit opens; a first Xi–Putin–Trump summit follows on Thursday.
- **2 — Health / Africa:** The UN appeals for help as Ebola cases double in
  DR Congo — over 11,000 cases and 5,500 deaths in six months, the
  second-largest Ebola outbreak on record.
- **3 — Politics / Americas:** Mary Peltola wins Alaska, giving Democrats a
  56–44 US Senate majority; she is the first Alaska Native in the Senate.
- **4 — Science / Space:** NASA's Voyager 1, launched in 1977, reaches one
  light-day from Earth; its signal now takes a full 24 hours to arrive.
- **5 — Weather / South Asia:** Cyclone Akvan strengthens into a severe storm
  off India's Andhra Pradesh coast (100–110 km/h), with landfall expected
  Friday between Nellore and Visakhapatnam.

Every claim is sourced in [SOURCES.md](SOURCES.md) (17 candidates researched,
each final story verified in at least two independent sources that were opened
and read). The variant selection process is documented in
[EVAL.md](EVAL.md).

## How it was made

The image was rendered with Python + Pillow by `build/render.py`, using only
the bundled Liberation Sans fonts (`build/fonts/`, SIL Open Font License 1.1 —
see `build/fonts/OFL.txt`) and icons drawn entirely with code. No photos,
logos, or third-party artwork. Three layouts were rendered and compared
pairwise; the winning layout (big lead + numbered list) was saved as
`entry.png`.

## The program

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. It uses no network, clock, or randomness, so two runs
write byte-identical output:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
sha256sum out/entry.png   # identical on every run
```

## License

MIT — see [LICENSE](LICENSE). The bundled fonts are under the SIL Open Font
License 1.1 (see `build/fonts/OFL.txt`).
