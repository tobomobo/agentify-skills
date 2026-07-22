# Agent guide

## Quality gate

Run `npm run ci` before every pull request.

## API security

Verify request signatures before parsing untrusted payloads.

## Common gotcha

Never reuse a request nonce. A production replay incident established this
rule; the repository does not prove that the sharp edge is gone.
