/** I4 — Node.js CLI client tests (written before implementation). */

const { describe, it, beforeEach, afterEach } = require("node:test");
const assert = require("node:assert/strict");
const { parseArgs, formatResult, convert, API_URL } = require("./cli.js");

describe("Currency CLI", () => {
  describe("parseArgs", () => {
    it("extracts from, to, amount", () => {
      const result = parseArgs(["node", "cli.js", "USD", "EUR", "100"]);
      assert.equal(result.from, "USD");
      assert.equal(result.to, "EUR");
      assert.equal(result.amount, 100);
    });

    it("throws on missing args", () => {
      assert.throws(() => parseArgs(["node", "cli.js"]), /Usage/);
    });

    it("normalizes lowercase currencies to uppercase", () => {
      const result = parseArgs(["node", "cli.js", "usd", "eur", "50"]);
      assert.equal(result.from, "USD");
      assert.equal(result.to, "EUR");
      assert.equal(result.amount, 50);
    });

    it("rejects zero amount", () => {
      assert.throws(
        () => parseArgs(["node", "cli.js", "USD", "EUR", "0"]),
        /Amount must be a positive number/
      );
    });

    it("rejects non-numeric amount", () => {
      assert.throws(
        () => parseArgs(["node", "cli.js", "USD", "EUR", "abc"]),
        /Amount must be a positive number/
      );
    });
  });

  describe("formatResult", () => {
    it("produces readable output", () => {
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

    it("handles decimal amounts", () => {
      const output = formatResult({
        from_currency: "USD",
        to_currency: "EUR",
        amount: 10.5,
        converted_amount: 9.66,
        rate: 0.92,
      });
      assert.ok(output.includes("10.5 USD"));
      assert.ok(output.includes("9.66 EUR"));
      assert.ok(output.includes("rate: 0.92"));
    });
  });

  describe("convert", () => {
    /** @type {typeof fetch | undefined} */
    let originalFetch;

    beforeEach(() => {
      originalFetch = globalThis.fetch;
    });

    afterEach(() => {
      globalThis.fetch = originalFetch;
    });

    it("returns parsed JSON on success", async () => {
      const mockData = {
        from_currency: "USD",
        to_currency: "EUR",
        amount: 100,
        converted_amount: 92,
        rate: 0.92,
      };

      globalThis.fetch = async (url, options) => {
        assert.equal(url, `${API_URL}/convert`);
        assert.equal(options.method, "POST");
        assert.equal(options.headers["Content-Type"], "application/json");
        assert.deepEqual(JSON.parse(options.body), {
          from_currency: "USD",
          to_currency: "EUR",
          amount: 100,
        });
        return {
          ok: true,
          json: async () => mockData,
        };
      };

      const result = await convert("USD", "EUR", 100);
      assert.deepEqual(result, mockData);
    });

    it("throws with detail message on API error", async () => {
      globalThis.fetch = async () => ({
        ok: false,
        status: 400,
        json: async () => ({ detail: "Invalid currency code" }),
      });

      await assert.rejects(() => convert("USD", "XXX", 100), {
        message: "Invalid currency code",
      });
    });
  });
});
