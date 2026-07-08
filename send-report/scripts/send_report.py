#!/usr/bin/env python3
"""Dispatch an accessibility review report to the Apps Script email endpoint.

Replicates the exact email-send path the a11y-review-server uses: it POSTs a
JSON payload of {file_name, email, review} to the Apps Script web app URL and
prints the response body.

Secrets / configuration are read from the environment:
  APPS_SCRIPT_URL  (required) - the Apps Script web app URL that sends the email
  APPSCRIPT_SECRET (optional) - if set, sent as the X-Appscript-Secret header

Report generation and server logic are intentionally NOT part of this script;
the email body (report) and recipient are passed in.
"""
import argparse
import json
import os
import sys
import urllib.request


def send_report(designer_email, report, file_name):
    try:
        apps_script_url = os.environ["APPS_SCRIPT_URL"]
    except KeyError:
        sys.exit("APPS_SCRIPT_URL is not set in the environment.")

    payload = json.dumps({
        "file_name": file_name,
        "email": designer_email,
        "review": report,
    }).encode()

    headers = {"Content-Type": "application/json"}
    appscript_secret = os.environ.get("APPSCRIPT_SECRET")
    if appscript_secret:
        headers["X-Appscript-Secret"] = appscript_secret

    req = urllib.request.Request(apps_script_url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode()
    print(f"Review dispatched for {file_name} to {designer_email} "
          f"- Apps Script response: {body}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--designer-email", required=True,
                        help="Recipient email address for the report.")
    parser.add_argument("--file-name", default="Accessibility Design Review",
                        help="Human-readable name of the reviewed file "
                             "(used in the email subject).")
    parser.add_argument("--report",
                        help="The report body (HTML fragment). If omitted, "
                             "the report is read from stdin.")
    args = parser.parse_args()

    report = args.report if args.report is not None else sys.stdin.read()
    if not report.strip():
        sys.exit("No report content provided (pass --report or pipe via stdin).")

    send_report(args.designer_email, report, args.file_name)


if __name__ == "__main__":
    main()
