#!/usr/bin/env python3
"""
Mock AI CLI Tool - Simulates behavior of claude-code, gemini, aider

This tool simulates an AI coding assistant for testing and demonstration purposes.
It responds to prompts with realistic code generation, reviews, and fixes.

Usage:
    python mock_ai_cli.py [--mode MODE]

Modes:
    - coder: Generates code (like claude-code)
    - reviewer: Reviews code for issues (like gemini)
    - fixer: Fixes code issues (like aider)
    - interactive: Interactive mode (stays open, responds to input)

This enables testing the full orchestration workflow without requiring
actual AI CLI tools to be installed.
"""

import sys
import time
import random
import argparse

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Response Templates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CODER_RESPONSES = {
    "rest api": """
I'll create a REST API for user authentication with FastAPI:

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
import bcrypt

app = FastAPI()
security = HTTPBearer()

# User model
class User(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# In-memory user storage (replace with database)
users_db = {}

@app.post("/register")
async def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_db[user.username] = hashed

    return {"message": "User registered successfully"}

@app.post("/login")
async def login(credentials: UserLogin):
    if credentials.username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    stored_hash = users_db[credentials.username]
    if not bcrypt.checkpw(credentials.password.encode(), stored_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    token = jwt.encode(
        {"sub": credentials.username},
        "SECRET_KEY",  # Should be in env var
        algorithm="HS256"
    )

    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            "SECRET_KEY",
            algorithms=["HS256"]
        )
        return {"message": f"Hello {payload['sub']}!"}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

This API provides:
- `/register` - Register new users with hashed passwords
- `/login` - Authenticate and get JWT token
- `/protected` - Access protected resource with token

To run: `pip install fastapi uvicorn pyjwt bcrypt && python main.py`
""",

    "fibonacci": """
Here's a Python implementation of fibonacci numbers:

```python
def fibonacci(n: int) -> int:
    \"\"\"
    Calculate the nth Fibonacci number.

    Args:
        n: Position in sequence (0-indexed)

    Returns:
        The nth Fibonacci number

    Time complexity: O(n)
    Space complexity: O(1)
    \"\"\"
    if n < 0:
        raise ValueError("n must be non-negative")

    if n <= 1:
        return n

    # Iterative approach (better than recursive)
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr

# Alternative: Generator for sequence
def fibonacci_sequence(count: int):
    \"\"\"Generate first 'count' fibonacci numbers.\"\"\"
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b

# Usage examples
print(f"10th fibonacci: {fibonacci(10)}")  # 55
print(f"First 10: {list(fibonacci_sequence(10))}")
```

This uses an iterative approach which is O(n) time and O(1) space,
much better than the naive recursive O(2^n) approach.
""",

    "default": """
I'll help you with that. Here's a Python implementation:

```python
def process_data(data):
    \"\"\"Process the input data.\"\"\"
    result = []
    for item in data:
        # Process each item
        processed = item.strip().lower()
        if processed:
            result.append(processed)
    return result

# Example usage
data = ["  Hello  ", "World", "  "]
output = process_data(data)
print(output)  # ['hello', 'world']
```

This provides a basic implementation that you can customize.
"""
}

REVIEWER_RESPONSES = {
    "security": """
I've reviewed the code for security issues. Here are my findings:

**CRITICAL Issues:**

1. **Hardcoded Secret Key** (Line 42)
   - Problem: `SECRET_KEY = "SECRET_KEY"` is hardcoded
   - Risk: JWT tokens can be forged by anyone
   - Fix: Use environment variable: `os.getenv("JWT_SECRET_KEY")`

2. **No Password Strength Validation**
   - Problem: Accepts any password, even "123"
   - Risk: Weak passwords compromise security
   - Fix: Add minimum length, complexity requirements

3. **No Rate Limiting**
   - Problem: /login endpoint has no rate limiting
   - Risk: Brute force attacks possible
   - Fix: Add rate limiting with slowapi or similar

**MEDIUM Issues:**

4. **SQL Injection Risk** (if using database)
   - Current: Uses dict, but migration to SQL could introduce risk
   - Fix: Use parameterized queries or ORM

5. **No HTTPS Enforcement**
   - Problem: Credentials could be sent over HTTP
   - Fix: Add HTTPS redirect, HSTS header

**LOW Issues:**

6. **No Password Reset Flow**
   - Missing: Forgot password functionality
   - Impact: User lockout scenarios

**Recommendations:**
1. Move SECRET_KEY to environment variable immediately
2. Add password validation (min 8 chars, special char, number)
3. Implement rate limiting (max 5 login attempts per minute)
4. Use HTTPS in production
5. Add comprehensive input validation

Let me know if you'd like me to show the fixes!
""",

    "default": """
I've reviewed the code. Here are some observations:

**Good practices:**
- Clear function names and docstrings
- Type hints used appropriately
- Error handling in place

**Potential improvements:**
1. Add input validation for edge cases
2. Consider performance optimization for large datasets
3. Add unit tests for critical functions
4. Improve error messages to be more descriptive

**Security notes:**
- No obvious security vulnerabilities detected
- Consider adding input sanitization if user-facing

Overall the code looks solid, with room for minor improvements.
"""
}

