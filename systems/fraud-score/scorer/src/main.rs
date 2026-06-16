//! A3 — Rust fraud scorer CLI: reads JSON from stdin, outputs JSON to stdout.

use fraud_scorer::{calculate_risk, TransactionInput};
use std::io::{self, Read};

fn main() {
    let mut input_str = String::new();
    io::stdin().read_to_string(&mut input_str).expect("Failed to read stdin");

    let input: TransactionInput =
        serde_json::from_str(&input_str).expect("Invalid JSON input");

    let result = calculate_risk(&input);
    let json = serde_json::to_string(&result).expect("Failed to serialize");
    println!("{}", json);
}
