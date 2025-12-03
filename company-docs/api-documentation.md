# AgentForce Infotech Internal API Documentation

## Authentication

All API requests require authentication using JWT Bearer tokens:
```
Authorization: Bearer <your-jwt-token>
```

Get your API token:
1. Login to AgentForce Developer Portal: https://devportal.agentforce.com
2. Go to "API Tokens" section
3. Generate new token (expires in 90 days)
4. Store securely (use 1Password)

## Base URLs

- **Development**: https://api-dev.agentforce.com/v2
- **Staging**: https://api-staging.agentforce.com/v2
- **Production**: https://api.agentforce.com/v2

Note: We're on API version 2. Version 1 is deprecated and will be removed Q2 2025.

## Common Endpoints

### User Management
- `GET /v2/users` - List all users (paginated, 50 per page)
- `GET /v2/users/{id}` - Get user details by ID
- `POST /v2/users` - Create new user (requires admin role)
- `PUT /v2/users/{id}` - Update user (requires user or admin role)
- `DELETE /v2/users/{id}` - Deactivate user (requires admin role)

### Projects (AgentForce Projects)
- `GET /v2/projects` - List projects (supports filtering by status, team)
- `GET /v2/projects/{id}` - Get project details
- `POST /v2/projects` - Create project (requires project_manager role)
- `PUT /v2/projects/{id}` - Update project
- `DELETE /v2/projects/{id}` - Archive project

### Tasks (Jira Integration)
- `GET /v2/tasks` - List tasks (supports filtering: status, assignee, project)
- `GET /v2/tasks/{id}` - Get task details
- `POST /v2/tasks` - Create task
- `PUT /v2/tasks/{id}/status` - Update task status
- `GET /v2/tasks/{id}/comments` - Get task comments

### Time Tracking
- `POST /v2/timesheets` - Log time entry
- `GET /v2/timesheets` - Get time entries (filter by date range, project)

## Rate Limits

- **Standard users**: 200 requests per minute, 5000 requests per hour
- **API service accounts**: 500 requests per minute, 20000 requests per hour
- Contact API team (api-team@agentforce.com) for higher limits

Rate limit headers included in response:
- `X-RateLimit-Limit`: Total allowed requests
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset time (Unix timestamp)

## Error Codes

- **400**: Bad Request (validation error)
- **401**: Unauthorized (invalid or missing token)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **429**: Rate Limit Exceeded
- **500**: Internal Server Error
- **503**: Service Unavailable (maintenance mode)

Error response format:
```json
{
  "error": {
    "code": 400,
    "message": "Validation failed",
    "details": ["field_name: error description"]
  }
}
```

## API Documentation

- **Interactive Swagger UI**: https://api.agentforce.com/v2/docs
- **Postman Collection**: Available in GitLab repo `agentforce/postman-collections`
- **API Changelog**: https://docs.agentforce.com/api/changelog

For API questions, contact API team: api-team@agentforce.com or #agentforce-api-support Slack channel.
