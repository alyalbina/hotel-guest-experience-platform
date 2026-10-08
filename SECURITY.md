# Security and data handling

Do not open a public issue containing credentials, real guest records or screenshots of private configuration.

## Rotate credentials from the uploaded original

1. **Telegram:** open the original bot in BotFather, revoke its API token and issue a new token. Revocation invalidates the old token; simply changing a local `.env` file does not.
2. **Google Cloud:** identify the service account from the private original JSON, disable/delete the exposed service-account key, and create a replacement only if Sheets export is needed. If Sheets is unnecessary, retire the key and remove unneeded sharing.
3. Review the original spreadsheet's sharing and service-account permissions. Remove broad access. Room/contact fields and IDs are data, even when they are not authentication secrets.
4. If the original secrets ever reached a repository, remove them from all relevant history and copies, then rotate them. A new clean commit or `.gitignore` does not make an old key safe.

No rotation was performed automatically: it requires the owner's BotFather/Cloud account. The public package contains neither old token nor Google private key.

## Current controls

Staff passwords use salted PBKDF2-SHA256. Sessions use random opaque tokens, stored hashed in SQLite, with eight-hour expiry and logout invalidation. Mutations require a CSRF token. Cookies are HttpOnly/SameSite Strict and Secure outside demo mode. Roles are checked on the server, including department boundaries. Ten sign-in attempts per client per 15 minutes limit guessing on a single instance. SQL values are parameterized; updates use version checking inside a write transaction.

Guest intake persists locally before confirming success and is deduplicated by source reference. HTML renders guest text as text; exports use RAW values and formula guards. The public demo uses only synthetic rows. `export-demo` regenerates data in an isolated temporary database; it never reads operational records. The publication gate flags prohibited files and common credential patterns, but cannot certify the absence of every possible secret.

## Deployment boundary

`DEMO_MODE=true` has intentionally public demo credentials. Use fictional information and keep the local server bound to `127.0.0.1`. The static preview exposes only synthetic operations and performs no server writes. For a private non-demo instance, use a fresh DB, `DEMO_MODE=false`, private staff accounts and HTTPS. Back up the SQLite file using its backup API, restrict filesystem access, and establish a retention/deletion process before accepting personal data.

The prototype does not verify hotel stays or guest identity, provide SSO/MFA, implement legal consent/retention requirements, or claim regulatory certification. The original extended guest form is optional and should remain off unless there is a justified need. Never use the emergency-assistance menu as an emergency channel.
