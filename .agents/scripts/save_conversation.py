#!/usr/bin/env python3
"""
Workspace Stop Hook: Saves current conversation ID and stop metadata
so the overnight sidecar watcher can resume the same conversation.
"""

import json
import sys
from pathlib import Path


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print("{}", file=sys.stdout)
            return

        payload = json.loads(raw_input)

        # Resolve runtime directory relative to this script: .agents/runtime
        script_dir = Path(__file__).resolve().parent
        runtime_dir = script_dir.parent / "runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)

        conv_id = payload.get("conversationId")
        if conv_id and isinstance(conv_id, str) and conv_id.strip():
            conv_file = runtime_dir / "conversation_id.txt"
            conv_file.write_text(conv_id.strip(), encoding="utf-8")

        # Save complete stop metadata
        stop_file = runtime_dir / "last_stop.json"
        stop_file.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    except Exception as e:
        print(f"[save_conversation] Error saving hook data: {e}", file=sys.stderr)
    finally:
        # Stop hook output contract: {} allows normal termination
        print("{}", file=sys.stdout)


if __name__ == "__main__":
    main()
