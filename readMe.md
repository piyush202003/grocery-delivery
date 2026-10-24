- temporary: 
    ```powershell 
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
    ```
- permanent: 
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```