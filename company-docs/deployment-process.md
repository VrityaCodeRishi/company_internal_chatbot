# AgentForce Infotech Deployment Process

## Staging Deployment (GitLab CI/CD)

1. Create a feature branch from `main`:
   `git checkout -b feature/PROJ-123-add-user-authentication`

2. Make your changes and commit with descriptive messages following our convention:
   `git commit -m "PROJ-123: Add OAuth2 authentication for user login"`

3. Push to GitLab and create a Merge Request (MR):
   - Target branch: `main`
   - Assign reviewers: At least one from your team
   - Link Jira ticket in MR description

4. Get code review approval from:
   - At least one team member
   - Tech Lead (Vikram Singh) for critical changes

5. Merge to `main` branch (triggers automatic staging deployment via GitLab CI/CD)
   - Pipeline automatically builds, tests, and deploys to staging

6. Verify deployment:
   - Check staging URL: https://staging.agentforce.com
   - Run smoke tests: Postman collection in `tests/smoke-tests/`
   - Check Grafana dashboards for errors: https://grafana.agentforce.internal

## Production Deployment

1. Ensure all tests pass in staging for at least 24 hours
2. Create a release branch: `git checkout -b release/v2.4.1`
3. Update version numbers:
   - `package.json` (frontend): `"version": "2.4.1"`
   - `setup.py` (backend): `version="2.4.1"`
   - Update `CHANGELOG.md` with release notes
4. Create MR to `main` with release notes and get approval from Product Owner
5. After merge, tag the release:
   `git tag -a v2.4.1 -m "Release v2.4.1: User authentication and bug fixes"`
   `git push origin v2.4.1`
6. This triggers production deployment pipeline (requires manual approval)
7. Monitor deployment in GitLab CI/CD: https://gitlab.agentforce.internal/{project}/-/pipelines
8. Verify production:
   - Production URL: https://app.agentforce.com
   - Check health endpoints: https://app.agentforce.com/health
   - Monitor Grafana for 15 minutes post-deployment

## Rollback Procedure

If deployment fails or issues are detected:

1. Go to GitLab CI/CD pipeline: https://gitlab.agentforce.internal/{project}/-/pipelines
2. Find the last successful production deployment
3. Click "Rollback" button (if available) OR manually deploy previous image tag
4. Notify team in #agentforce-deployments Slack channel
5. Create incident ticket in Jira for post-mortem

Emergency rollback: Contact on-call DevOps engineer (check PagerDuty schedule) or Anjali Mehta (anjali.mehta@agentforce.com, ext 2056).

## Deployment Windows

- Staging: Anytime (automated)
- Production: Tuesday-Thursday, 2 PM - 4 PM IST (avoid Monday and Friday)
- Hotfixes: Can be deployed outside window with Tech Lead approval
