#!/usr/bin/env node
/**
 * fix-claude-tool-use-ids.js
 *
 * Robust patch for Claude Code CLI that fixes the API error:
 *   API Error: 400 {"type":"error","error":{"type":"invalid_request_error",
 *              "message":"messages.N.content.M: tool_use ids must be unique"}}
 *
 * PROBLEM:
 *   The Anthropic API rejects requests when the conversation history contains
 *   two or more tool_use blocks with the same ID. This happens when Claude Code
 *   accumulates duplicate messages during a session (e.g., after retries,
 *   compaction, or concurrency errors).
 *
 * SOLUTION:
 *   Inserts a new error handler into the CLI's error-handling chain that:
 *   1. Detects the "tool_use ids must be unique" error from the API
 *   2. Scans the messagesForAPI array for duplicate tool_use IDs
 *   3. Removes the duplicate tool_use and corresponding tool_result blocks
 *   4. Returns a user-friendly message suggesting retry
 *
 * APPROACH:
 *   Instead of matching exact minified variable names (which change between
 *   versions), this script uses regex patterns to find the structural anchor
 *   point in the error handler function. It identifies:
 *   - The error handler function (3-param function with API error handling)
 *   - The "unexpected tool_use_id" error check (stable string literal anchor)
 *   - The variable names dynamically from surrounding code
 *
 * USAGE:
 *   node scripts/fix-claude-tool-use-ids.js
 *
 * Must be re-run after every Claude Code update.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { join, dirname } from 'path';

// ============================================================================
// Step 1: Find the Claude Code cli.js file dynamically
// ============================================================================

function findCliPath() {
  // Static paths to check
  const staticPaths = [
    '/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js',
    '/usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js',
    '/usr/lib/node_modules/@anthropic-ai/claude-code/cli.js',
    join(process.env.HOME || '', '.npm', 'global', 'lib', 'node_modules', '@anthropic-ai', 'claude-code', 'cli.js'),
    join(process.env.HOME || '', '.nvm', 'versions', 'node'),  // will be handled below
  ];

  // Check static paths first
  for (const p of staticPaths) {
    if (existsSync(p) && p.endsWith('.js')) {
      return p;
    }
  }

  // Try to resolve via npm root -g
  try {
    const npmRoot = execSync('npm root -g', { encoding: 'utf-8' }).trim();
    const npmPath = join(npmRoot, '@anthropic-ai', 'claude-code', 'cli.js');
    if (existsSync(npmPath)) return npmPath;
  } catch {}

  // Try to find via `which claude` and resolve symlinks
  try {
    const claudeBin = execSync('which claude', { encoding: 'utf-8' }).trim();
    if (claudeBin) {
      // Resolve symlinks
      const realPath = execSync(`readlink -f "${claudeBin}"`, { encoding: 'utf-8' }).trim();
      // The binary is typically in .../bin/claude, and cli.js is in .../lib/node_modules/@anthropic-ai/claude-code/cli.js
      // Or it could be a symlink directly into the package
      const packageDir = dirname(realPath);
      // Check if cli.js is in the same directory
      let cliCandidate = join(packageDir, 'cli.js');
      if (existsSync(cliCandidate)) return cliCandidate;
      // Check parent patterns like .../node_modules/@anthropic-ai/claude-code/
      cliCandidate = join(packageDir, '..', 'lib', 'node_modules', '@anthropic-ai', 'claude-code', 'cli.js');
      if (existsSync(cliCandidate)) return cliCandidate;
    }
  } catch {}

  // Try find command as a last resort (limit depth to avoid long scans)
  try {
    const found = execSync(
      'find /opt /usr/local /usr/lib -maxdepth 8 -name "cli.js" -path "*claude-code*" 2>/dev/null | head -1',
      { encoding: 'utf-8' }
    ).trim();
    if (found && existsSync(found)) return found;
  } catch {}

  return null;
}

// ============================================================================
// Step 2: Extract minified variable names from the code structure
// ============================================================================

/**
 * Finds the error handler function and extracts the variable names used
 * for error class, return function, and headless check.
 *
 * We look for the structural pattern:
 *   function FUNCNAME(ERR, MODEL, CONTEXT) {
 *     ... instanceof ERRORCLASS && ERRORCLASS.status === 400 ...
 *     ... RETURNFN({content: ..., error: ...}) ...
 *     ... HEADLESSFN() ? "" : " Run /rewind ..." ...
 */
