# Workflow integration

The profiler can be used beside any local inference experiment that launches a process.

A typical batch workflow writes:

- a job record from the experiment planner;
- a latency/result record from the model runner;
- a memory timeline from this profiler.

Join them with a run ID at the orchestration layer. Keeping the profiler independent means the same timeline format can be used for MLX, llama.cpp, custom Python processes or local services.
