# Runbook: production hotfix

1. Reproduce with the health check: `python -m scripts.smoke`.
2. Fix it, add a test that fails without the fix, run `python -m pytest -q`.
3. Ship it:
   - admins: push the fix straight to `main` (the pull request rule can be bypassed during an incident); `Deploy
     staging` ships it to staging; then run `gh workflow run deploy-production.yml`;
   - otherwise, or if the push to `main` doesn't go through: push your fix branch and run
     `gh workflow run deploy-production.yml --ref <your-branch>`.
4. The run waits for a release approver in the `production` environment; approve it under **Review deployments**.
5. Watch the pinned **Production status** issue turn green, comment on the incident issue and close it. Open the pull
   request for the after-the-fact review.
