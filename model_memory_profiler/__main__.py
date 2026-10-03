from argparse import ArgumentParser, REMAINDER
import json

from .analysis import compare, summarize
from .io import read_jsonl, write_jsonl
from .runner import profile_command
from .sampler import sample_pid


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run")
    run.add_argument("--out", required=True)
    run.add_argument("--interval", type=float, default=.1)
    run.add_argument("command", nargs=REMAINDER)

    watch = sub.add_parser("watch")
    watch.add_argument("pid", type=int)
    watch.add_argument("--seconds", type=float, default=30)
    watch.add_argument("--interval", type=float, default=.1)
    watch.add_argument("--out", required=True)

    report = sub.add_parser("report")
    report.add_argument("path")

    comp = sub.add_parser("compare")
    comp.add_argument("left")
    comp.add_argument("right")

    args = parser.parse_args()

    if args.cmd == "run":
        command = args.command[1:] if args.command and args.command[0] == "--" else args.command
        rows, code = profile_command(command, args.interval)
        write_jsonl(args.out, rows)
        print(json.dumps({"returncode": code, **summarize(rows)}, indent=2))
    elif args.cmd == "watch":
        rows = sample_pid(args.pid, interval=args.interval, seconds=args.seconds)
        write_jsonl(args.out, rows)
        print(json.dumps(summarize(rows), indent=2))
    elif args.cmd == "report":
        print(json.dumps(summarize(read_jsonl(args.path)), indent=2))
    else:
        print(json.dumps(compare(read_jsonl(args.left), read_jsonl(args.right)), indent=2))


if __name__ == "__main__":
    main()
