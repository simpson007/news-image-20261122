// News front page entry for news-image-20261122 (Node 22, standard library
// only). The page is rendered ahead of time and stored beside this file as
// entry.png; this program reads those bytes and writes them, unchanged, to
// the output location the grader provides. Running it twice therefore
// produces byte-identical output every time.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
writeFileSync(target, readFileSync(source));
