/** I4 — Node.js CLI client tests (written before implementation). */

const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const { parseArgs, formatResult } = require("./cli.js");

describe("Currency CLI", () => {
  it("parseArgs extracts from, to, amount", () => {
    const result = parseArgs(["node", "cli.js", "USD", "EUR", "100"]);
    assert.equal(result.from, "USD");
    assert.equal(result.to, "EUR");
    assert.equal(result.amount, 100);
  });

  it("parseArgs throws on missing args", () => {
    assert.throws(() => parseArgs(["node", "cli.js"]), /Usage/);
  });

  it("formatResult produces readable output", () => {
    const output = formatResult({
      from_currency: "USD",
      to_currency: "EUR",
      amount: 100,
      converted_amount: 92,
      rate: 0.92,
    });
    assert.ok(output.includes("100 USD"));
    assert.ok(output.includes("92 EUR"));
  });
});
