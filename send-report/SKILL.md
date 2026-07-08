---
name: send-report
description: Sends an accessibility review report to a designer by email, replicating the exact Apps Script email-dispatch path used by the a11y-review-server. Use this skill when the user invokes /send-report, or asks to email/dispatch/send an already-generated a11y review report to a recipient. Takes a designer_email and a report; does NOT generate the report or run any review.
---

# Send Report

Dispatch an already-generated accessibility review report to a designer by
email. This mirrors the exact email-send mechanics of the `a11y-review-server`
(`server.py`, `run_review`): it POSTs a JSON payload to an Apps Script web app
URL, which sends the email.

This skill does **not** generate reports or run any review. It assumes the
report body and recipient are supplied to it.

## Inputs

- `designer_email` (required) - the recipient's email address.
- `report` (required) - the report body. The server sends the report as the
  body of an HTML email, so this should be an HTML fragment (no `<html>`,
  `<head>`, or `<body>` wrapper), matching what the server dispatches.
- `file_name` (optional) - a human-readable name of the reviewed file, used in
  the email subject. Defaults to `Accessibility Design Review`. In the server
  this is derived from the Figma URL; since report generation is out of scope
  here, pass it explicitly if you have it.

## Steps

1. Confirm you have a `designer_email` and a `report`. If either is missing,
   ask the user for it.

2. Confirm `APPS_SCRIPT_URL` is set in the environment. If it is not, tell the
   user it must be populated before the report can be sent.

3. Run the bundled script, passing the report on stdin (so large HTML bodies
   don't hit shell argument limits):

   ```bash
   printf '%s' "$REPORT_HTML" | \
     python3 .claude/skills/send-report/scripts/send_report.py \
       --designer-email "designer@mozilla.com" \
       --file-name "Some Design File"
   ```

   Alternatively pass the report inline with `--report "<h2>...</h2>"`.

4. Report the Apps Script response back to the user. A successful dispatch
   prints `Review dispatched for <file_name> to <email> - Apps Script
   response: <body>`.

## Payload contract

The script POSTs the following JSON to `APPS_SCRIPT_URL` with
`Content-Type: application/json` (30-second timeout), identical to the server:

```json
{
  "file_name": "<file_name>",
  "email": "<designer_email>",
  "review": "<report>"
}
```

## Secrets / configuration

- `APPS_SCRIPT_URL` (required) - the Apps Script web app URL that sends the
  email. Read from the environment; never hard-coded.
- `APPSCRIPT_SECRET` (optional) - if set, it is sent as an `X-Appscript-Secret`
  header. The current server does **not** send any secret to the Apps Script
  endpoint, so by default (unset) the behavior is byte-for-byte identical to
  the server. Only populate this if the Apps Script endpoint is later updated
  to require it.
