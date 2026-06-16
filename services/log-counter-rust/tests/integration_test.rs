use log_counter::{count_from_file, count_log_levels};

#[test]
fn counts_all_levels() {
    let content = "INFO: started\nWARN: low memory\nERROR: disk full\nINFO: retrying\nERROR: timeout";
    let counts = count_log_levels(content);
    assert_eq!(counts.info, 2);
    assert_eq!(counts.warn, 1);
    assert_eq!(counts.error, 2);
}

#[test]
fn empty_file_returns_zeros() {
    let counts = count_log_levels("");
    assert_eq!(counts.info, 0);
    assert_eq!(counts.warn, 0);
    assert_eq!(counts.error, 0);
}

#[test]
fn missing_file_returns_error() {
    let result = count_from_file("/nonexistent/path/to/file.log");
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("File not found"));
}

#[test]
fn reads_sample_file() {
    let result = count_from_file("sample.log");
    assert!(result.is_ok());
    let counts = result.unwrap();
    assert_eq!(counts.info, 3);
    assert_eq!(counts.warn, 2);
    assert_eq!(counts.error, 2);
}
