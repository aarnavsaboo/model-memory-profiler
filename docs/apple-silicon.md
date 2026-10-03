# Apple Silicon notes

Process RSS is a useful repeatable measurement but it is not identical to total unified-memory pressure.

A local model runtime may use memory through frameworks and mappings that are not represented perfectly by one process RSS number. Child processes can also hold significant memory. The profiler therefore stores both root-process RSS and discovered child RSS, plus system-level virtual-memory snapshots when the operating-system tools are available.

For model comparisons, keep the machine, runtime version and background workload as stable as practical. The most useful results are relative curves collected under the same conditions.
