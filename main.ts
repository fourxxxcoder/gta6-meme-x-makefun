// Entry program for make.fun's "Post a GTA 6 meme on X" bounty.
//
// The real entry is the post on X: a GTA 6 meme whose picture carries
// the make.fun ghost, posted publicly with the bounty link and a play
// code in its text. This program's only job is to hand that post's
// address to the grader: it copies POST.json from the repository root
// into the output directory, byte for byte, and prints nothing.
//
// Local run, the way the grader runs it:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

try {
  copyFileSync(join(botDir, "POST.json"), join(outputDir, "POST.json"));
} catch (err) {
  // A missing POST.json means the entry names no post at all: fail
  // loudly here instead of letting the grader find an empty output.
  console.error(`could not copy POST.json from ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}
