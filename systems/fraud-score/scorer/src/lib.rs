//! A3 — Fraud risk scoring engine.

use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct TransactionInput {
    pub transaction_id: u64,
    pub user_id: String,
    pub amount: f64,
    pub merchant: String,
    pub currency: String,
}

#[derive(Debug, Serialize, PartialEq)]
pub struct RiskScoreOutput {
    pub transaction_id: u64,
    pub risk_score: f64,
    pub risk_level: String,
    pub factors: Vec<String>,
}

pub fn calculate_risk(input: &TransactionInput) -> RiskScoreOutput {
    let mut score = 0.0;
    let mut factors = Vec::new();

    if input.amount > 1000.0 {
        score += 40.0;
        factors.push("high_amount".to_string());
    } else if input.amount > 500.0 {
        score += 20.0;
        factors.push("elevated_amount".to_string());
    }

    let merchant_lower = input.merchant.to_lowercase();
    let suspicious = ["crypto", "gambling", "wire", "offshore", "anonymous"];
    for keyword in suspicious {
        if merchant_lower.contains(keyword) {
            score += 30.0;
            factors.push(format!("suspicious_merchant:{}", keyword));
            break;
        }
    }

    if input.currency != "USD" {
        score += 10.0;
        factors.push("foreign_currency".to_string());
    }

    if input.user_id.starts_with("blocked") {
        score += 50.0;
        factors.push("blocked_user_prefix".to_string());
    }

    score = score.min(100.0);

    let risk_level = if score >= 60.0 {
        "high"
    } else if score >= 30.0 {
        "medium"
    } else {
        "low"
    };

    RiskScoreOutput {
        transaction_id: input.transaction_id,
        risk_score: score,
        risk_level: risk_level.to_string(),
        factors,
    }
}
