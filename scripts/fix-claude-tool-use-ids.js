#!/usr/bin/env node
/**
 * fix-claude-tool-use-ids.js
 *
 * Patch per Claude Code CLI (v2.x) che aggiunge la gestione dell'errore:
 *   API Error: 400 {"type":"error","error":{"type":"invalid_request_error",
 *              "message":"messages.N.content.M: tool_use ids must be unique"}}
 *
 * PROBLEMA:
 *   L'API Anthropic rifiuta la richiesta quando la cronologia della
 *   conversazione contiene due blocchi tool_use con lo stesso ID.
 *   Questo accade quando Claude Code accumula messaggi duplicati nella
 *   sessione (es. dopo retry, compaction o errori di concorrenza).
 *
 * SOLUZIONE:
 *   Aggiunge un handler specifico che:
 *   1. Scansiona l'array messages inviato all'API
 *   2. Individua gli ID tool_use duplicati
 *   3. Rimuove i blocchi duplicati (tool_use + relativi tool_result)
 *   4. Mostra un messaggio utile suggerendo di riprovare
 *
 * UTILIZZO:
 *   node scripts/fix-claude-tool-use-ids.js
 *
 * Da ri-eseguire dopo ogni aggiornamento di Claude Code.
 */

const fs = require('fs');
const path = require('path');

// Percorso del file CLI di Claude Code
const CLI_PATHS = [
  '/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js',
  path.join(process.env.HOME || '', '.npm', 'global', 'lib', 'node_modules', '@anthropic-ai', 'claude-code', 'cli.js'),
  '/usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js',
];

// Stringa target: il punto di inserimento (handler esistente adiacente)
const TARGET = 'if(A instanceof Z4&&A.status===400&&A.message.includes("unexpected `tool_use_id` found in `tool_result`"))c("tengu_unexpected_tool_result",{});';

// Nuovo handler da inserire PRIMA del target
const NEW_HANDLER = [
  'if(A instanceof Z4&&A.status===400&&A.message.includes("tool_use ids must be unique")){',
  'if(K?.messagesForAPI){',
  'let Y=new Set,z=new Set;',
  'for(let w of K.messagesForAPI)',
  'if(w.role==="assistant"&&Array.isArray(w.content))',
  'for(let H of w.content)',
  'if(H.type==="tool_use"&&H.id){',
  'if(Y.has(H.id))z.add(H.id);else Y.add(H.id)}',
  'if(z.size>0)',
  'for(let w of K.messagesForAPI)',
  'if(Array.isArray(w.content))',
  'w.content=w.content.filter((H)=>',
  '!(H.type==="tool_use"&&z.has(H.id))&&',
  '!(H.type==="tool_result"&&z.has(H.tool_use_id)))}',
  'let Y=i7()?"":" Run /rewind to recover the conversation.";',
  'return CY({content:"API Error: 400 due to duplicate tool_use IDs in conversation history. The conversation has been cleaned up - please retry your last message."+Y,error:"invalid_request"})}',
].join('');

let cliPath = null;
for (const p of CLI_PATHS) {
  if (fs.existsSync(p)) {
    cliPath = p;
    break;
  }
}

if (!cliPath) {
  console.error('ERRORE: File cli.js di Claude Code non trovato.');
  console.error('Percorsi controllati:', CLI_PATHS);
  process.exit(1);
}

console.log(`Trovato cli.js: ${cliPath}`);

let content = fs.readFileSync(cliPath, 'utf-8');

// Controlla se la patch è già applicata
if (content.includes('tool_use ids must be unique')) {
  console.log('✓ La patch è già applicata. Nessuna modifica necessaria.');
  process.exit(0);
}

if (!content.includes(TARGET)) {
  console.error('ERRORE: Stringa target non trovata in cli.js.');
  console.error('Il formato del file potrebbe essere cambiato dopo un aggiornamento.');
  console.error('Verifica manualmente la versione di Claude Code installata.');
  process.exit(1);
}

const patched = content.replace(TARGET, NEW_HANDLER + TARGET);
fs.writeFileSync(cliPath, patched, 'utf-8');

console.log('✓ Patch applicata con successo!');
console.log('');
console.log('FIX: Aggiunto handler per "tool_use ids must be unique"');
console.log('  - Deduplicazione automatica degli ID tool_use duplicati');
console.log('  - Messaggio utente chiaro con suggerimento di retry');
console.log('');
console.log('Riavvia Claude Code per applicare le modifiche.');
