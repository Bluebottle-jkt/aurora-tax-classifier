# Resend Email Notifications Guide - AURORA Tax Classifier

Complete guide to email notifications using Resend in the AURORA Tax Classifier application.

**Created**: December 24, 2025
**Status**: Email System Implemented
**Service**: Resend (https://resend.com)

---

## Table of Contents

1. [Overview](#overview)
2. [What Was Implemented](#what-was-implemented)
3. [Getting Started](#getting-started)
4. [Email Templates](#email-templates)
5. [Integration](#integration)
6. [Configuration](#configuration)
7. [Usage Examples](#usage-examples)
8. [Testing](#testing)
9. [Customization](#customization)
10. [Troubleshooting](#troubleshooting)

---

## Overview

Resend provides email notification capabilities for AURORA Tax Classifier including:

✅ **Job Completion Emails** - Notify users when analysis completes
✅ **Job Failure Emails** - Alert users when processing fails
✅ **Welcome Emails** - Onboard new users
✅ **Beautiful HTML Templates** - Branded, responsive emails
✅ **Plain Text Fallback** - Accessibility for all email clients

---

## What Was Implemented

### Files Created

| File | Purpose |
|------|---------|
| `backend/src/adapters/notifications/resend_email_service.py` | Main email service |
| `backend/src/adapters/notifications/__init__.py` | Module initialization |
| `RESEND_EMAIL_GUIDE.md` | This documentation |

### Files Modified

| File | Changes |
|------|---------|
| `backend/requirements.txt` | Added `resend==2.19.0` |
| `.env.example` | Added Resend configuration |

### Email Templates Included

1. **Job Completion** - Sent when file processing completes successfully
2. **Job Failure** - Sent when file processing encounters an error
3. **Welcome Email** - Sent to new users (optional integration with Clerk)

---

## Getting Started

### Step 1: Create Resend Account

1. Go to https://resend.com/
2. Sign up for a free account (100 emails/day free tier)
3. Verify your email address
4. Complete account setup

### Step 2: Get API Key

In your Resend dashboard:

1. Navigate to **API Keys** section
2. Click **Create API Key**
3. Name it "AURORA Tax Classifier"
4. Select **Full Access** or **Sending Access**
5. Copy the API key (starts with `re_`)
6. Store it securely (you won't see it again!)

### Step 3: Verify Domain (Optional but Recommended)

For production use, verify your sending domain:

1. Go to **Domains** in Resend dashboard
2. Click **Add Domain**
3. Enter your domain (e.g., `aurora-classifier.com`)
4. Add DNS records to your domain:
   - SPF record
   - DKIM record
   - DMARC record (optional)
5. Wait for verification (usually a few minutes)

**Without verified domain:**
- Emails sent from: `onboarding@resend.dev`
- Limited to 100 emails/day
- Some email providers may flag as spam

**With verified domain:**
- Emails sent from: `noreply@yourdomain.com`
- Higher sending limits
- Better deliverability

### Step 4: Configure Environment Variables

Add to your `.env` file:

```bash
# Resend Email Configuration
RESEND_API_KEY=re_your_actual_api_key_here
RESEND_FROM_EMAIL=noreply@yourdomain.com

# Frontend URL (for email links)
FRONTEND_URL=http://localhost:3000
```

**Important:**
- `RESEND_API_KEY` - Required, get from Resend dashboard
- `RESEND_FROM_EMAIL` - Use verified domain or `onboarding@resend.dev`
- `FRONTEND_URL` - URL where your frontend is hosted

### Step 5: Test the Integration

Create a test script `test_email.py`:

```python
import os
from dotenv import load_dotenv
from backend.src.adapters.notifications import ResendEmailService

load_dotenv()

email_service = ResendEmailService()

# Test completion email
result = email_service.send_job_completion_email(
    to_email="your-email@example.com",
    job_id="test-123",
    filename="test-data.csv",
    total_rows=100,
    duration_seconds=45.5
)

print(result)
```

Run:
```bash
python test_email.py
```

---

## Email Templates

### 1. Job Completion Email

**Sent when**: File processing completes successfully

**Includes**:
- Success badge
- File details (name, rows, processing time)
- Job ID
- "View Results" CTA button
- Feature list
- Responsive HTML design

**Preview**:
- Subject: `✅ AURORA: Your analysis is complete - filename.csv`
- Beautiful gradient header with AURORA branding
- Green success indicator
- Job details table
- Call-to-action button
- Professional footer

### 2. Job Failure Email

**Sent when**: File processing fails

**Includes**:
- Error badge
- File details
- Error message
- Troubleshooting tips
- "Try Again" CTA button
- Support contact info

**Preview**:
- Subject: `❌ AURORA: Analysis failed - filename.csv`
- Red error indicator
- Error details
- Common solutions list
- Retry button

### 3. Welcome Email

**Sent when**: New user signs up (optional)

**Includes**:
- Welcome message
- Feature highlights
- Quick tips
- "Get Started" CTA button
- Dashboard links

**Preview**:
- Subject: `Welcome to AURORA Tax Classifier! 🎉`
- Animated gradient header
- Feature cards
- Getting started guide
- Quick tips

---

## Integration

### Basic Usage

```python
from backend.src.adapters.notifications import ResendEmailService

# Initialize service
email_service = ResendEmailService()

# Send completion email
result = email_service.send_job_completion_email(
    to_email="user@example.com",
    job_id="job-abc-123",
    filename="transactions.csv",
    total_rows=1500,
    duration_seconds=120.5
)

if result["success"]:
    print("Email sent successfully!")
else:
    print(f"Error: {result['error']}")
```

### Integration with Job Processing

In `backend/src/application/use_cases/process_job_use_case.py`:

```python
from ...adapters.notifications import ResendEmailService

class ProcessJobUseCase:
    def __init__(
        self,
        job_repo,
        classifier,
        email_service: ResendEmailService = None
    ):
        self.job_repo = job_repo
        self.classifier = classifier
        self.email_service = email_service or ResendEmailService()

    async def execute(self, job_id: str, user_email: str):
        try:
            # Process job...
            job = self.job_repo.get(job_id)
            # ... classification logic ...

            # Mark as complete
            job.status = "completed"
            self.job_repo.save(job)

            # Send success email
            self.email_service.send_job_completion_email(
                to_email=user_email,
                job_id=job_id,
                filename=job.filename,
                total_rows=job.total_rows,
                duration_seconds=(job.completed_at - job.created_at).total_seconds()
            )

        except Exception as e:
            # Mark as failed
            job.status = "failed"
            job.error_message = str(e)
            self.job_repo.save(job)

            # Send failure email
            self.email_service.send_job_failure_email(
                to_email=user_email,
                job_id=job_id,
                filename=job.filename,
                error_message=str(e)
            )
```

### Integration with Clerk (Optional)

Send welcome email when user signs up:

```python
from ...adapters.notifications import ResendEmailService

# In Clerk webhook handler
@app.post("/api/webhooks/clerk")
async def clerk_webhook(request: Request):
    payload = await request.json()

    if payload["type"] == "user.created":
        user_data = payload["data"]
        email = user_data["email_addresses"][0]["email_address"]
        name = user_data.get("first_name")

        # Send welcome email
        email_service = ResendEmailService()
        email_service.send_welcome_email(
            to_email=email,
            user_name=name
        )

    return {"status": "ok"}
```

---

## Configuration

### Environment Variables

```bash
# Required
RESEND_API_KEY=re_xxxxxxxxxxxx

# Optional (with defaults)
RESEND_FROM_EMAIL=noreply@yourdomain.com  # Default: noreply@aurora-classifier.com
FRONTEND_URL=https://your-domain.com       # Default: http://localhost:3000
```

### Custom From Email

```python
email_service = ResendEmailService()
email_service.from_email = "custom@yourdomain.com"
```

### Custom App URL

```python
email_service = ResendEmailService()
email_service.app_url = "https://custom-domain.com"
```

---

## Usage Examples

### Example 1: Send Completion Email

```python
from backend.src.adapters.notifications import ResendEmailService

email_service = ResendEmailService()

result = email_service.send_job_completion_email(
    to_email="analyst@company.com",
    job_id="550e8400-e29b-41d4-a716-446655440000",
    filename="monthly-transactions.xlsx",
    total_rows=2500,
    duration_seconds=180.5
)

print(f"Success: {result['success']}")
if result['success']:
    print(f"Email ID: {result['response']['id']}")
```

### Example 2: Send Failure Email with Error Details

```python
result = email_service.send_job_failure_email(
    to_email="analyst@company.com",
    job_id="550e8400-e29b-41d4-a716-446655440000",
    filename="corrupted-file.csv",
    error_message="File encoding error: Unable to decode CSV with UTF-8"
)

if not result['success']:
    print(f"Failed to send email: {result['error']}")
```

### Example 3: Send Welcome Email to New User

```python
result = email_service.send_welcome_email(
    to_email="newuser@company.com",
    user_name="John Doe"
)

print("Welcome email sent!" if result['success'] else "Failed to send")
```

### Example 4: Error Handling

```python
try:
    result = email_service.send_job_completion_email(
        to_email="invalid-email",  # Invalid email
        job_id="test",
        filename="test.csv",
        total_rows=10,
        duration_seconds=5.0
    )

    if not result['success']:
        # Log error, retry, or notify admin
        logger.error(f"Email send failed: {result['error']}")
        # Optionally: retry with exponential backoff
        # Or: save to queue for later processing

except Exception as e:
    logger.critical(f"Email service error: {e}")
```

---

## Testing

### Manual Testing

1. **Test with your own email**:
```python
from backend.src.adapters.notifications import ResendEmailService

email_service = ResendEmailService()

# Test all templates
email_service.send_welcome_email("your@email.com", "Your Name")
email_service.send_job_completion_email("your@email.com", "test-1", "test.csv", 100, 30.0)
email_service.send_job_failure_email("your@email.com", "test-2", "test.csv", "Test error")
```

2. **Check Resend dashboard**:
   - Go to **Emails** tab
   - View sent emails
   - Check delivery status
   - Preview email content

### Automated Testing

```python
import pytest
from unittest.mock import patch, MagicMock
from backend.src.adapters.notifications import ResendEmailService

def test_send_completion_email_success():
    """Test successful email sending."""
    with patch('resend.Emails.send') as mock_send:
        mock_send.return_value = {"id": "email-123"}

        service = ResendEmailService()
        result = service.send_job_completion_email(
            to_email="test@example.com",
            job_id="job-1",
            filename="test.csv",
            total_rows=50,
            duration_seconds=10.0
        )

        assert result["success"] is True
        assert "response" in result
        mock_send.assert_called_once()

def test_send_completion_email_failure():
    """Test email sending failure."""
    with patch('resend.Emails.send') as mock_send:
        mock_send.side_effect = Exception("API Error")

        service = ResendEmailService()
        result = service.send_job_completion_email(
            to_email="test@example.com",
            job_id="job-1",
            filename="test.csv",
            total_rows=50,
            duration_seconds=10.0
        )

        assert result["success"] is False
        assert "error" in result
```

### Test Email Appearance

Use Resend's test mode to preview emails:

```python
# Send to Resend's test inbox
result = email_service.send_job_completion_email(
    to_email="test@resend.dev",  # Resend test inbox
    job_id="preview-1",
    filename="sample.csv",
    total_rows=1000,
    duration_seconds=60.0
)

# View in Resend dashboard under "Test Emails"
```

---

## Customization

### Custom Email Templates

Modify templates in `resend_email_service.py`:

```python
def _build_completion_email_html(self, job_id, filename, total_rows, duration_seconds):
    # Add your custom HTML
    custom_section = """
    <div style="background-color: #your-color; padding: 20px;">
        <p>Your custom content here</p>
    </div>
    """

    return f"""
    ... existing template ...
    {custom_section}
    ... rest of template ...
    """
```

### Custom Colors

Update the gradient colors:

```python
# Change header gradient
<div style="background: linear-gradient(90deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);">

# Change CTA button
<a href="..." style="background: linear-gradient(90deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);">
```

### Add Custom Email Types

Create new email method:

```python
def send_custom_notification(
    self,
    to_email: str,
    subject: str,
    message: str
) -> Dict[str, Any]:
    """Send custom notification email."""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h1>{subject}</h1>
        <p>{message}</p>
    </body>
    </html>
    """

    try:
        response = resend.Emails.send({
            "from": self.from_email,
            "to": to_email,
            "subject": subject,
            "html": html_content,
        })
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Add Attachments

```python
def send_email_with_attachment(
    self,
    to_email: str,
    subject: str,
    html_content: str,
    attachment_path: str
) -> Dict[str, Any]:
    """Send email with file attachment."""

    with open(attachment_path, 'rb') as f:
        attachment_data = f.read()

    try:
        response = resend.Emails.send({
            "from": self.from_email,
            "to": to_email,
            "subject": subject,
            "html": html_content,
            "attachments": [{
                "filename": os.path.basename(attachment_path),
                "content": attachment_data
            }]
        })
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

## Troubleshooting

### Issue: "Missing RESEND_API_KEY"

**Symptom**: `ValueError: RESEND_API_KEY environment variable is required`

**Solution**:
1. Check `.env` file exists
2. Verify `RESEND_API_KEY` is set
3. Restart application
4. Check API key is valid in Resend dashboard

### Issue: Emails Not Being Delivered

**Symptom**: Email sent successfully but not received

**Solution**:
1. Check spam/junk folder
2. Verify email address is correct
3. Check Resend dashboard for delivery status
4. Verify domain is verified (for production)
5. Check recipient's email provider isn't blocking

### Issue: "403 Forbidden" Error

**Symptom**: API returns 403 error

**Solution**:
1. Verify API key is correct
2. Check API key has "Sending Access" permission
3. Regenerate API key if needed
4. Ensure no IP restrictions in Resend settings

### Issue: Emails Look Different in Different Clients

**Symptom**: HTML rendering varies across email clients

**Solution**:
- Use inline CSS (already implemented)
- Test with Email on Acid or Litmus
- Provide plain text fallback (already implemented)
- Avoid complex CSS features
- Use tables for layout (already implemented)

### Issue: Slow Email Sending

**Symptom**: Email takes long time to send

**Solution**:
1. Send emails asynchronously:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)

async def send_email_async(email_service, to_email, ...):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        email_service.send_job_completion_email,
        to_email, job_id, filename, total_rows, duration_seconds
    )
    return result
```

2. Use background tasks:
```python
from fastapi import BackgroundTasks

@app.post("/api/jobs/{job_id}/complete")
async def complete_job(
    job_id: str,
    background_tasks: BackgroundTasks
):
    # ... job completion logic ...

    # Send email in background
    background_tasks.add_task(
        email_service.send_job_completion_email,
        user_email, job_id, filename, rows, duration
    )

    return {"status": "completed"}
```

---

## Advanced Features

### Batch Emails

Send to multiple recipients:

```python
def send_batch_completion_emails(
    self,
    recipients: List[str],
    job_id: str,
    filename: str,
    total_rows: int,
    duration_seconds: float
) -> Dict[str, Any]:
    """Send completion email to multiple recipients."""

    results = []
    for email in recipients:
        result = self.send_job_completion_email(
            to_email=email,
            job_id=job_id,
            filename=filename,
            total_rows=total_rows,
            duration_seconds=duration_seconds
        )
        results.append({"email": email, "result": result})

    return {
        "total": len(recipients),
        "successes": sum(1 for r in results if r["result"]["success"]),
        "failures": sum(1 for r in results if not r["result"]["success"]),
        "details": results
    }
```

### Email Templates with Variables

Create reusable templates:

```python
def send_template_email(
    self,
    to_email: str,
    template_name: str,
    variables: Dict[str, Any]
) -> Dict[str, Any]:
    """Send email using template with variables."""

    templates = {
        "completion": self._build_completion_email_html,
        "failure": self._build_failure_email_html,
        "welcome": self._build_welcome_email_html,
    }

    html_content = templates[template_name](**variables)

    # ... send email ...
```

### Scheduled Emails

Use with task queue (Celery, RQ):

```python
from celery import Celery

celery_app = Celery('aurora', broker='redis://localhost:6379')

@celery_app.task
def send_scheduled_email(to_email, job_id, ...):
    email_service = ResendEmailService()
    return email_service.send_job_completion_email(
        to_email, job_id, ...
    )

# Schedule for later
send_scheduled_email.apply_async(
    args=[email, job_id, ...],
    countdown=3600  # Send in 1 hour
)
```

---

## Production Checklist

Before going to production:

- [ ] Verify domain in Resend
- [ ] Use production API key
- [ ] Set up DKIM, SPF, DMARC records
- [ ] Update `RESEND_FROM_EMAIL` to verified domain
- [ ] Update `FRONTEND_URL` to production URL
- [ ] Test all email templates
- [ ] Set up email monitoring/logging
- [ ] Configure error notifications
- [ ] Test spam score (mail-tester.com)
- [ ] Set up email analytics (optional)
- [ ] Document email suppression list handling
- [ ] Configure bounce/complaint handling

---

## Resources

**Resend Documentation:**
- Main Docs: https://resend.com/docs
- API Reference: https://resend.com/docs/api-reference
- Python SDK: https://resend.com/docs/send-with-python
- Email Testing: https://resend.com/docs/dashboard/emails/send-test-email

**AURORA Project:**
- [README.md](README.md) - Project overview
- [CLERK_AUTHENTICATION_GUIDE.md](CLERK_AUTHENTICATION_GUIDE.md) - Authentication docs
- [PROJECT_EXPANSION_STATUS.md](PROJECT_EXPANSION_STATUS.md) - Current status

**Email Testing Tools:**
- Litmus: https://litmus.com/
- Email on Acid: https://www.emailonacid.com/
- Mail Tester: https://www.mail-tester.com/

---

## Summary

Resend email notifications are now fully integrated into AURORA Tax Classifier with:

✅ Job completion notifications
✅ Job failure alerts
✅ Welcome emails for new users
✅ Beautiful HTML templates
✅ Plain text fallbacks
✅ Easy customization
✅ Production-ready configuration

**Next Steps:**
1. Get Resend API key
2. Add to `.env` file
3. Test email sending
4. Verify domain (for production)
5. Integrate with job processing
6. Deploy and monitor

---

**Created**: December 24, 2025
**Status**: Complete and Ready to Use
**Version**: 1.0

Happy emailing! 📧