function extractVariableNames(content) {
  const result = {};

  // Find the error class name: X instanceof <CLASS> && A.status===400
  // This is the class used for APIError checks
  const errorClassMatch = content.match(
    /instanceof\s+([A-Za-z0-9_$]+)&&[A-Za-z0-9_$]+\.status===400&&[A-Za-z0-9_$]+\.message\.includes\("unexpected `tool_use_id` found in `tool_result`"\)/
  );
  if (errorClassMatch) {
    result.errorClass = errorClassMatch[1];
  }

  // Find the error parameter name (the first param in the function)
  // Look for: instanceof <errorClass>&&<ERR>.status===400
  if (result.errorClass) {
    const errParamMatch = content.match(
      new RegExp(`instanceof\\s+${escapeRegex(result.errorClass)}&&([A-Za-z0-9_$]+)\\.status===400`)
    );
    if (errParamMatch) {
      result.errParam = errParamMatch[1];
    }
  }

  // Find the return function: return <FN>({content:...,error:"invalid_request"})
  // Use the tool_use concurrency handler which we know exists
  const returnFnMatch = content.match(
    /return\s+([A-Za-z0-9_$]+)\(\{content:"API Error: 400 due to tool use concurrency issues\."/
  );
  if (returnFnMatch) {
    result.returnFn = returnFnMatch[1];
  }

  // Find the headless check function: <FN>()?"":" Run /rewind to recover the conversation."
  const headlessFnMatch = content.match(
    /([A-Za-z0-9_$]+)\(\)\?"":"\s*Run \/rewind to recover the conversation\."/
  );
  if (headlessFnMatch) {
    result.headlessFn = headlessFnMatch[1];
  }

  // Find the context parameter (3rd param that has .messagesForAPI)
  // Pattern: if(<CONTEXT>?.messages&&<CONTEXT>?.messagesForAPI)
  const contextParamMatch = content.match(
    /if\(([A-Za-z0-9_$]+)\?\.messages&&\1\?\.messagesForAPI\)/
  );
  if (contextParamMatch) {
    result.contextParam = contextParamMatch[1];
  }

  return result;
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// ============================================================================
// Step 3: Build the patch using extracted variable names
// ============================================================================

function buildPatchHandler(vars) {
  const E = vars.errParam || 'A';       // error parameter
  const EC = vars.errorClass || 'Z4';   // error class (APIError)
  const K = vars.contextParam || 'K';   // context with messages
  const RET = vars.returnFn || 'CY';    // return function
  const HL = vars.headlessFn || 'i7';   // headless check

  // The handler that deduplicates tool_use IDs and returns a friendly message
  return [
    `if(${E} instanceof ${EC}&&${E}.status===400&&${E}.message.includes("tool_use ids must be unique")){`,
    `if(${K}?.messagesForAPI){`,
    `let _seen=new Set,_dups=new Set;`,
    `for(let _m of ${K}.messagesForAPI)`,
    `if(_m.role==="assistant"&&Array.isArray(_m.content))`,
    `for(let _b of _m.content)`,
    `if(_b.type==="tool_use"&&_b.id){`,
    `if(_seen.has(_b.id))_dups.add(_b.id);else _seen.add(_b.id)}`,
    `if(_dups.size>0)`,
    `for(let _m of ${K}.messagesForAPI)`,
    `if(Array.isArray(_m.content))`,
    `_m.content=_m.content.filter((_b)=>`,
    `!(_b.type==="tool_use"&&_dups.has(_b.id))&&`,
    `!(_b.type==="tool_result"&&_dups.has(_b.tool_use_id)))}`,
    `let _rw=${HL}()?"":" Run /rewind to recover the conversation.";`,
    `return ${RET}({content:"API Error: 400 due to duplicate tool_use IDs in conversation history. The duplicates have been cleaned up - please retry your last message."+_rw,error:"invalid_request"})}`,
  ].join('');
}

// ============================================================================
// Step 4: Find the insertion point using multiple strategies
// ============================================================================

function findInsertionPoint(content, vars) {
  const strategies = [];

  // Strategy 1: Exact string match for the "unexpected tool_use_id" handler
  // This is the most reliable anchor - it's right after the tool_use concurrency handler
  const EC = vars.errorClass || 'Z4';
  const E = vars.errParam || 'A';

  // Build regex that matches: if(ERR instanceof CLASS && ERR.status===400 && ERR.message.includes("unexpected `tool_use_id` found in `tool_result`"))
  const strategy1Regex = new RegExp(
    `if\\(${escapeRegex(E)}\\s*instanceof\\s+${escapeRegex(EC)}&&${escapeRegex(E)}\\.status===400&&${escapeRegex(E)}\\.message\\.includes\\("unexpected \`tool_use_id\` found in \`tool_result\`"\\)\\)`
  );
  const match1 = content.match(strategy1Regex);
  if (match1) {
    strategies.push({
      name: 'Strategy 1: Before "unexpected tool_use_id" handler (regex with extracted vars)',
      index: match1.index,
      insertBefore: match1[0],
    });
  }

  // Strategy 2: Use the string literal directly (version-independent)
  const strategy2Literal = 'unexpected `tool_use_id` found in `tool_result`';
  const idx2 = content.indexOf(strategy2Literal);
  if (idx2 !== -1) {
    // Walk backwards to find the start of the if-statement
    const searchStart = Math.max(0, idx2 - 200);
    const prefix = content.substring(searchStart, idx2);
    const ifStart = prefix.lastIndexOf('if(');
    if (ifStart !== -1) {
      strategies.push({
        name: 'Strategy 2: Before "unexpected tool_use_id" handler (string literal search)',
        index: searchStart + ifStart,
        insertBefore: content.substring(searchStart + ifStart, idx2 + strategy2Literal.length + 3),
      });
    }
  }

  // Strategy 3: Look for the end of the "tool use concurrency" handler block
  // Pattern: error:"invalid_request"})}}if(...unexpected tool_use_id...)
  const strategy3Regex = /error:"invalid_request"\}\)\}\}(if\([^)]*\.includes\("unexpected `tool_use_id` found in `tool_result`"\))/;
  const match3 = content.match(strategy3Regex);
  if (match3) {
    strategies.push({
      name: 'Strategy 3: After concurrency handler, before unexpected_tool_result handler',
      index: match3.index + match3[0].length - match3[1].length,
      insertBefore: match3[1],
    });
  }

  // Strategy 4: Fallback - look for any 400 error handler pattern near tool_use related code
  const strategy4Regex = new RegExp(
    `if\\([A-Za-z0-9_$]+\\s*instanceof\\s+[A-Za-z0-9_$]+&&[A-Za-z0-9_$]+\\.status===400&&[A-Za-z0-9_$]+\\.message\\.includes\\("unexpected \`tool_use_id\` found in \`tool_result\`"\\)\\)`
  );
  const match4 = content.match(strategy4Regex);
  if (match4) {
    strategies.push({
      name: 'Strategy 4: Generic regex for unexpected_tool_result handler (any var names)',
      index: match4.index,
      insertBefore: match4[0],
    });
  }

  return strategies;
}

