FROM rust:1.83-slim AS scorer-build
WORKDIR /scorer
COPY scorer/Cargo.toml scorer/Cargo.toml
COPY scorer/src/ scorer/src/
RUN cargo build --release

FROM node:22-slim
WORKDIR /app
COPY worker/package.json .
COPY worker/worker.js .
COPY --from=scorer-build /scorer/target/release/fraud-scorer /app/scorer/fraud-scorer
CMD ["node", "worker.js"]
