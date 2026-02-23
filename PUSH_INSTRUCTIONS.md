# Push to GitHub (medphys23/campania_transplant)

Follow these steps **in order** so Git uses your new token.

---

## 1. Confirm the repo in the browser

- Log in to GitHub as **medphys23**.
- Open: https://github.com/medphys23/campania_transplant
- If you get **404**, create the repo: https://github.com/new → name: `campania_transplant` → Create repository (leave it empty).

---

## 2. Clear old GitHub credentials (Windows)

Otherwise Windows may keep using an old password or the wrong account.

1. Press **Windows key**, type **Credential Manager**, open it.
2. Click **Windows Credentials**.
3. Under **Generic Credentials**, find any entry for **git:https://github.com** (or **github.com**).
4. Open it → **Remove**.

---

## 3. Check your token scope

- Go to: https://github.com/settings/tokens
- Open the token you use for push.
- It must have **repo** (or **Full control of private repositories**) checked. If not, create a new token with **repo** and use that one.

---

## 4. Push using the token

Open **PowerShell** or **Command Prompt** and run:

```powershell
cd "g:\My Drive\General Surgery\HBP\transplant"
git push -u origin main
```

When prompted:

- **Username:** `medphys23`
- **Password:** paste your **new** Personal Access Token (not your GitHub password).

Git will not show the password as you paste; that’s normal.

---

## 5. If it still says "repository not found"

Try pushing with the token in the URL **once** (replace `YOUR_NEW_TOKEN` with your actual token, then run and **delete this line from the file after**):

```powershell
git push https://medphys23:YOUR_NEW_TOKEN@github.com/medphys23/campania_transplant.git main
```

**Do not commit this file or share it**—it would expose the token. After push works, set the remote back to the normal URL:

```powershell
git remote set-url origin https://github.com/medphys23/campania_transplant.git
```

Then you can delete this instruction file if you like.
