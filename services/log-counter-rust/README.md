# B6 — Rust Log Counter CLI

CLI that counts INFO, WARN, and ERROR log levels in a file.

## Build & Run

```bash
cargo build
cargo run -- sample.log
```

## Test

```bash
cargo test
```

## Usage

```bash
cargo run -- <file-path>
```

Handles missing files gracefully with a clear error message.
