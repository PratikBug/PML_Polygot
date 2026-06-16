/** A3 — Node.js worker: polls API, scores via Rust CLI, updates results. */

const { execSync } = require("child_process");

const API_URL = process.env.FRAUD_API_URL || "http://localhost:8002";
const SCORER_PATH = process.env.SCORER_PATH || "../scorer/target/release/fraud-scorer";
const POLL_INTERVAL_MS = parseInt(process.env.POLL_INTERVAL_MS || "3000", 10);

function buildScoreInput(tx) {
  return {
    transaction_id: tx.id,
    user_id: tx.user_id,
    amount: parseFloat(tx.amount),
    merchant: tx.merchant,
    currency: tx.currency || "USD",
  };
}

function parseScoreOutput(stdout) {
  try {
    return JSON.parse(stdout.trim());
  } catch {
    throw new Error(`Invalid scorer output: ${stdout}`);
  }
}

async function fetchPending() {
  const res = await fetch(`${API_URL}/transactions/pending`);
  if (!res.ok) throw new Error(`Failed to fetch pending: ${res.status}`);
  return res.json();
}

function scoreTransaction(input) {
  const json = JSON.stringify(input);
  const output = execSync(`${SCORER_PATH}`, { input: json, encoding: "utf-8", timeout: 10000 });
  return parseScoreOutput(output);
}

async function updateScore(transactionId, score) {
  const res = await fetch(`${API_URL}/transactions/${transactionId}/score`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(score),
  });
  if (!res.ok) throw new Error(`Failed to update score: ${res.status}`);
  return res.json();
}

async function processOnce() {
  const pending = await fetchPending();
  if (pending.length === 0) {
    console.log("[worker] No pending transactions");
    return 0;
  }

  let processed = 0;
  for (const tx of pending) {
    try {
      const input = buildScoreInput(tx);
      const score = scoreTransaction(input);
      await updateScore(tx.id, score);
      console.log(`[worker] Scored tx ${tx.id}: ${score.risk_level} (${score.risk_score})`);
      processed++;
    } catch (err) {
      console.error(`[worker] Error processing tx ${tx.id}: ${err.message}`);
    }
  }
  return processed;
}

async function main() {
  console.log(`[worker] Starting — API: ${API_URL}, scorer: ${SCORER_PATH}`);
  const count = await processOnce();
  if (process.env.WORKER_MODE === "daemon") {
    setInterval(async () => {
      try {
        await processOnce();
      } catch (err) {
        console.error(`[worker] Poll error: ${err.message}`);
      }
    }, POLL_INTERVAL_MS);
  } else {
    console.log(`[worker] Processed ${count} transactions`);
  }
}

if (require.main === module) {
  main().catch((err) => {
    console.error(`[worker] Fatal: ${err.message}`);
    process.exit(1);
  });
}

module.exports = { buildScoreInput, parseScoreOutput, scoreTransaction, API_URL };
