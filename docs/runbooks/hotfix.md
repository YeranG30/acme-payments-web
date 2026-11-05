# Runbook: production hotfix

1. Reproduce with the health check: `python -m scripts.smoke`.
2. Fix it, add a test that fails without the fix, run `python -m pytest -q`.
3. Push the fix straight to `main` (admins may bypass the pull request rule during an incident). `Deploy staging`
   ships it to staging.
4. Run `gh workflow run deploy-production.yml`. The run waits for a release approver in the `production`
   environment; approve it under **Review deployments**.
5. Watch the pinned **Production status** issue turn green, comment on the incident issue and close it.
