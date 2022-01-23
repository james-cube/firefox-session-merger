#!/usr/bin/env python3
import argparse
import json
try:
    import lz4.block as lz4
except ImportError:
    import lz4

def load_sessionstore_file(filename):
    with open(filename, 'rb') as json_data:
        if json_data.read(8) == b'mozLz40\0':
            return json.loads(lz4.decompress(json_data.read()))
        json_data.seek(0)
        return json.load(json_data)

def load_sessionstore_files(filenames):
    for filename in filenames:
        yield load_sessionstore_file(filename)

def extract_all_tabs(session):
    for window in session.get("windows"):
        for tab in window.get("tabs"):
            yield tab

def flatten_session(session):
    if len(session.get("windows")) > 1:
        main_window = session.get("windows")[0]
        main_window["tabs"] = list(extract_all_tabs(session))
        session["windows"] = [main_window]

def urls_from_session(session):
    for tab in extract_all_tabs(session):
        for entry in tab.get("entries"):
            yield entry.get("url")


def has_duplicate_in_session(session, tab):
    for url in urls_from_session(session):
        for entry in tab.get("entries"):
            if entry.get("url") == url:
                return True
    return False


def simple_merge_into(main_session, other_session):
    for window in other_session.get("windows"):
        main_session.get("windows").append(window)

def deep_merge_into(main_session, other_session):
    tabs = extract_all_tabs(other_session)
    for tab in tabs:
        if has_duplicate_in_session(main_session, tab) == False:
            main_session.get("windows")[0].get("tabs").append(tab)

def write_to_file(filename, output):
    with open(filename, "wb") as out:
        output = output.encode('utf-8')
        if filename.find(".jsonlz4") >= 0:
            out.write(b'mozLz40\0' + lz4.compress(output))
        else:
            out.write(output)

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-urls', action='store_true', help='Print urls from all windows in session')
    group.add_argument('--simple-merge', action='store_true', help='Put each session in another firefox window, without duplicate search')
    group.add_argument('--deep-merge', action='store_true', help='Create single firefox window from all sessions and remove duplicate tabs')
    parser.add_argument('--files', dest='files', help='List of files to process', nargs='+', required=True)
    parser.add_argument('--output', dest='output', help='Output file', required=True)
    args = parser.parse_args()

    if args.list_urls:
        sessions = list(load_sessionstore_files(args.files))
        with open(args.output, "w") as output:
            for session in sessions:
                for url in urls_from_session(session):
                    output.write(url + '\n')
                output.write('\n')

    if args.simple_merge or args.deep_merge:
        if len(args.files) > 1:
            sessions = list(load_sessionstore_files(args.files))
            main_session = sessions[0]
            if args.simple_merge:
                for other_session in sessions[1:]:
                    simple_merge_into(main_session, other_session)
                write_to_file(args.output, json.dumps(main_session, indent=4))
            elif args.deep_merge:
                flatten_session(main_session)
                for other_session in sessions[1:]:
                    deep_merge_into(main_session, other_session)
                write_to_file(args.output, json.dumps(main_session, indent=4))
        else:
            print("Not enough files for merge")

if __name__ == "__main__":
    main()
