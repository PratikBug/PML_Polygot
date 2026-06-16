/** A3 — Node.js worker tests. */

const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const { buildScoreInput, parseScoreOutput } = require("./worker.js");

describe("Fraud Worker", () => {
  it("buildScoreInput creates valid JSON for scorer", () => {
    const tx = { id: 1, user_id: "u1", amount: 500, merchant: "Amazon", currency: "USD" };
    const input = buildScoreInput(tx);
    assert.equal(input.transaction_id, 1);
    assert.equal(input.amount, 500);
    assert.equal(input.merchant, "Amazon");
  });

  it("parseScoreOutput extracts risk fields", () => {
    const output = '{"transaction_id":1,"risk_score":75.0,"risk_level":"high","factors":["high_amount"]}';
    const result = parseScoreOutput(output);
    assert.equal(result.risk_score, 75);
    assert.equal(result.risk_level, "high");
    assert.ok(result.factors.includes("high_amount"));
  });

  it("parseScoreOutput throws on invalid JSON", () => {
    assert.throws(() => parseScoreOutput("not json"), /Invalid scorer output/);
  });
});
