import { getPlatformProxy } from "wrangler";
import { readFileSync, writeFileSync } from "node:fs";
import { extractTranscript } from "./src/transcript.js";
const { env, dispose } = await getPlatformProxy({ configPath: "wrangler.jsonc", remoteBindings: true });
const src = process.env.SRC, type = process.env.TYPE || "application/pdf";
if (process.env.DUMP) {
  const md = await env.AI.toMarkdown({ name: "t.pdf", blob: new Blob([readFileSync(src)], { type }) });
  writeFileSync(process.env.DUMP, (Array.isArray(md) ? md[0] : md).data);
}
const t0 = Date.now();
const r = await extractTranscript(env, new File([readFileSync(src)], "t", { type }));
console.log(`== ${Date.now() - t0} ms`, r.error || "");
if (r.courses) {
  console.log(r.courses.map((c) => `${c.term} ${c.code.padEnd(9)} h=${c.hours} ${c.grade.padEnd(2)} ${c.points ?? ""} ${c.flag || ""} ${c.title}`).join("\n"));
  console.log("in progress:", r.inProgress.map((c) => `${c.term} ${c.code} h=${c.hours}`).join(", "), "| skipped:", r.skipped, "| summary:", JSON.stringify(r.summary));
}
await dispose();
