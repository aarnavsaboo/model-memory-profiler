# model-memory-profiler

Process and system-memory profiling utilities for local language-model workloads.

Local inference often becomes a memory-planning problem before it becomes a raw compute problem. Model weights, runtime allocations, prompt processing, key-value cache growth and concurrent jobs all compete for the same machine memory. This repository records those changes as a timeline instead of relying on a single value from Activity Monitor.

The profiler is deliberately lightweight and uses operating-system tools available on macOS. It can wrap an arbitrary local inference command or attach to an existing process.

## Measurements

- process RSS over time
- peak RSS
- median steady-state RSS
- child-process RSS where available
- system virtual-memory page counts from `vm_stat`
- swap usage snapshots from `sysctl vm.swapusage`
- elapsed process time
- process exit code
- command metadata
- sampling interval
- optional phase markers written by the workload
- memory delta between selected phases

## Example

Profile an arbitrary local model command:

```bash
python -m model_memory_profiler run \
  --out runs/model.jsonl \
  -- python -m mlx_lm.generate \
     --model path/to/local-model \
     --prompt "Summarize this document." \
     --max-tokens 256
```

Attach to a running process:

```bash
python -m model_memory_profiler watch 12345 --seconds 30 --out runs/watch.jsonl
```

Summarize a timeline:

```bash
python -m model_memory_profiler report runs/model.jsonl
```

## Why a timeline?

A model can briefly allocate substantially more memory during loading than it needs while generating. Long prompts can grow memory after the model is already warm. A batch workflow may have a very different steady-state profile from one isolated request.

A timeline makes those phases visible and gives experiment runners something machine-readable to join with latency and quality results.

## Workflow integration

The JSONL format is intentionally simple. Each sample includes a monotonic timestamp, process RSS and any available system-memory counters. A higher-level benchmark can launch the profiler beside a model run, then join the records by run ID.

```text
experiment runner
   |
   +---- local model process
   |
   +---- memory profiler
              |
              v
        memory timeline
              |
              v
          summary row
              |
        +-----+------+
        |            |
     latency      task score
```

## Repository layout

- `process.py` — process RSS and child discovery
- `system.py` — macOS memory snapshots
- `sampler.py` — timeline collection
- `runner.py` — command wrapping
- `phases.py` — optional phase records
- `analysis.py` — peak, median and phase summaries
- `io.py` — JSONL records
- `docs/` — measurement caveats and workflow notes
- `tests/` — parser and summary tests

Process RSS is not a complete accounting of Apple unified memory. The project treats it as a repeatable observable for relative experiments on the same machine.

Maintained by **Aarnav Saboo**.