// ============================================================================
// Main
// ============================================================================

console.log('=== Claude Code - Duplicate tool_use ID Fix ===\n');

// Find CLI path
const cliPath = findCliPath();
if (!cliPath) {
  console.error('ERROR: Could not find Claude Code cli.js file.');
  console.error('Checked common installation paths and used npm/which for dynamic discovery.');
  console.error('Make sure Claude Code is installed globally via npm.');
  process.exit(1);
}

console.log(`Found cli.js: ${cliPath}`);

// Read the file
let content = readFileSync(cliPath, 'utf-8');
console.log(`File size: ${(content.length / 1024 / 1024).toFixed(1)} MB`);

// Check if patch is already applied
if (content.includes('tool_use ids must be unique')) {
  console.log('\n[OK] Patch is already applied. No changes needed.');
  process.exit(0);
}

// Get Claude Code version
try {
  const pkgPath = join(dirname(cliPath), 'package.json');
  if (existsSync(pkgPath)) {
    const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));
    console.log(`Claude Code version: ${pkg.version || 'unknown'}`);
  }
} catch {}

// Extract variable names from the minified code
console.log('\nAnalyzing minified code structure...');
const vars = extractVariableNames(content);
console.log('  Error class:     ', vars.errorClass || '(not found, using fallback Z4)');
console.log('  Error param:     ', vars.errParam || '(not found, using fallback A)');
console.log('  Return function: ', vars.returnFn || '(not found, using fallback CY)');
console.log('  Headless check:  ', vars.headlessFn || '(not found, using fallback i7)');
console.log('  Context param:   ', vars.contextParam || '(not found, using fallback K)');

