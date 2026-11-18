# EVAL — Self-judging of the three variants (Phase D)

Question used for every comparison, per the owner brief: *"Which image best
sums up the world news of Wednesday 18 November 2026 for a careful picture
editor?"* — judged on: naming the day, selection and breadth, readability
from the image alone, faithfulness, and craft/legibility at small size.
Each pair was compared 3 times, with the left/right (first/second) position
swapped between rounds. All three variants carry identical stories and
wording; only layout differs. Variants were also inspected at 512x512.

## Variants

- **A** — dark tile grid: lead tile, 2x2 supporting tiles, wide weather tile.
- **B** — newspaper front page: cream paper, masthead, two columns, weather strip.
- **C** — big lead + numbered list 1–5 (the pattern that won the 17 Nov edition 11/12).

## Pairwise results (3 rounds per pair, positions swapped)

| Pair | Round 1 | Round 2 (swapped) | Round 3 | Pair score |
|---|---|---|---|---|
| A vs B | A | A | A | A 3–0 |
| A vs C | C | C | A | C 2–1 |
| B vs C | C | C | C | C 3–0 |

Win rate over the 6 rounds each variant played: **C 5/6 (83%), A 4/6 (67%),
B 0/6 (0%)**. Winner: **C**.

## Why

- **A vs B:** A's tiles carry the full body text of every story and stay
  legible at 512px. B's short column bodies drop detail, its type is the
  smallest of the three, and it leaves a large empty band above the footer.
- **A vs C:** C's single-column numbered scan is the fastest to read and its
  list headlines stay bold at 512px; A's weather tile squeezes its headline
  onto one small line. A took one round because its tile bodies are more
  complete (e.g. the Ebola "second-largest on record" detail).
- **B vs C:** C wins every round — same completeness gap as against A, plus
  B's weakest small-size legibility.

## Weaknesses found and fixed in the winner (C)

1. One-line list bodies dropped two details A carried — restored within the
   one-line budget: Ebola body now ends "second-largest on record", Voyager
   body now says "the first object this far out", and the cyclone body now
   names the landfall stretch "Nellore–Visakhapatnam".
2. Earlier drafts of B and C overflowed the canvas (fifth story cut off);
   both were re-laid-out and re-checked before judging, so all comparisons
   used complete images.

## Residual weaknesses (accepted)

- The lead icon (starburst over an island in a strait) reads partly as a sun
  over an island; it is decorative and no story depends on it.
- C's one-line bodies are necessarily terser than A's full tile bodies;
  the judging rounds still favoured C's readability over A's completeness.

## Final entry

`entry.png` = variant C after the fixes above.
1024x1024 PNG, 141,681 bytes, sha256
a374f69b4eb387f0cecb30bb2d50413e7325df6a06828ea64ee8961d9c510830
(re-verified in Phase E via two runs of main.py).

Checklist: all facts match SOURCES.md; no typos found on a line-by-line
read; readable at 512px; no clipped or overlapping text; all graphics are
original code-drawn icons; date "WEDNESDAY 18 NOVEMBER 2026" is prominent;
no photos, logos, faces, or hidden text.
