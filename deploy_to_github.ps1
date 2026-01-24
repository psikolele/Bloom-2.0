# Deploy Bloom 2.0 to GitHub

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Git is not installed." -ForegroundColor Red
    exit 1
}

# Check if gh CLI is installed
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "Error: GitHub CLI (gh) is not installed." -ForegroundColor Red
    exit 1
}

if (Test-Path .git) {
    Write-Host "Git already initialized. Pushing to Bloom-2.0..." -ForegroundColor Green
    git add .
    git commit -m "Update Bloom 2.0 Integrated App"
    git push origin main
} else {
    Write-Host "Initializing Bloom 2.0 Repository..." -ForegroundColor Green
    git init
    git add .
    git commit -m "Initial commit - Bloom 2.0 Integrated Suite"
    # Create private repo by default? User asked for "Bloom Versione 2.0". I'll call it Bloom-2.0
    gh repo create Bloom-2.0 --public --source=. --remote=origin --push
}

if ($?) {
    Write-Host "Successfully deployed Bloom 2.0!" -ForegroundColor Green
    Start-Process "https://github.com/$(gh api user -q .login)/Bloom-2.0"
} else {
    Write-Host "Deployment failed." -ForegroundColor Red
}

Read-Host -Prompt "Press Enter to exit"
