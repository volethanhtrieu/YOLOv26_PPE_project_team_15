# Contributing

Contributions should keep the project reproducible and make changes easy to
review. Start with the [architecture](docs/architecture.md) and
[setup guide](docs/QUICKSTART.md).

## Working on a change

1. Start from main_sub, the current integration branch. Preserve local changes
   before switching branches.
2. Create a focused feature/fix branch. Keep unrelated data, API and training
   changes in separate PRs when possible.
3. Name the affected runtime: review, Variant C, research Event Engine, data,
   or training. Shared filenames do not imply shared contracts.
4. Add a regression test and update the relevant guide when behaviour changes.
5. Run the checks below. Include the actual results and skipped cases in the PR.

## Required local checks

```sh
python scripts/check_docs.py
python ppe.py test -q
python bytetrack_ppe/test_ablation_v1.py
```

For review API changes, also run:

```sh
python bytetrack_ppe/test_api.py --allow-empty
python bytetrack_ppe/test_job_api_v3.py --allow-empty
python bytetrack_ppe/test_human_review_v3.py
```

For inference changes, add a short real-model check and review a representative
full-length video. State which video/checkpoint was used and whether it may be
shared. See [test tiers](docs/TESTING.md).

## Review checklist

- Explain the problem, solution and scope in the PR.
- Preserve person/head/helmet/vest semantics and test any schema changes.
- Document thresholds as operating settings; do not claim optimality without
  an evaluation.
- Separate detector, tracking, association and event metrics.
- Preserve AI status and human decisions separately.
- List dependencies and environment changes. Do not replace pinned packages
  with an unversioned install recipe in a module README.
- Keep data, credentials, signed links, weights and generated artifacts out of Git.
- Use reproducible commands with example paths, not personal machine paths.

## Documentation

The root README is the project overview. docs/ contains task-based guides.
Module references explain details and identify any historical workflows.
Update the maintained-file list in scripts/check_docs.py when adding a new
guide. The link checker validates local paths and Markdown heading anchors;
it does not check remote services or execute code examples.

## Reporting issues

Use the bug or feature template. Include a sanitized command, branch/commit,
configuration and relevant logs. Do not attach private footage by default.
For sensitive reports, follow [SECURITY.md](SECURITY.md).

Repository licensing still requires a team decision. Do not add a license or
change dataset/weight distribution terms as part of an unrelated code change.
