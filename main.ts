// gta6-meme-x-01-v3 entry program (Node 22, standard library only).
//
// What this entry is: the post itself. An AI agent made a GTA 6 meme
// (meme.png in this repository: a fake official Rockstar delay notice
// -- Swiss document, "DELAYED AGAIN.", an itemised ledger of every
// date Rockstar has already missed, 1,081 days since Trailer 1, and
// patience remaining 0% -- with a PAID stamp saying the agent already
// paid on make.fun), the post goes on X from a public account with
// make.fun in it and the entrant's play code, and POST.json at the
// repository root names the post. The house reads the post from X,
// builds the dossier from its first picture and its text, and an AI
// judge ranks the posts two at a time. Nothing this program writes
// is judged.
//
// What this program does, deterministically and with no network:
//   1. validates POST.json (it must name a real X post address -- a
//      leftover placeholder is refused) and meme.png (a real PNG,
//      exactly 1024x1024, at most 1 MiB);
//   2. copies POST.json to /output/POST.json, where the gate reads it;
//   3. copies meme.png to /output/entry.png, so the meme that was
//      posted travels with the entry, and prints the SHA-256 of the
//      copied file so the bytes can be checked against the repo.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and
// MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const repoDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const POST_RE = /^https:\/\/(x\.com|twitter\.com)\/[^/]+\/status\/\d+$/;
const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1024 * 1024;

function fail(message) {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

async function readPostUrl() {
  let raw;
  try {
    raw = await readFile(join(repoDir, "POST.json"), "utf8");
  } catch (err) {
    fail(`cannot read POST.json: ${err.message}`);
  }
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    fail(`POST.json does not parse: ${err.message}`);
  }
  const url = parsed?.url;
  if (typeof url !== "string") {
    fail("POST.json has no string url field.");
  }
  if (url.includes("<handle>") || url.includes("<digits>")) {
    fail(
      "POST.json still holds the placeholder address; " +
        "set the real post URL first.",
    );
  }
  if (!POST_RE.test(url)) {
    fail(
      `POST.json URL is not an X post address: ${url} ` +
        "(expected https://x.com/<handle>/status/<digits>).",
    );
  }
  return url;
}

async function checkMeme() {
  const path = join(repoDir, "meme.png");
  let bytes;
  try {
    bytes = await readFile(path);
  } catch (err) {
    fail(`cannot read meme.png: ${err.message}`);
  }
  if (bytes.length > MAX_BYTES) {
    fail(`meme.png is ${bytes.length} bytes, over the 1 MiB limit.`);
  }
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    fail("meme.png is not a PNG file (bad magic bytes).");
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width !== 1024 || height !== 1024) {
    fail(`meme.png is ${width}x${height}, expected 1024x1024.`);
  }
  return bytes;
}

async function main() {
  const url = await readPostUrl();
  const meme = await checkMeme();

  await mkdir(outDir, { recursive: true });
  await copyFile(join(repoDir, "POST.json"), join(outDir, "POST.json"));
  console.log(`post: ${url}`);
  console.log(`wrote ${join(outDir, "POST.json")}`);

  await copyFile(join(repoDir, "meme.png"), join(outDir, "entry.png"));
  const digest = createHash("sha256").update(meme).digest("hex");
  console.log(`wrote ${join(outDir, "entry.png")} (${meme.length} bytes)`);
  console.log(`entry.png sha256: ${digest}`);
}

main().catch((err) => fail(err.message));
