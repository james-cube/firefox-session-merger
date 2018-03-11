[![Build Status](https://travis-ci.org/james-cube/firefox-session-merger.svg?branch=master)](https://travis-ci.org/james-cube/firefox-session-merger)

# firefox-session-merger

Tool for merging firefox session files. Designed for people who don't want to use cloud based tools like firefox sync, want to version control their session files or have any other reason to do this locally.

## Usage

### How firefox stores session? (up to date with Firefox 54)

NOTE: In recent versions of firefox `sessionsstore.js` files are compressed into `sessionstore.jsonlz4`. Automatic compression/decompression is not curently supported by this tool.

After setting in `about:preferences` under `When Firefox starts` option `Show your windows and tabs from last time` and closing firefox, `sessionstore.js` file is created in profile directory. In linux it should be typically in `~/.mozilla/firefox/{profile}/`. Alternatively `~/.mozilla/firefox/{profile}/sessionstore-backups/` have few last and recovery session files. This file have information about all windows, tabs, recently closed tabs and can be ported between computers and firefox instances using simple copy-paste. 

### How to use the tool?

Close all firefox instances. Collect your `sessionstore.js` files as described above, copy them to tool directory and performe merge. Copy created file to your firefox profile replacing previous `sessionstore.js`. Start firefox, it should display tabs from all sessions you merged. 

#### Listing urls

Creating simple list of urls for those who don't want to read through json or open firefox session.

`python3 firefox_session_merger.py --list-urls --files sessionstore.js --output output.txt`

#### Simple merge

Merge two or more sessions into one. Each one will be loaded by firefox into separate window with all of them opened after starting firefox.

`python3 firefox_session_merger.py --simple-merge --files sessionstore_laptop.js sessionstore_desktop.js --output sessionstore_merged.js`

#### Deep merge

Merge two or more sessions into one. All tabs will be loaded into single window and duplicates wil be removed.

`python3 firefox_session_merger.py --deep-merge --files sessionstore_laptop.js sessionstore_desktop.js --output sessionstore_merged.js`

### All program arguments

```
usage: firefox_session_merger.py [-h]
                                 (--list-urls | --simple-merge | --deep-merge)
                                 --files FILES [FILES ...] --output OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  --list-urls           Print urls from all windows in session
  --simple-merge        Put each session in another firefox window, without
                        duplicate search
  --deep-merge          Create single firefox window from all sessions and
                        remove duplicate tabs
  --files FILES [FILES ...]
                        List of files to process
  --output OUTPUT       Output file
```
