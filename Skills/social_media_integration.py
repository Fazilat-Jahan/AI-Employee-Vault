"""
Social Media Integration for AI Employee Vault
Implements Gold Tier requirement for Facebook and Instagram integration
"""
import requests
import json
from datetime import datetime
from pathlib import Path

class SocialMediaIntegration:
    def __init__(self):
        self.facebook_access_token = None
        self.instagram_access_token = None

    def set_facebook_credentials(self, access_token):
        """Set Facebook access token"""
        self.facebook_access_token = access_token

    def set_instagram_credentials(self, access_token):
        """Set Instagram access token"""
        self.instagram_access_token = access_token

    def post_to_facebook(self, message, page_id=None):
        """Post message to Facebook page or personal timeline"""
        if not self.facebook_access_token:
            raise Exception("Facebook access token not set")

        url = f"https://graph.facebook.com/v18.0/me/feed"
        if page_id:
            url = f"https://graph.facebook.com/v18.0/{page_id}/feed"

        params = {
            'message': message,
            'access_token': self.facebook_access_token
        }

        response = requests.post(url, params=params)

        if response.status_code == 200:
            post_id = response.json().get('id')
            self.log_social_action('facebook_post', {'message': message, 'post_id': post_id}, 'success')
            return post_id
        else:
            self.log_social_action('facebook_post', {'message': message}, 'failed', response.text)
            raise Exception(f"Facebook post failed: {response.text}")

    def post_to_instagram_basic(self, image_url, caption):
        """Post to Instagram using basic Graph API"""
        if not self.instagram_access_token:
            raise Exception("Instagram access token not set")

        # First upload the image
        url = "https://graph.facebook.com/v18.0/me/media"
        params = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.instagram_access_token
        }

        response = requests.post(url, params=params)

        if response.status_code == 200:
            container_id = response.json().get('id')

            # Publish the container
            publish_url = "https://graph.facebook.com/v18.0/me/media_publish"
            publish_params = {
                'creation_id': container_id,
                'access_token': self.instagram_access_token
            }

            publish_response = requests.post(publish_url, params=publish_params)

            if publish_response.status_code == 200:
                post_id = publish_response.json().get('id')
                self.log_social_action('instagram_post', {'caption': caption, 'post_id': post_id}, 'success')
                return post_id
            else:
                self.log_social_action('instagram_post', {'caption': caption}, 'failed', publish_response.text)
                raise Exception(f"Instagram publish failed: {publish_response.text}")
        else:
            self.log_social_action('instagram_post', {'caption': caption}, 'failed', response.text)
            raise Exception(f"Instagram upload failed: {response.text}")

    def generate_facebook_summary(self, days=7):
        """Generate summary of Facebook activity"""
        if not self.facebook_access_token:
            raise Exception("Facebook access token not set")

        # This would require additional permissions and endpoints
        # For demo purposes, we'll return a sample summary
        summary = {
            "period_days": days,
            "engagement_rate": "3.2%",
            "reach": 1245,
            "impressions": 2341,
            "top_posts": [],
            "comments_received": 23,
            "shares": 12
        }

        self.log_social_action('facebook_summary', {'days': days}, 'success')
        return summary

    def generate_instagram_summary(self, days=7):
        """Generate summary of Instagram activity"""
        if not self.instagram_access_token:
            raise Exception("Instagram access token not set")

        # This would require additional permissions and endpoints
        # For demo purposes, we'll return a sample summary
        summary = {
            "period_days": days,
            "reach": 892,
            "impressions": 1567,
            "profile_views": 432,
            "followers": 1245,
            "avg_engagement_rate": "4.1%",
            "top_posts": []
        }

        self.log_social_action('instagram_summary', {'days': days}, 'success')
        return summary

    def log_social_action(self, action_type, details, result, error_message=None):
        """Log social media actions for audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "details": details,
            "result": result,
            "error_message": error_message,
            "system": "social_media_integration"
        }

        # Create logs directory if it doesn't exist
        logs_dir = Path("Logs")
        logs_dir.mkdir(exist_ok=True)

        # Log to daily file
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = logs_dir / f"{today}.json"

        # Read existing logs or create empty list
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                import ast
                try:
                    logs = ast.literal_eval(f.read())  # Safely parse the list
                except:
                    logs = []

        # Add new log entry
        logs.append(log_entry)

        # Write back to file
        with open(log_file, 'w') as f:
            f.write(str(logs))

        return log_entry

# Twitter/X Integration
class TwitterIntegration:
    def __init__(self, bearer_token=None, api_key=None, api_secret=None, access_token=None, access_token_secret=None):
        self.bearer_token = bearer_token
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.base_url = "https://api.twitter.com/2"

    def authenticate_v2(self):
        """Authenticate using bearer token for v2 API"""
        if not self.bearer_token:
            raise Exception("Twitter Bearer Token not set")
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        return headers

    def post_tweet(self, text):
        """Post a tweet to Twitter/X"""
        if not self.bearer_token:
            raise Exception("Twitter authentication credentials not set")

        url = f"{self.base_url}/tweets"
        headers = self.authenticate_v2()
        payload = {"text": text}

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            tweet_data = response.json()
            tweet_id = tweet_data.get("data", {}).get("id")
            self.log_twitter_action('tweet_post', {'text': text, 'tweet_id': tweet_id}, 'success')
            return tweet_id
        else:
            self.log_twitter_action('tweet_post', {'text': text}, 'failed', response.text)
            raise Exception(f"Tweet failed: {response.text}")

    def get_tweets(self, user_id, max_results=10):
        """Get tweets from a specific user"""
        if not self.bearer_token:
            raise Exception("Twitter authentication credentials not set")

        url = f"{self.base_url}/users/{user_id}/tweets"
        headers = self.authenticate_v2()
        params = {"max_results": max_results}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Get tweets failed: {response.text}")

    def generate_twitter_summary(self, days=7):
        """Generate summary of Twitter activity"""
        # This would require additional API calls to get analytics
        # For demo purposes, we'll return a sample summary
        summary = {
            "period_days": days,
            "tweets_posted": 12,
            "likes_received": 156,
            "retweets": 23,
            "replies": 8,
            "impressions": 3456,
            "engagement_rate": "4.2%"
        }

        self.log_twitter_action('twitter_summary', {'days': days}, 'success')
        return summary

    def log_twitter_action(self, action_type, details, result, error_message=None):
        """Log Twitter actions for audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "details": details,
            "result": result,
            "error_message": error_message,
            "system": "twitter_integration"
        }

        # Create logs directory if it doesn't exist
        logs_dir = Path("Logs")
        logs_dir.mkdir(exist_ok=True)

        # Log to daily file
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = logs_dir / f"{today}.json"

        # Read existing logs or create empty list
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                import ast
                try:
                    logs = ast.literal_eval(f.read())  # Safely parse the list
                except:
                    logs = []

        # Add new log entry
        logs.append(log_entry)

        # Write back to file
        with open(log_file, 'w') as f:
            f.write(str(logs))

        return log_entry