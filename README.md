# User Management System

This project is a simple Python-based user management system that handles basic operations such as login, session tracking, and order management.  

# Features
- Stores user credentials and details (username, password, email, etc.)  
- Tracks session IDs and verification codes  
- Allows users to log in and maintain active sessions  
- Handles user preferences such as "likes" and order history  

# Files
- **main.py** – The core script that manages user authentication and session handling.  
- **allusers.txt** – A mock database containing user details (stored in a '|'separated format.  

## How to Run
1. Clone the repository:  
   ```bash
   git clone <your-repo-link>
   cd <repo-name>
Run the main script:

python main.py
The script will load users from allusers.txt and allow login/session operations.

## Example User Record

username|password|firstname|lastname|gender|age|email|address|verificationcode|likes|lastlogin|currenttoken|currentsessionid|orders
arjun|abcd1234|Arjun|Debnath|M|16|arjunsdebnath@gmail.com|Seattle, WA, 98039|DONE|donut|08/23/2023, 05:18:16|...


