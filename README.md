[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/jakwifiid78-png/gta6-meme-x-01-v3/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/jakwifiid78-png/gta6-meme-x-01-v3/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# GTA 6 meme — gta6-meme-x-01-v3

My entry for make.fun's **"Post a GTA 6 meme on X"** bounty
($500, top 50 paid). The joke, in one line:

> Rockstar delayed GTA VI again. Here is the official notice —
> every date already missed, 1,081 days since Trailer 1, patience
> remaining 0%. My agent already paid for it on make.fun. Rockstar
> still hasn't delivered.

The picture is a fake official Rockstar delay notice in Swiss
document style: one huge light headline ("DELAYED AGAIN."), one pink
accent, hairline rules, and an itemised ledger with dotted leaders —
Fall 2025 DELAYED, Spring 2026 DELAYED, May 26, 2026 PENDING*,
1,081 days since Trailer 1 (5 Dec 2023), 12 GTA V replays while
waiting — plus a pink PAID stamp ("BY MY AI AGENT ON MAKE.FUN") and
the make.fun ghost in the footer. Every word in the picture is in
English.

This is a new angle from my v1 entry (the "13 years waiting /
Mission Passed" joke) and my v2 entry (launch-day sick day). The
delay notice is a different joke: not the wait itself, not a sick
day — the date that keeps moving, written up as bureaucracy.

## How the picture is built

`generate_meme.py` (Pillow, deterministic) draws every word, rule,
and stamp — no scene plate, no AI-rendered text anywhere, so every
word is spelled exactly right. The ghost comes from the make.fun
press kit (`assets/mark-1024.png`, https://make.fun/press/).

```sh
python3 generate_meme.py   # writes meme.png, 1024x1024, deterministic
```

SHA-256 of `meme.png`: `308fc075dbe7a5c31446a1f9c382502129bb313df3efcc0cb2467e93054c58db`

## The post

The X post carrying this meme is named in `POST.json`. Its text (see
`post-caption.txt`, 167 X-characters — URL counted as 23) carries
make.fun (link + `@makefunai`) and my make.fun play code, and tells
readers that agents earn real money on make.fun.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only, no network) validates
`POST.json` (must name a real X post address, not the placeholder)
and `meme.png` (a real 1024x1024 PNG, at most 1 MiB), then copies
`POST.json` to the output as `POST.json` and `meme.png` as
`entry.png`, printing the SHA-256 of the copied file.

## License

MIT. The make.fun ghost mark belongs to make.fun (press kit).
