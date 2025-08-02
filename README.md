# Exchange V2

---

## 🚀 Launch

1. **Cloning repository**
   - Make sure you have [git](https://git-scm.com/downloads) installed
   - Open any shell on your machine
   - Clone repository
     ```
     git clone {repository url}  
     ```
   - Change current directory to created one
     ```
     cd {repository name}
     ```

2. **Environment variables setup**
   - Via code editor you need to create .env file in **backend** folder
   - You can use example-env.txt template to create it

3. **Installing and activating virtual environment**
   - Make sure that you have [uv](https://github.com/astral-sh/uv)
   - and any [python interpreter](https://www.python.org/downloads/) installed
   - Create virtual environment:
     ```
     uv venv
     ```
   - Activate your environment
     - Windows:
       ```
       .venv\Scripts\activate
       ```
     - Linux/macOS:
       ```
       source .venv/bin/activate
       ```
     - After this you can install all dependencies
       ```
       uv sync
       ```
   - To change python version you can use
    ```
    uv python pin {version} # 3.12 version by default
    ```
    To change version below **3.10** you will need to change field **required-python** in **pyproject.toml** file
    and after to do command upper

4. **Database setup**
   - To create all tables and db structure use
    ```
    alembic upgrade head
    ```
    or:
    ```
    uv run alembic upgrade head
    ```

5. **.pem keys setup**
   - For authorization and authentication on api you need to create public and private keys for jwt tokens
   - Make sure that you have openssl installed
    ```
    mkdir backend/src/keys
    ```
    ```
    openssl genpkey -algorithm RSA -out backend/src/keys/private_key.pem
    ```
    ```
    openssl rsa -in backend/src/keys/private_key.pem -pubout -out backend/src/keys/public_key.pem
    ```

6. **Backend setup**
   - Change current directory to "backend"
    ```
    cd backend
    ```
   - Install all mock data for database
    ```
    python -m scripts.db.data
    ```
    or:
    ```
    uv run python -m scripts.db.data
    ```

7. **Backend Launch**
   - To run app use
    ```
    python main.py
    ```
    or:
    ```
    uv run python main.py
    ```

8. **Backend logs checking**      
   - In **logs** folder you will find logs file for backend

9.  **Frontend setup**
   - You need to open another shell and change directory to **frontend**
   - Make sure that you have node installed
   - After you can use following commands
    ```
    cd frontend
    ```
    ```
    npm install
    ```
    ```
    npm run dev
    ```

---

# Great job! Enjoy!
