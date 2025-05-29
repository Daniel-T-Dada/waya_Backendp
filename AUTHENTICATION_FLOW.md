# Waya Backend Authentication Flow

## Overview

The Waya Backend uses a comprehensive authentication system built on Django REST Framework with JWT tokens, email verification, and role-based access control.

## Complete Authentication Flow

### 1. User Registration (`POST /users/register`)

**Step 1: Initial Registration**
```json
POST /users/register
Content-Type: application/json

{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "SecurePassword123",
    "password2": "SecurePassword123",
    "role": "parent",
    "terms_accepted": true
}
```

**Response (201 Created):**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "parent",
    "is_verified": false,
    "date_joined": "2024-01-15T10:30:00Z"
}
```

**What happens internally:**
1. User account is created with `is_verified=false`
2. Verification email is sent to the user's email address
3. User cannot access protected endpoints until verified

### 2. Email Verification (`POST /users/verify-email`)

**Step 2: Email Verification**
```json
POST /users/verify-email
Content-Type: application/json

{
    "key": "verification_token_from_email"
}
```

**Response (200 OK):**
```json
{
    "detail": "Email successfully verified"
}
```

**What happens internally:**
1. User's `is_verified` field is set to `true`
2. User can now access protected endpoints after login

### 3. User Login (`POST /users/login`)

**Step 3: Authentication**
```json
POST /users/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "SecurePassword123"
}
```

**Response (200 OK):**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "John Doe",
    "email": "user@example.com",
    "avatar": null,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM5NTUyODAwLCJpYXQiOjE2Mzk1NTA5MDAsImp0aSI6IjEyMzQ1NjciLCJ1c2VyX2lkIjoiMTIzZTQ1NjctZTg5Yi0xMmQzLWE0NTYtNDI2NjE0MTc0MDAwIn0.example_signature",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzOTYzNzMwMCwiaWF0IjoxNjM5NTUwOTAwLCJqdGkiOiI3ODkwMTIzNCIsInVzZXJfaWQiOiIxMjNlNDU2Ny1lODliLTEyZDMtYTQ1Ni00MjY2MTQxNzQwMDAifQ.example_refresh_signature"
}
```

### 4. Protected API Access

**Step 4: Using JWT Token for API Calls**
```http
GET /children/list
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Token Management

### Token Lifetimes
- **Access Token**: 30 minutes
- **Refresh Token**: 1 day
- **Refresh Token Rotation**: Enabled (new refresh token on each refresh)

### Token Refresh (`POST /users/token/refresh`)

```json
POST /users/token/refresh
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
    "access": "new_access_token",
    "refresh": "new_refresh_token"
}
```

## User Roles & Permissions

### Available Roles
1. **Parent**: Full access to family management features
2. **Child**: Limited access to age-appropriate features

### Role-Based Access Control
- Parents can create/manage children profiles
- Parents can assign/manage tasks
- Children can view assigned tasks and update status
- Family wallet access varies by role

## Password Management

### Password Reset Flow

**Step 1: Request Password Reset**
```json
POST /users/password/reset/
Content-Type: application/json

{
    "email": "user@example.com"
}
```

**Step 2: Confirm Password Reset**
```json
POST /users/password/reset/confirm/
Content-Type: application/json

{
    "token": "reset_token_from_email",
    "password": "NewSecurePassword123"
}
```

### Password Change (Authenticated Users)
```json
POST /users/password/change/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "old_password": "CurrentPassword123",
    "new_password": "NewPassword123"
}
```

## Social Authentication

### Google OAuth Integration
```json
POST /users/google/
Content-Type: application/json

{
    "access_token": "google_oauth_access_token"
}
```

### Facebook OAuth Integration
```json
POST /users/facebook/
Content-Type: application/json

{
    "access_token": "facebook_oauth_access_token"
}
```

## Security Features

### 1. Email Verification
- Mandatory email verification for new accounts
- Users cannot access protected resources until verified

### 2. JWT Security
- Secure token generation with rotation
- Blacklisting of old tokens on refresh
- Short access token lifetime (30 minutes)

### 3. Password Validation
- Minimum length requirements
- Common password detection
- User attribute similarity checks

### 4. Rate Limiting
- Protection against brute force attacks
- API endpoint throttling

## API Documentation Access

### Swagger UI
- **URL**: `http://127.0.0.1:8000/api/docs/`
- **Features**: Interactive API testing, authentication support

### ReDoc
- **URL**: `http://127.0.0.1:8000/api/redoc/`
- **Features**: Clean documentation layout

### OpenAPI Schema
- **URL**: `http://127.0.0.1:8000/api/schema/`
- **Format**: JSON schema for API clients

## Error Handling

### Common Authentication Errors

**401 Unauthorized**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
```json
{
    "detail": "You do not have permission to perform this action."
}
```

**400 Bad Request (Registration)**
```json
{
    "email": ["A user with this email already exists."],
    "password": ["This password is too common."]
}
```

## Frontend Integration Guidelines

### 1. Token Storage
- Store access token in memory (not localStorage for security)
- Store refresh token in httpOnly cookie or secure storage
- Implement automatic token refresh logic

### 2. API Client Setup
```javascript
// Example API client setup
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Content-Type': 'application/json',
    }
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
    const token = getAccessToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle token refresh on 401
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            const newToken = await refreshToken();
            if (newToken) {
                error.config.headers.Authorization = `Bearer ${newToken}`;
                return apiClient.request(error.config);
            }
        }
        return Promise.reject(error);
    }
);
```

### 3. User State Management
```javascript
// Example user state structure
const userState = {
    isAuthenticated: boolean,
    user: {
        id: string,
        email: string,
        full_name: string,
        role: 'parent' | 'child',
        avatar: string | null,
        is_verified: boolean
    },
    tokens: {
        access: string,
        refresh: string
    }
};
```

## Testing the Authentication Flow

### 1. Test Registration
```bash
curl -X POST http://127.0.0.1:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "TestPassword123",
    "password2": "TestPassword123",
    "role": "parent",
    "terms_accepted": true
  }'
```

### 2. Test Login
```bash
curl -X POST http://127.0.0.1:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

### 3. Test Protected Endpoint
```bash
curl -X GET http://127.0.0.1:8000/children/list \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Production Considerations

### 1. Environment Variables
- `SECRET_KEY`: Strong secret key for JWT signing
- `SENDGRID_API_KEY`: For email verification
- `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET`: For OAuth
- `DEBUG=False`: Disable debug mode

### 2. Security Headers
- HTTPS enforcement
- Secure cookie settings
- CORS configuration for production domains

### 3. Database Security
- SSL connections for production database
- Regular backups and security updates

---

## Quick Reference

### Key Endpoints
- **Registration**: `POST /users/register`
- **Login**: `POST /users/login`
- **Email Verification**: `POST /users/verify-email`
- **Token Refresh**: `POST /users/token/refresh`
- **Password Reset**: `POST /users/password/reset/`
- **Profile**: `GET /users/profile`

### Documentation
- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **OpenAPI Schema**: `/api/schema/`

### Authentication Header
```
Authorization: Bearer <access_token>
```

This authentication system provides a secure, scalable foundation for the Waya family management platform.
