# Contributing

1. Use a feature branch and a reviewed PR.
2. Never commit datasets, weights, generated videos or credentials.
3. Add regression tests and run python ppe.py test -q.
4. Run affected API/video smoke tests and record external fixtures.
5. Document changes to thresholds and event policies.

Do not claim accuracy from smoke tests. Review and research runtimes have
different contracts. Use the launcher to avoid importing the wrong app.py.