// Find insertion point
console.log('\nSearching for insertion point...');
const strategies = findInsertionPoint(content, vars);

if (strategies.length === 0) {
  console.error('\nERROR: Could not find any suitable insertion point in cli.js.');
  console.error('The file format may have changed significantly after a Claude Code update.');
  console.error('');
  console.error('Debug info - looking for these anchor patterns:');
  console.error('  - String "unexpected `tool_use_id` found in `tool_result`":',
    content.includes('unexpected `tool_use_id` found in `tool_result`') ? 'FOUND' : 'NOT FOUND');
  console.error('  - String "tengu_unexpected_tool_result":',
    content.includes('tengu_unexpected_tool_result') ? 'FOUND' : 'NOT FOUND');
  console.error('  - String "tool use concurrency":',
    content.includes('tool use concurrency') ? 'FOUND' : 'NOT FOUND');
  console.error('  - String "tool_use_id":',
    content.includes('tool_use_id') ? 'FOUND' : 'NOT FOUND');
  process.exit(1);
}

// Use the first (best) strategy
const chosen = strategies[0];
console.log(`\nUsing: ${chosen.name}`);
console.log(`  Insertion index: ${chosen.index}`);

// Build the patch handler
const handler = buildPatchHandler(vars);

// Apply the patch - insert the new handler before the anchor point
const before = content.substring(0, chosen.index);
const after = content.substring(chosen.index);
const patched = before + handler + after;

// Safety check: make sure we didn't break the file structure
if (patched.length < content.length) {
  console.error('ERROR: Patched file is shorter than original. Something went wrong.');
  process.exit(1);
}

const expectedGrowth = handler.length;
const actualGrowth = patched.length - content.length;
if (actualGrowth !== expectedGrowth) {
  console.error(`ERROR: Unexpected size change. Expected +${expectedGrowth}, got +${actualGrowth}.`);
  process.exit(1);
}

// Write the patched file
writeFileSync(cliPath, patched, 'utf-8');

// Verify
const verify = readFileSync(cliPath, 'utf-8');
if (!verify.includes('tool_use ids must be unique')) {
  console.error('ERROR: Verification failed - patch string not found in written file.');
  process.exit(1);
}

console.log('\n[OK] Patch applied successfully!');
console.log('');
console.log('What was added:');
console.log('  - Handler for "tool_use ids must be unique" API error');
console.log('  - Automatic deduplication of duplicate tool_use IDs in conversation history');
console.log('  - Removes both duplicate tool_use blocks and their corresponding tool_result blocks');
console.log('  - Returns a clear user message suggesting to retry the last message');
console.log('');
console.log('Restart Claude Code for the changes to take effect.');
console.log(`Handler size: ${handler.length} bytes inserted at position ${chosen.index}`);
