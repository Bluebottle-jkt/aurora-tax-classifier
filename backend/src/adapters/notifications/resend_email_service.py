"""
Resend Email Service Adapter
Handles sending email notifications using Resend API
"""
import os
from typing import Optional, Dict, Any
import resend
from datetime import datetime


class ResendEmailService:
    """
    Email notification service using Resend API.

    Handles:
    - Job completion notifications
    - Error notifications
    - Welcome emails
    - Custom email templates
    """

    def __init__(self):
        """Initialize Resend with API key from environment."""
        api_key = os.getenv("RESEND_API_KEY")
        if not api_key:
            raise ValueError(
                "RESEND_API_KEY environment variable is required. "
                "Get your API key from https://resend.com/"
            )

        resend.api_key = api_key
        self.from_email = os.getenv("RESEND_FROM_EMAIL", "noreply@aurora-classifier.com")
        self.app_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

    def send_job_completion_email(
        self,
        to_email: str,
        job_id: str,
        filename: str,
        total_rows: int,
        duration_seconds: float
    ) -> Dict[str, Any]:
        """
        Send email notification when job processing completes.

        Args:
            to_email: Recipient email address
            job_id: Job identifier
            filename: Original uploaded filename
            total_rows: Number of rows processed
            duration_seconds: Processing time in seconds

        Returns:
            Response from Resend API
        """
        subject = f"✅ AURORA: Your analysis is complete - {filename}"

        html_content = self._build_completion_email_html(
            job_id=job_id,
            filename=filename,
            total_rows=total_rows,
            duration_seconds=duration_seconds
        )

        text_content = self._build_completion_email_text(
            job_id=job_id,
            filename=filename,
            total_rows=total_rows,
            duration_seconds=duration_seconds
        )

        try:
            response = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content,
                "text": text_content,
            })
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_job_failure_email(
        self,
        to_email: str,
        job_id: str,
        filename: str,
        error_message: str
    ) -> Dict[str, Any]:
        """
        Send email notification when job processing fails.

        Args:
            to_email: Recipient email address
            job_id: Job identifier
            filename: Original uploaded filename
            error_message: Error description

        Returns:
            Response from Resend API
        """
        subject = f"❌ AURORA: Analysis failed - {filename}"

        html_content = self._build_failure_email_html(
            job_id=job_id,
            filename=filename,
            error_message=error_message
        )

        text_content = self._build_failure_email_text(
            job_id=job_id,
            filename=filename,
            error_message=error_message
        )

        try:
            response = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content,
                "text": text_content,
            })
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_welcome_email(
        self,
        to_email: str,
        user_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send welcome email to new users.

        Args:
            to_email: Recipient email address
            user_name: User's name (optional)

        Returns:
            Response from Resend API
        """
        subject = "Welcome to AURORA Tax Classifier! 🎉"

        html_content = self._build_welcome_email_html(user_name)
        text_content = self._build_welcome_email_text(user_name)

        try:
            response = resend.Emails.send({
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content,
                "text": text_content,
            })
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # HTML Email Templates

    def _build_completion_email_html(
        self,
        job_id: str,
        filename: str,
        total_rows: int,
        duration_seconds: float
    ) -> str:
        """Build HTML email for job completion."""
        duration_minutes = duration_seconds / 60
        results_url = f"{self.app_url}/results/{job_id}"

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Complete</title>
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 40px auto; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">

        <!-- Header -->
        <div style="background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); padding: 30px; text-align: center;">
            <h1 style="margin: 0; color: white; font-size: 32px; font-weight: bold;">
                AURORA
            </h1>
            <p style="margin: 10px 0 0 0; color: #e0e7ff; font-size: 14px;">
                Audit Object Recognition & Analytics
            </p>
        </div>

        <!-- Success Badge -->
        <div style="text-align: center; padding: 30px 20px 0;">
            <div style="display: inline-block; background-color: #10b981; color: white; padding: 8px 20px; border-radius: 20px; font-size: 14px; font-weight: 600;">
                ✓ Analysis Complete
            </div>
        </div>

        <!-- Content -->
        <div style="padding: 20px 40px 40px;">
            <h2 style="color: #f1f5f9; margin-top: 0;">Your analysis is ready!</h2>

            <p style="color: #cbd5e1; line-height: 1.6;">
                We've successfully processed your file and classified all tax objects.
            </p>

            <!-- Job Details -->
            <div style="background-color: #1e293b; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px 0; color: #94a3b8; font-size: 14px;">File:</td>
                        <td style="padding: 8px 0; color: #e2e8f0; font-size: 14px; font-weight: 600; text-align: right;">{filename}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #94a3b8; font-size: 14px;">Rows Processed:</td>
                        <td style="padding: 8px 0; color: #e2e8f0; font-size: 14px; font-weight: 600; text-align: right;">{total_rows:,}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #94a3b8; font-size: 14px;">Processing Time:</td>
                        <td style="padding: 8px 0; color: #e2e8f0; font-size: 14px; font-weight: 600; text-align: right;">{duration_minutes:.1f} min</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #94a3b8; font-size: 14px;">Job ID:</td>
                        <td style="padding: 8px 0; color: #e2e8f0; font-size: 14px; font-family: monospace; text-align: right;">{job_id}</td>
                    </tr>
                </table>
            </div>

            <!-- CTA Button -->
            <div style="text-align: center; margin: 30px 0 20px;">
                <a href="{results_url}" style="display: inline-block; background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); color: white; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 600; font-size: 16px;">
                    View Results →
                </a>
            </div>

            <!-- Features -->
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #334155;">
                <p style="color: #cbd5e1; font-size: 14px; margin-bottom: 15px;">Your results include:</p>
                <ul style="color: #94a3b8; font-size: 14px; line-height: 1.8; margin: 0; padding-left: 20px;">
                    <li>Tax object classifications (PPh 21, 22, 23, etc.)</li>
                    <li>Fiscal corrections (positive/negative)</li>
                    <li>Confidence scores for each prediction</li>
                    <li>Risk assessments and alerts</li>
                    <li>Downloadable Excel report</li>
                </ul>
            </div>
        </div>

        <!-- Footer -->
        <div style="background-color: #0f172a; padding: 20px; text-align: center; border-top: 1px solid #334155;">
            <p style="color: #64748b; font-size: 12px; margin: 5px 0;">
                © {datetime.now().year} AURORA Tax Classifier. All rights reserved.
            </p>
            <p style="color: #64748b; font-size: 12px; margin: 5px 0;">
                <a href="{self.app_url}" style="color: #3b82f6; text-decoration: none;">Visit Dashboard</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

    def _build_failure_email_html(
        self,
        job_id: str,
        filename: str,
        error_message: str
    ) -> str:
        """Build HTML email for job failure."""
        dashboard_url = f"{self.app_url}/upload"

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Failed</title>
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 40px auto; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">

        <!-- Header -->
        <div style="background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); padding: 30px; text-align: center;">
            <h1 style="margin: 0; color: white; font-size: 32px; font-weight: bold;">
                AURORA
            </h1>
            <p style="margin: 10px 0 0 0; color: #e0e7ff; font-size: 14px;">
                Audit Object Recognition & Analytics
            </p>
        </div>

        <!-- Error Badge -->
        <div style="text-align: center; padding: 30px 20px 0;">
            <div style="display: inline-block; background-color: #ef4444; color: white; padding: 8px 20px; border-radius: 20px; font-size: 14px; font-weight: 600;">
                ✗ Analysis Failed
            </div>
        </div>

        <!-- Content -->
        <div style="padding: 20px 40px 40px;">
            <h2 style="color: #f1f5f9; margin-top: 0;">We encountered an issue</h2>

            <p style="color: #cbd5e1; line-height: 1.6;">
                Unfortunately, we couldn't complete the analysis of your file. Don't worry - your data is safe and you can try again.
            </p>

            <!-- Error Details -->
            <div style="background-color: #7f1d1d; border-radius: 8px; padding: 20px; margin: 20px 0; border-left: 4px solid #ef4444;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px 0; color: #fca5a5; font-size: 14px;">File:</td>
                        <td style="padding: 8px 0; color: #fee2e2; font-size: 14px; font-weight: 600; text-align: right;">{filename}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #fca5a5; font-size: 14px;">Job ID:</td>
                        <td style="padding: 8px 0; color: #fee2e2; font-size: 14px; font-family: monospace; text-align: right;">{job_id}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #fca5a5; font-size: 14px; vertical-align: top;">Error:</td>
                        <td style="padding: 8px 0; color: #fee2e2; font-size: 14px; text-align: right;">{error_message}</td>
                    </tr>
                </table>
            </div>

            <!-- Troubleshooting -->
            <div style="background-color: #1e293b; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <p style="color: #f1f5f9; font-size: 14px; font-weight: 600; margin-top: 0;">Common solutions:</p>
                <ul style="color: #94a3b8; font-size: 14px; line-height: 1.8; margin: 10px 0; padding-left: 20px;">
                    <li>Check that your file is in CSV or Excel format</li>
                    <li>Ensure the file has a "Uraian" column</li>
                    <li>Verify the file isn't corrupted</li>
                    <li>Try with a smaller file first</li>
                </ul>
            </div>

            <!-- CTA Button -->
            <div style="text-align: center; margin: 30px 0 20px;">
                <a href="{dashboard_url}" style="display: inline-block; background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); color: white; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 600; font-size: 16px;">
                    Try Again →
                </a>
            </div>

            <p style="color: #64748b; font-size: 13px; text-align: center; margin-top: 20px;">
                Need help? Contact our support team for assistance.
            </p>
        </div>

        <!-- Footer -->
        <div style="background-color: #0f172a; padding: 20px; text-align: center; border-top: 1px solid #334155;">
            <p style="color: #64748b; font-size: 12px; margin: 5px 0;">
                © {datetime.now().year} AURORA Tax Classifier. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
"""

    def _build_welcome_email_html(self, user_name: Optional[str]) -> str:
        """Build HTML email for welcome message."""
        greeting = f"Hi {user_name}," if user_name else "Welcome!"

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to AURORA</title>
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 40px auto; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">

        <!-- Header with animated gradient -->
        <div style="background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%); padding: 40px; text-align: center;">
            <h1 style="margin: 0; color: white; font-size: 42px; font-weight: bold; letter-spacing: 2px;">
                AURORA
            </h1>
            <p style="margin: 10px 0 0 0; color: #e0e7ff; font-size: 16px;">
                Audit Object Recognition & Analytics
            </p>
        </div>

        <!-- Content -->
        <div style="padding: 40px;">
            <h2 style="color: #f1f5f9; margin-top: 0; font-size: 24px;">{greeting}</h2>

            <p style="color: #cbd5e1; line-height: 1.8; font-size: 16px;">
                Welcome to <strong>AURORA Tax Classifier</strong>! We're excited to help you streamline your Indonesian tax classification and analysis.
            </p>

            <!-- Features Grid -->
            <div style="margin: 30px 0;">
                <div style="background-color: #1e293b; border-radius: 8px; padding: 20px; margin-bottom: 15px;">
                    <div style="color: #3b82f6; font-size: 24px; margin-bottom: 10px;">🎯</div>
                    <h3 style="color: #f1f5f9; margin: 0 0 8px 0; font-size: 18px;">Accurate Classifications</h3>
                    <p style="color: #94a3b8; margin: 0; font-size: 14px; line-height: 1.6;">
                        AI-powered recognition of 14+ tax object types including PPh 21, 22, 23, and fiscal corrections.
                    </p>
                </div>

                <div style="background-color: #1e293b; border-radius: 8px; padding: 20px; margin-bottom: 15px;">
                    <div style="color: #8b5cf6; font-size: 24px; margin-bottom: 10px;">⚡</div>
                    <h3 style="color: #f1f5f9; margin: 0 0 8px 0; font-size: 18px;">Lightning Fast</h3>
                    <p style="color: #94a3b8; margin: 0; font-size: 14px; line-height: 1.6;">
                        Process thousands of transactions in minutes with our optimized ML models.
                    </p>
                </div>

                <div style="background-color: #1e293b; border-radius: 8px; padding: 20px;">
                    <div style="color: #ec4899; font-size: 24px; margin-bottom: 10px;">📊</div>
                    <h3 style="color: #f1f5f9; margin: 0 0 8px 0; font-size: 18px;">Detailed Reports</h3>
                    <p style="color: #94a3b8; margin: 0; font-size: 14px; line-height: 1.6;">
                        Get confidence scores, risk assessments, and downloadable Excel reports for your analysis.
                    </p>
                </div>
            </div>

            <!-- Get Started -->
            <div style="background: linear-gradient(135deg, #1e3a8a 0%, #6b21a8 100%); border-radius: 8px; padding: 25px; margin: 30px 0; text-align: center;">
                <h3 style="color: white; margin: 0 0 15px 0; font-size: 20px;">Ready to get started?</h3>
                <a href="{self.app_url}/upload" style="display: inline-block; background-color: white; color: #1e293b; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 600; font-size: 16px; margin-top: 10px;">
                    Upload Your First File →
                </a>
            </div>

            <!-- Quick Tips -->
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #334155;">
                <p style="color: #cbd5e1; font-size: 14px; font-weight: 600; margin-bottom: 15px;">Quick tips to get the most out of AURORA:</p>
                <ul style="color: #94a3b8; font-size: 14px; line-height: 1.8; margin: 0; padding-left: 20px;">
                    <li>Upload CSV or Excel files with transaction descriptions</li>
                    <li>Ensure your file has a column named "Uraian"</li>
                    <li>Review results and download detailed reports</li>
                    <li>Check confidence scores to verify classifications</li>
                </ul>
            </div>
        </div>

        <!-- Footer -->
        <div style="background-color: #0f172a; padding: 25px; text-align: center; border-top: 1px solid #334155;">
            <p style="color: #64748b; font-size: 12px; margin: 5px 0;">
                © {datetime.now().year} AURORA Tax Classifier. All rights reserved.
            </p>
            <p style="color: #64748b; font-size: 12px; margin: 15px 0 5px;">
                <a href="{self.app_url}" style="color: #3b82f6; text-decoration: none; margin: 0 10px;">Dashboard</a> |
                <a href="{self.app_url}/profile" style="color: #3b82f6; text-decoration: none; margin: 0 10px;">Profile</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

    # Plain Text Email Templates

    def _build_completion_email_text(
        self,
        job_id: str,
        filename: str,
        total_rows: int,
        duration_seconds: float
    ) -> str:
        """Build plain text email for job completion."""
        duration_minutes = duration_seconds / 60
        results_url = f"{self.app_url}/results/{job_id}"

        return f"""
AURORA Tax Classifier - Analysis Complete

Your analysis is ready!

We've successfully processed your file and classified all tax objects.

Job Details:
- File: {filename}
- Rows Processed: {total_rows:,}
- Processing Time: {duration_minutes:.1f} minutes
- Job ID: {job_id}

Your results include:
• Tax object classifications (PPh 21, 22, 23, etc.)
• Fiscal corrections (positive/negative)
• Confidence scores for each prediction
• Risk assessments and alerts
• Downloadable Excel report

View your results here:
{results_url}

© {datetime.now().year} AURORA Tax Classifier
Visit Dashboard: {self.app_url}
"""

    def _build_failure_email_text(
        self,
        job_id: str,
        filename: str,
        error_message: str
    ) -> str:
        """Build plain text email for job failure."""
        dashboard_url = f"{self.app_url}/upload"

        return f"""
AURORA Tax Classifier - Analysis Failed

We encountered an issue processing your file.

Job Details:
- File: {filename}
- Job ID: {job_id}
- Error: {error_message}

Common solutions:
• Check that your file is in CSV or Excel format
• Ensure the file has a "Uraian" column
• Verify the file isn't corrupted
• Try with a smaller file first

Try again here:
{dashboard_url}

Need help? Contact our support team for assistance.

© {datetime.now().year} AURORA Tax Classifier
"""

    def _build_welcome_email_text(self, user_name: Optional[str]) -> str:
        """Build plain text email for welcome message."""
        greeting = f"Hi {user_name}," if user_name else "Welcome!"

        return f"""
AURORA Tax Classifier - Welcome!

{greeting}

Welcome to AURORA Tax Classifier! We're excited to help you streamline your Indonesian tax classification and analysis.

What AURORA offers:
• Accurate Classifications: AI-powered recognition of 14+ tax object types
• Lightning Fast: Process thousands of transactions in minutes
• Detailed Reports: Confidence scores, risk assessments, and Excel reports

Quick tips to get started:
• Upload CSV or Excel files with transaction descriptions
• Ensure your file has a column named "Uraian"
• Review results and download detailed reports
• Check confidence scores to verify classifications

Get started:
{self.app_url}/upload

© {datetime.now().year} AURORA Tax Classifier
Visit Dashboard: {self.app_url}
Manage Profile: {self.app_url}/profile
"""
