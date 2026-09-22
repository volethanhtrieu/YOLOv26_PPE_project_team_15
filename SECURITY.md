# Security and safe operation

## Intended environment

This branch provides local development/research applications. It has not been
audited for public deployment, multi-tenant isolation, or safety-critical use.
The review development server enables Flask debug mode and binds to loopback.
Do not expose it through a public tunnel or open network interface.

Before deployment, assess authentication, authorization, upload limits, path
handling, retention, secret management, dependency vulnerabilities and audit logs.
These are review requirements, not claims that controls already exist.

## Data and artifacts

- Load only checkpoints from trusted sources.
- Do not commit credentials, .env files, access tokens, databases or runtime logs.
- Obtain permission before uploading video, evidence or metadata to W&B.
- Review licenses separately for source code, datasets and weights.
- Keep AI event status separate from human review decisions.

## Reporting a vulnerability

Do not put secrets or exploitable private details into a public issue.
If GitHub private vulnerability reporting is enabled, use the repository Security
tab. Otherwise contact a maintainer privately through an established channel.
No dedicated security mailbox or response-time commitment has been set up.
