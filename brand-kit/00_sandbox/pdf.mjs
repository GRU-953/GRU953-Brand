// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader (GRU953)
import { browser } from './render.mjs';
const b = await browser();
const p = await b.newPage();
await p.goto('file://'+process.argv[2]);
await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>{[...document.querySelectorAll('details')].forEach(d=>d.open=true)});
await p.waitForTimeout(1200);
await p.pdf({path:process.argv[3], format:'A4', printBackground:true,
  margin:{top:'14mm',bottom:'14mm',left:'14mm',right:'14mm'}});
await b.close();
