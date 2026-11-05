# Contributing

## Changes

- Open a pull request against `main`. CI (`lint`, `test`) must be green; the ruleset on `main` requires both.
- Merging to `main` deploys to **staging** (`Deploy staging`). Staging is ours to break: no approval needed.

## Production

- Run `Deploy production` (`gh workflow run deploy-production.yml`). It deploys `main`.
- The `production` environment requires an approval from a release approver (Actions > the run > Review
  deployments). The deploy then runs the health check and updates the pinned **Production status** issue.

## Incidents

Speed matters more than ceremony. Admins can push a fix straight to `main` (the ruleset allows it), let it reach
staging, then run `Deploy production`. If the fix can't go to `main` right away, deploy your fix branch itself with
`gh workflow run deploy-production.yml --ref <your-branch>` and get it approved; open the pull request after. See
[docs/runbooks/hotfix.md](docs/runbooks/hotfix.md).
