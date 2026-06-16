//! B6 — Rust CLI that counts INFO/WARN/ERROR log levels in a file.

use log_counter::count_from_file;
use std::env;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: log-counter <file-path>");
        process::exit(1);
    }

    let path = &args[1];
    match count_from_file(path) {
        Ok(counts) => {
            println!("INFO:  {}", counts.info);
            println!("WARN:  {}", counts.warn);
            println!("ERROR: {}", counts.error);
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            process::exit(1);
        }
    }
}
