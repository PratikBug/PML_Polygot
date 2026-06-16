/** I4 — Node.js CLI client for currency converter API. */

const API_URL = process.env.CONVERTER_API_URL || "http://localhost:8001";

function parseArgs(argv) {
  const args = argv.slice(2);
  if (args.length < 3) {
    throw new Error("Usage: node cli.js <from> <to> <amount>");
  }
  const amount = parseFloat(args[2]);
  if (isNaN(amount) || amount <= 0) {
    throw new Error("Amount must be a positive number");
  }
  return { from: args[0].toUpperCase(), to: args[1].toUpperCase(), amount };
}

function formatResult(data) {
  return `${data.amount} ${data.from_currency} = ${data.converted_amount} ${data.to_currency} (rate: ${data.rate})`;
}

async function convert(from, to, amount) {
  const response = await fetch(`${API_URL}/convert`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ from_currency: from, to_currency: to, amount }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `API error: ${response.status}`);
  }
  return response.json();
}

async function main() {
  const { from, to, amount } = parseArgs(process.argv);
  const result = await convert(from, to, amount);
  console.log(formatResult(result));
}

if (require.main === module) {
  main().catch((err) => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  });
}

module.exports = { parseArgs, formatResult, convert, API_URL };
