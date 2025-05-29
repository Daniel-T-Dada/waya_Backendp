# Waya Backend API Endpoints Summary

## 🚀 New API-Prefixed Endpoints

All authentication endpoints are now available with the `/api/` prefix as requested by the frontend team.

### 🔐 Authentication Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/api/register` | POST | User registration | ✅ Active |
| `/api/login` | POST | User login | ✅ Active |
| `/api/verify-email` | POST | Email verification | ✅ Active |
| `/api/password/change` | POST | Change password | ✅ Active |
| `/api/password/reset` | POST | Request password reset | ✅ Active |
| `/api/password/reset/confirm/<uidb64>/<token>` | POST | Confirm password reset | ✅ Active |
| `/api/forgot-password` | POST | Forgot password | ✅ Active |
| `/api/reset-password/confirm` | POST | Reset password confirmation | ✅ Active |
| `/api/auth/google` | POST | Google OAuth login | ✅ Active |
| `/api/token/refresh` | POST | JWT token refresh | ✅ Active |

### 📚 API Documentation Endpoints

| Endpoint | Description | Status |
|----------|-------------|---------|
| `/api/docs/` | Swagger UI Documentation | ✅ Active |
| `/api/redoc/` | ReDoc Documentation | ✅ Active |
| `/api/schema/` | OpenAPI Schema | ✅ Active |

## 🔄 Backward Compatibility

All original `/users/` endpoints remain active for backward compatibility:

| Original Endpoint | New API Endpoint | Status |
|-------------------|------------------|---------|
| `/users/register/` | `/api/register` | Both Active |
| `/users/login/` | `/api/login` | Both Active |
| `/users/verify-email/` | `/api/verify-email` | Both Active |
| `/users/password/change/` | `/api/password/change` | Both Active |
| `/users/password/reset/` | `/api/password/reset` | Both Active |

## 🛠️ Frontend Integration Guide

### Base URL
- **Development**: `http://127.0.0.1:8000`
- **Production**: `https://waya-backendp-7.onrender.com`

### Example Usage

#### Registration
```javascript
const response = await fetch('/api/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password1: 'securepassword',
    password2: 'securepassword',
    first_name: 'John',
    last_name: 'Doe',
    role: 'parent'
  })
});
```

#### Login
```javascript
const response = await fetch('/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securepassword'
  })
});

const data = await response.json();
// Store tokens
localStorage.setItem('access_token', data.access_token);
localStorage.setItem('refresh_token', data.refresh_token);
```

#### Token Refresh
```javascript
const response = await fetch('/api/token/refresh', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    refresh: localStorage.getItem('refresh_token')
  })
});

const data = await response.json();
localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);
```

#### Authenticated Requests
```javascript
const response = await fetch('/api/some-endpoint', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json',
  }
});
```

## ✅ Testing Status

- **All API endpoints**: ✅ Working
- **Token refresh**: ✅ Working (Fixed blacklist issue)
- **Email verification**: ✅ Working
- **Password reset**: ✅ Working
- **Google OAuth**: ✅ Working
- **API Documentation**: ✅ Working
- **Backward compatibility**: ✅ Maintained

## 🔧 Recent Changes Made

1. **Added API-prefixed URLs**: Created `users/api_urls.py` with `/api/` prefixed endpoints
2. **Updated main URLs**: Added API routes in `waya_backend/urls.py`
3. **Fixed JWT Token Refresh**: Added `rest_framework_simplejwt.token_blacklist` to `INSTALLED_APPS`
4. **Maintained Backward Compatibility**: Old `/users/` endpoints still work
5. **Enhanced Documentation**: Added comprehensive Swagger/OpenAPI documentation

## 📋 Next Steps for Frontend Team

1. **Update API Base URLs**: Change all authentication endpoints from `/users/` to `/api/`
2. **Test Integration**: Use the Swagger UI at `/api/docs/` to test endpoints
3. **Update Documentation**: Reference this summary and the Swagger docs
4. **Gradual Migration**: Can migrate gradually since old endpoints still work

## 🌐 API Documentation Links

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

## 📞 Support

For any issues or questions regarding the API endpoints, please refer to:
1. The comprehensive `AUTHENTICATION_FLOW.md` documentation
2. The Swagger UI for interactive testing
3. This summary document for quick reference

---
**Last Updated**: May 29, 2025
**API Version**: 1.0.0
**Status**: ✅ Production Ready
