use fraud_scorer::{calculate_risk, TransactionInput};

#[test]
fn low_risk_small_amount() {
    let input = TransactionInput {
        transaction_id: 1,
        user_id: "user-1".to_string(),
        amount: 25.0,
        merchant: "Coffee Shop".to_string(),
        currency: "USD".to_string(),
    };
    let result = calculate_risk(&input);
    assert_eq!(result.risk_level, "low");
    assert!(result.risk_score < 30.0);
}

#[test]
fn high_risk_large_suspicious_transaction() {
    let input = TransactionInput {
        transaction_id: 2,
        user_id: "user-2".to_string(),
        amount: 5000.0,
        merchant: "Crypto Exchange".to_string(),
        currency: "EUR".to_string(),
    };
    let result = calculate_risk(&input);
    assert_eq!(result.risk_level, "high");
    assert!(result.risk_score >= 60.0);
    assert!(result.factors.iter().any(|f| f.contains("high_amount")));
}

#[test]
fn medium_risk_elevated_amount() {
    let input = TransactionInput {
        transaction_id: 3,
        user_id: "user-3".to_string(),
        amount: 750.0,
        merchant: "Electronics".to_string(),
        currency: "USD".to_string(),
    };
    let result = calculate_risk(&input);
    assert_eq!(result.risk_level, "medium");
}

#[test]
fn blocked_user_prefix_triggers_high_risk() {
    let input = TransactionInput {
        transaction_id: 4,
        user_id: "blocked-user-99".to_string(),
        amount: 10.0,
        merchant: "Store".to_string(),
        currency: "USD".to_string(),
    };
    let result = calculate_risk(&input);
    assert!(result.risk_score >= 50.0);
    assert!(result.factors.contains(&"blocked_user_prefix".to_string()));
}
