---
description: publish changes to github without approval
---

// turbo-all

1. Stage all changes
```powershell
git add .
```

2. Commit changes with a generic message (or ask for one)
```powershell
git commit -m "Automated update"
```

3. Push to origin main
```powershell
git push origin main
```
