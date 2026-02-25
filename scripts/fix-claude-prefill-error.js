#!/usr/bin/env node
/**
 * fix-claude-prefill-error.js
 *
 * Patch per Claude Code CLI (v2.x) che aggiunge la gestione dell'errore:
 *   API Error: 400 {"type":"error","error":{"type":"invalid_request_error",
 *              "message":"This model does not support assistant message prefill.
 *               The conversation must end with a user message."}}
 *
 * PROBLEMA:
 *   L'API Anthropic rifiuta la richiesta quando l'array messages termina
 *   con un messaggio di ruolo "assistant" anziché "user".
 *   Questo accade quando Claude Code accumula messaggi durante una sessione
 *   lunga: dopo un blocco tool_use completato, il cursore interno può
 *   risultare su un messaggio assistant, e il successivo invio all'API
 *   include quel trailing assistant message che alcuni modelli non accettano
 *   in modalità prefill.
 *
 * SOLUZIONE:
 *   Aggiunge un handler specifico che:
 *   1. Intercetta l'errore 400 con messaggio "does not support assistant message prefill"
 *   2. Rimuove automaticamente i messaggi assistant in coda da K.messagesForAPI e K.messages
 *   3. Mostra un messaggio chiaro suggerendo di riprovare
 *
 * UTILIZZO:
 *   node scripts/fix-claude-prefill-error.js
 *
 * Da ri-eseguire dopo ogni aggiornamento di Claude Code.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

// Percorso del file CLI di Claude Code
const CLI_PATHS = [
  '/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js',
  join(process.env.HOME || '', '.npm', 'global', 'lib', 'node_modules', '@anthropic-ai', 'claude-code', 'cli.js'),
  '/usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js',
];

// Stringa target: il punto di inserimento (handler esistente adiacente)
const TARGET = 'if(A instanceof Z4&&A.status===400&&A.message.includes("unexpected `tool_use_id` found in `tool_result`"))c("tengu_unexpected_tool_result",{});';

// Nuovo handler da inserire PRIMA del target
const NEW_HANDLER = [
  'if(A instanceof Z4&&A.status===400&&A.message.includes("does not support assistant message prefill")){',
  'if(K?.messagesForAPI){',
  'while(K.messagesForAPI.length>0&&K.messagesForAPI[K.messagesForAPI.length-1].role==="assistant")',
  'K.messagesForAPI.pop()}',
  'if(K?.messages){',
  'while(K.messages.length>0&&K.messages[K.messages.length-1].role==="assistant")',
  'K.messages.pop()}',
  'let Y=i7()?"":" Run /rewind to recover the conversation.";',
  'return CY({content:"API Error: 400 - This model does not support assistant message prefill. Trailing assistant messages have been removed from conversation history - please retry your last message."+Y,error:"invalid_request"})}',
].join('');

let cliPath = null;
for (const p of CLI_PATHS) {
  if (existsSync(p)) {
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

let content = readFileSync(cliPath, 'utf-8');

// Controlla se la patch è già applicata
if (content.includes('does not support assistant message prefill')) {
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
writeFileSync(cliPath, patched, 'utf-8');

console.log('✓ Patch applicata con successo!');
console.log('');
console.log('FIX: Aggiunto handler per "does not support assistant message prefill"');
console.log('  - Rimozione automatica dei messaggi assistant in coda alla cronologia');
console.log('  - Messaggio utente chiaro con suggerimento di retry');
console.log('');
console.log('Riavvia Claude Code per applicare le modifiche.');
