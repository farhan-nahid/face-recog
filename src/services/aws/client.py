import boto3
from botocore.config import Config
from core.settings import settings

# Configure retry logic and connection pooling with adaptive retry mode
aws_config = Config(
    retries={
        "max_attempts": 10,
        "mode": "adaptive",  # Adaptive mode adjusts retry behavior based on errors
    },
    connect_timeout=10,  # Increased for better connectivity
    read_timeout=60,  # Increased for larger responses
    max_pool_connections=50,
    tcp_keepalive=True,  # Enable TCP keepalive to prevent connection drops
)

rekognition_client = boto3.client(
    "rekognition",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
    config=aws_config,
)


sts_client = boto3.client(
    "sts",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
    config=aws_config,
)
