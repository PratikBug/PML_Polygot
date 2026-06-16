/** B5 — Node.js transaction API (mirrors B4 FastAPI service). */

const express = require("express");

const app = express();
app.use(express.json());

const transactions = [];

function validateTransaction(body) {
  const errors = [];
  if (typeof body.amount !== "number" || body.amount <= 0) {
    errors.push("amount must be a positive number");
  }
  const type = (body.type || "").toLowerCase().trim();
  if (!["credit", "debit"].includes(type)) {
    errors.push("type must be 'credit' or 'debit'");
  }
  if (body.description && body.description.length > 200) {
    errors.push("description must be 200 characters or fewer");
  }
  return { errors, type };
}

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.post("/transactions", (req, res) => {
  const { errors, type } = validateTransaction(req.body);
  if (errors.length > 0) {
    return res.status(400).json({ errors });
  }
  const record = {
    id: transactions.length + 1,
    amount: req.body.amount,
    type,
    description: req.body.description || "",
  };
  transactions.push(record);
  res.status(201).json(record);
});

app.get("/transactions", (_req, res) => {
  res.json(transactions);
});

app.get("/balance", (_req, res) => {
  let balance = 0;
  for (const tx of transactions) {
    balance += tx.type === "credit" ? tx.amount : -tx.amount;
  }
  res.json({ balance, transaction_count: transactions.length });
});

const PORT = process.env.PORT || 3000;

if (require.main === module) {
  app.listen(PORT, () => console.log(`Transaction API listening on :${PORT}`));
}

module.exports = { app, transactions, validateTransaction };
