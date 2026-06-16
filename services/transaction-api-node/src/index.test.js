const { describe, it, beforeEach } = require("node:test");
const assert = require("node:assert/strict");
const { app, transactions, validateTransaction } = require("./index.js");

function request(method, path, body) {
  return new Promise((resolve) => {
    const server = app.listen(0, async () => {
      const port = server.address().port;
      const url = `http://127.0.0.1:${port}${path}`;
      const options = { method, headers: { "Content-Type": "application/json" } };
      if (body) options.body = JSON.stringify(body);
      const res = await fetch(url, options);
      const data = await res.json().catch(() => null);
      server.close();
      resolve({ status: res.status, data });
    });
  });
}

describe("Transaction API", () => {
  beforeEach(() => {
    transactions.length = 0;
  });

  it("health returns ok", async () => {
    const { status, data } = await request("GET", "/health");
    assert.equal(status, 200);
    assert.equal(data.status, "ok");
  });

  it("creates credit transaction", async () => {
    const { status, data } = await request("POST", "/transactions", {
      amount: 100,
      type: "credit",
      description: "deposit",
    });
    assert.equal(status, 201);
    assert.equal(data.amount, 100);
    assert.equal(data.type, "credit");
    assert.equal(data.id, 1);
  });

  it("calculates balance correctly", async () => {
    await request("POST", "/transactions", { amount: 100, type: "credit" });
    await request("POST", "/transactions", { amount: 30, type: "debit" });
    const { status, data } = await request("GET", "/balance");
    assert.equal(status, 200);
    assert.equal(data.balance, 70);
    assert.equal(data.transaction_count, 2);
  });

  it("rejects invalid type", async () => {
    const { errors } = validateTransaction({ amount: 10, type: "transfer" });
    assert.ok(errors.length > 0);
  });

  it("rejects negative amount", async () => {
    const { errors } = validateTransaction({ amount: -5, type: "credit" });
    assert.ok(errors.length > 0);
  });
});
