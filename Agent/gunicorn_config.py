"""
Gunicorn configuration file for the Insurance project.
"""

import multiprocessing

# Bind to 127.0.0.1:8000
bind = "127.0.0.1:8000"

# Number of worker processes
# A good rule of thumb is 2-4 x number of CPU cores
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "gthread"

# Number of threads per worker
threads = 2

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

# Timeout (in seconds)
timeout = 120

# Access log file
accesslog = "/var/log/gunicorn/access.log"

# Error log file
errorlog = "/var/log/gunicorn/error.log"

# Log level
loglevel = "info"

# Process name
proc_name = "insurance"

# Preload application code before forking workers
preload_app = True

# Daemonize the Gunicorn process (run in background)
daemon = False  # We'll use systemd to manage the process

# User and group to run as
user = None  # Set this to your user
group = None  # Set this to your group

# Directory to store the pid file
pidfile = "/var/run/gunicorn/insurance.pid"

# Create directories for logs and pid file
import os
os.makedirs("/var/log/gunicorn", exist_ok=True)
os.makedirs("/var/run/gunicorn", exist_ok=True)
