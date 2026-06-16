//! B6 — Log level counting library.

use std::fs;

#[derive(Debug, Default, PartialEq, Eq)]
pub struct LogCounts {
    pub info: usize,
    pub warn: usize,
    pub error: usize,
}

pub fn count_log_levels(content: &str) -> LogCounts {
    let mut counts = LogCounts::default();
    for line in content.lines() {
        let upper = line.to_uppercase();
        if upper.contains("ERROR") {
            counts.error += 1;
        } else if upper.contains("WARN") {
            counts.warn += 1;
        } else if upper.contains("INFO") {
            counts.info += 1;
        }
    }
    counts
}

pub fn count_from_file(path: &str) -> Result<LogCounts, String> {
    let content = fs::read_to_string(path).map_err(|e| {
        if e.kind() == std::io::ErrorKind::NotFound {
            format!("File not found: {}", path)
        } else {
            format!("Failed to read file: {}", e)
        }
    })?;
    Ok(count_log_levels(&content))
}
