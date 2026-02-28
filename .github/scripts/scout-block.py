#!/usr/bin/env python3
import json, os, re, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_name = data.get('toolName', '')
if tool_name not in ('bash', 'glob', 'grep', 'view', 'edit', 'create'):
    sys.exit(0)

ignore_file = '.copilotignore'
if not os.path.isfile(ignore_file):
    sys.exit(0)

tool_args = data.get('toolArgs', {})
if isinstance(tool_args, str):
    try:
        tool_args = json.loads(tool_args)
    except Exception:
        args_str = tool_args
else:
    args_str = None

if isinstance(tool_args, dict):
    args_str = ' '.join(str(v) for v in tool_args.values())
elif args_str is None:
    args_str = str(tool_args)

block_patterns = []
allow_patterns = []
with open(ignore_file) as f:
    for line in f:
        pattern = line.rstrip(chr(10)).strip()
        if not pattern or pattern.startswith('#'):
            continue
        if pattern.startswith('!'):
            allow_patterns.append(pattern[1:].rstrip('/'))
        else:
            block_patterns.append(pattern.rstrip('/'))

def matches_path_segment(pattern, text):
    escaped = re.escape(pattern)
    return bool(re.search(r'(?:^|[\s/\\])' + escaped + r'(?:[\s/\\]|$)', text))

for pattern in allow_patterns:
    if pattern in args_str:
        sys.exit(0)

for pattern in block_patterns:
    if pattern.startswith('*.'):
        if pattern[1:] in args_str:
            print(json.dumps({'permissionDecision': 'deny', 'permissionDecisionReason': f'Blocked path: {pattern} (see .copilotignore)'}))
            sys.exit(0)
    elif matches_path_segment(pattern, args_str):
        print(json.dumps({'permissionDecision': 'deny', 'permissionDecisionReason': f'Blocked path: {pattern} (see .copilotignore)'}))
        sys.exit(0)