FIXER_RESPONSES = {
    "security": """
I've fixed the security issues. Here are the changes:

```python
import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, validator
from typing import Optional
import jwt
import bcrypt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# FIXED: Use environment variable for secret
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET_KEY environment variable must be set")

app = FastAPI()
security = HTTPBearer()

# FIXED: Add rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# FIXED: Password validation
class User(BaseModel):
    username: str
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain a number')
        if not any(c in '!@#$%^&*' for c in v):
            raise ValueError('Password must contain special character')
        return v

users_db = {}

@app.post("/register")
async def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_db[user.username] = hashed

    return {"message": "User registered successfully"}

# FIXED: Add rate limiting to login
@app.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: UserLogin):
    if credentials.username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_hash = users_db[credentials.username]
    if not bcrypt.checkpw(credentials.password.encode(), stored_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Use environment variable for JWT secret
    token = jwt.encode(
        {"sub": credentials.username},
        JWT_SECRET,  # FIXED: Use env var
        algorithm="HS256"
    )

    return {"access_token": token, "token_type": "bearer"}
```

**Changes Made:**
1. ✅ Moved JWT_SECRET to environment variable
2. ✅ Added password strength validation (8+ chars, uppercase, number, special char)
3. ✅ Added rate limiting (5 attempts/minute on login)
4. ✅ Added input validation with Pydantic validators

**To use:**
```bash
export JWT_SECRET_KEY="your-very-long-secret-key-here"
pip install slowapi
python main.py
```

All critical security issues resolved!
""",

    "default": """
I've made the requested fixes:

```python
def process_data(data):
    \"\"\"
    Process the input data with improved error handling.

    Args:
        data: List of items to process

    Returns:
        List of processed items

    Raises:
        ValueError: If data is not a list
    \"\"\"
    if not isinstance(data, list):
        raise ValueError("Input must be a list")

    result = []
    for item in data:
        try:
            # Process each item with error handling
            processed = str(item).strip().lower()
            if processed:
                result.append(processed)
        except Exception as e:
            # Log error but continue processing
            print(f"Warning: Could not process item {item}: {e}")
            continue

    return result
```

Changes:
- Added input validation
- Added error handling for individual items
- Improved docstring
- Added type checking

The code is now more robust and handles edge cases better.
"""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Response Selection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_response(prompt: str, mode: str) -> str:
    """
    Generate appropriate response based on prompt and mode.

    Args:
        prompt: User's input prompt
        mode: coder, reviewer, or fixer

    Returns:
        Simulated AI response
    """
    prompt_lower = prompt.lower()

    if mode == "coder":
        responses = CODER_RESPONSES
    elif mode == "reviewer":
        responses = REVIEWER_RESPONSES
    elif mode == "fixer":
        responses = FIXER_RESPONSES
    else:
        responses = CODER_RESPONSES

    # Match keywords in prompt
    for keyword, response in responses.items():
        if keyword in prompt_lower:
            return response

    return responses.get("default", "I can help with that. What would you like me to do?")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Interactive Mode
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def interactive_mode(mode: str):
    """
    Run in interactive mode - accepts prompts and responds.

    This simulates how real AI CLI tools work (stay open, respond to input).
    """
    print(f"Mock AI CLI ({mode} mode) - Ready!")
    print("Type your prompts (Ctrl+D to exit):")
    print()

    try:
        while True:
            # Read input (could be from orchestrator)
            try:
                line = input()
            except EOFError:
                break

            if not line.strip():
                continue

            # Simulate thinking time
            time.sleep(random.uniform(0.1, 0.3))

            # Generate response
            response = get_response(line, mode)
            print(response)
            print()  # Blank line between responses

            # Flush output (important for PTY communication)
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\nExiting...")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(description="Mock AI CLI Tool")
    parser.add_argument(
        "--mode",
        choices=["coder", "reviewer", "fixer", "interactive"],
        default="interactive",
        help="Tool mode (default: interactive)"
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Prompt to process (if not interactive)"
    )

    args = parser.parse_args()

    if args.prompt:
        # One-shot mode
        prompt = " ".join(args.prompt)
        response = get_response(prompt, args.mode)
        print(response)
    else:
        # Interactive mode
        interactive_mode(args.mode)


if __name__ == "__main__":
    main()
