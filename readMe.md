##### For installtion
- Download code 
- create 'uv' vertual environment
- Add all libraries listed in requiremet.txt file

##### Environment variables
- ADMIN_MAILS
- For map implementation
  - RAZORPAY_KEY_SECRET
- For Online payments
  - RAZORPAY_KEY_ID
  - RAZORPAY_KEY_SECRET

##### To Start the Project
- Run this commands in different terminals
```powershell
  python manage.py tailwind start
```
```powershell
  python manage.py runserver
```

- To run in mobile:
  - get IPv4 address from laptop and connect all devices to same wifi
  - to get IPv4 ip address run this in terminal:
    ```powershell
    ipconfig
    ```
  - Then add that IPv4 address in .env for ALLOWED_HOSTS
  - run this command on terminal to start the project
    ```powershell
    python manage.py runserver 0.0.0.0:8000
    ```

##### Other things
- Current Flawas
  - Email authentication and forgot password
  - Multiple phone numbers or to assign different phone numbers
  - need to solve order current status problem and reassiging of delivery partner
  - 
- Future Improvements