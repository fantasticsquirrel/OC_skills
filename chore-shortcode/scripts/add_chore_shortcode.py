#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
import sqlite3
from pathlib import Path

DB_DEFAULT = "/var/ralph-projects/chore_tracking/data/chore_tracking.db"

LINE_RE = re.compile(r'^\s*"(?P<name>.+?)"\s+(?P<reward>\.[0-9]+)\s+(?P<schedule>[a-z]{2}\d*)\s+(?P<completion>pc|sh)\s+(?P<assignment>sa|ro)\s+(?P<kids>[avw]{1,3})(?P<rest>.*)$', re.IGNORECASE)


def reward_to_cents(token: str) -> int:
    s = token.strip().lstrip('.')
    if not s:
        raise ValueError("invalid reward token")
    if len(s) == 1:
        return int(s) * 10
    if len(s) == 2:
        return int(s)
    # tolerate .150 etc by scaling to cents
    val = float("0." + s)
    return int(round(val * 100))


def parse_schedule(token: str):
    t = token.lower()
    if t == 'sn':
        return 'NONE', None, None
    if t == 'so':
        return 'ONCE', None, None
    m = re.fullmatch(r'(ed|ew|em|ad|aw)(\d+)', t)
    if not m:
        raise ValueError(f"invalid schedule token: {token}")
    code, n = m.group(1), int(m.group(2))
    if code == 'ed':
        return 'EVERY', n, 'DAY'
    if code == 'ew':
        return 'EVERY', n, 'WEEK'
    if code == 'em':
        return 'EVERY', n, 'MONTH'
    if code == 'ad':
        return 'AFTER_COMPLETION', n, 'DAY'
    return 'AFTER_COMPLETION', n, 'WEEK'


def parse_line(line: str):
    m = LINE_RE.match(line.strip())
    if not m:
        raise ValueError(f"could not parse line: {line}")

    name = m.group('name').strip()
    reward_cents = reward_to_cents(m.group('reward'))
    schedule_mode, schedule_interval, schedule_unit = parse_schedule(m.group('schedule'))
    completion_mode = 'PER_CHILD' if m.group('completion').lower() == 'pc' else 'SHARED'
    assignment_mode = 'ROTATING' if m.group('assignment').lower() == 'ro' else 'STATIC'
    kids = list(dict.fromkeys(ch.upper() for ch in m.group('kids')))

    timeout_days = None
    expires_at = None
    rest = m.group('rest') or ''
    for tok in rest.split():
        tt = tok.lower()
        if re.fullmatch(r't\d+', tt):
            timeout_days = int(tt[1:])
        elif re.fullmatch(r'x\d{4}-\d{2}-\d{2}', tt):
            expires_at = tt[1:]

    return {
        'name': name,
        'reward_cents': reward_cents,
        'schedule_mode': schedule_mode,
        'schedule_interval': schedule_interval,
        'schedule_unit': schedule_unit,
        'completion_mode': completion_mode,
        'assignment_mode': assignment_mode,
        'kids': kids,
        'timeout_days': timeout_days,
        'expires_at': expires_at,
    }


def ensure_child(cur: sqlite3.Cursor, household_id: int, name: str) -> int:
    cur.execute(
        'select id from children where household_id=? and name=? and active=1 order by id limit 1',
        (household_id, name),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        'insert into children (household_id,name,active,created_at) values (?,?,1,?)',
        (household_id, name, dt.datetime.now(dt.UTC).isoformat(sep=' ')),
    )
    return cur.lastrowid


def insert_chore(cur: sqlite3.Cursor, household_id: int, payload: dict) -> int:
    cur.execute(
        '''
        insert into chores (
          household_id,name,reward_cents,start_date,expires_at,timeout_days,
          schedule_mode,schedule_interval,schedule_unit,completion_mode,assignment_mode,archived_at,created_at
        ) values (?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''',
        (
            household_id,
            payload['name'],
            payload['reward_cents'],
            dt.date.today().isoformat(),
            payload['expires_at'],
            payload['timeout_days'],
            payload['schedule_mode'],
            payload['schedule_interval'],
            payload['schedule_unit'],
            payload['completion_mode'],
            payload['assignment_mode'],
            None,
            dt.datetime.now(dt.UTC).isoformat(sep=' '),
        ),
    )
    chore_id = cur.lastrowid

    kid_ids = [ensure_child(cur, household_id, k) for k in payload['kids']]
    for cid in kid_ids:
        cur.execute('insert into chore_allowed_children (chore_id,child_id) values (?,?)', (chore_id, cid))

    if payload['assignment_mode'] == 'ROTATING':
        for pos, cid in enumerate(kid_ids):
            cur.execute(
                'insert into chore_rotation_members (chore_id,child_id,position) values (?,?,?)',
                (chore_id, cid, pos),
            )
        cur.execute(
            'insert into chore_rotation_state (chore_id,current_position,last_occurrence_date) values (?,?,?)',
            (chore_id, 0, None),
        )

    return chore_id


def read_lines(args) -> list[str]:
    lines: list[str] = []
    lines.extend(args.line or [])
    if args.file:
        text = Path(args.file).read_text(encoding='utf-8')
        for raw in text.splitlines():
            raw = raw.strip()
            if raw:
                lines.append(raw)
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description='Add chore entries from shortcode lines')
    ap.add_argument('--db', default=DB_DEFAULT)
    ap.add_argument('--household', type=int, required=True)
    ap.add_argument('--line', action='append', help='single shortcode line; repeatable')
    ap.add_argument('--file', help='file with one shortcode entry per line')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    lines = read_lines(args)
    if not lines:
        raise SystemExit('No lines provided (use --line or --file).')

    parsed = [parse_line(l) for l in lines]

    if args.dry_run:
        for p in parsed:
            print(p)
        return 0

    con = sqlite3.connect(args.db)
    cur = con.cursor()
    created = []
    for p in parsed:
        cid = insert_chore(cur, args.household, p)
        created.append({'id': cid, 'name': p['name']})
    con.commit()

    for item in created:
        print(f"created chore {item['id']}: {item['name']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
