#!/bin/bash

# PenTest C2 Dashboard - GitHub Setup Script
# Script لإعداد Git ورفع المشروع على GitHub تلقائياً

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🚀 GitHub Setup Script                                  ║"
echo "║   إعداد ورفع المشروع على GitHub                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if git is installed
echo -e "${BLUE}[*]${NC} Checking git installation..."
if ! command -v git &> /dev/null; then
    echo -e "${RED}[!]${NC} Git is not installed!"
    echo -e "${YELLOW}[+]${NC} Installing git..."
    sudo apt update && sudo apt install git -y
fi
echo -e "${GREEN}[✓]${NC} Git is installed"
echo ""

# Git configuration
echo -e "${BLUE}[*]${NC} Configuring git..."
read -p "Enter your name: " git_name
read -p "Enter your email: " git_email

git config --global user.name "$git_name"
git config --global user.email "$git_email"
echo -e "${GREEN}[✓]${NC} Git configured"
echo ""

# Create .gitignore
echo -e "${BLUE}[*]${NC} Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.log

# Flask
instance/
.webassets-cache

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Custom
logs/
*.db
.env

# Sensitive
config_local.py
EOF
echo -e "${GREEN}[✓]${NC} .gitignore created"
echo ""

# Security warning about password
echo -e "${YELLOW}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║   ⚠️  SECURITY WARNING                                    ║${NC}"
echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${RED}[!]${NC} The current password in the code is: ${YELLOW}hamza_sku_2026${NC}"
echo ""
echo "Do you want to change it before uploading to GitHub?"
echo "1) Yes, change to generic password (recommended for public repos)"
echo "2) No, keep current password (only for private repos)"
read -p "Choice [1/2]: " change_password

if [ "$change_password" = "1" ]; then
    echo -e "${BLUE}[*]${NC} Changing password to generic value..."
    
    # Backup original file
    cp pentest_dashboard.py pentest_dashboard.py.backup
    
    # Change password in code
    sed -i 's/MASTER_PASSWORD = "hamza_sku_2026"/MASTER_PASSWORD = "change_me_in_production"/' pentest_dashboard.py
    
    echo -e "${GREEN}[✓]${NC} Password changed to: ${YELLOW}change_me_in_production${NC}"
    echo -e "${YELLOW}[!]${NC} Original file backed up as: pentest_dashboard.py.backup"
    echo ""
fi

# Initialize git repository
echo -e "${BLUE}[*]${NC} Initializing git repository..."
if [ -d .git ]; then
    echo -e "${YELLOW}[!]${NC} Git repository already exists"
else
    git init
    echo -e "${GREEN}[✓]${NC} Git repository initialized"
fi
echo ""

# Add files
echo -e "${BLUE}[*]${NC} Adding files to git..."
git add .
echo -e "${GREEN}[✓]${NC} Files added"
echo ""

# Commit
echo -e "${BLUE}[*]${NC} Creating initial commit..."
git commit -m "🚀 Initial commit: PenTest C2 Dashboard with authentication

Features:
- Secure login system with SHA-256 encryption
- Real-time dashboard with WebSocket
- Command execution terminal
- System monitoring (CPU, Memory, Uptime)
- Comprehensive logging system
- Professional Cyberpunk UI design

Security:
- Password protected access
- Session management
- Login attempt tracking
- Protected API endpoints
"
echo -e "${GREEN}[✓]${NC} Initial commit created"
echo ""

# GitHub repository
echo -e "${BLUE}[*]${NC} Setting up GitHub repository..."
echo ""
echo "Please create a new repository on GitHub:"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: pentest-c2-dashboard"
echo "3. Description: Advanced PenTest C2 Dashboard"
echo "4. Choose: Public or Private (Private recommended)"
echo "5. Do NOT add README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""
read -p "Press Enter when you've created the repository..."
echo ""

# Get GitHub username and repo
read -p "Enter your GitHub username: " github_username
read -p "Enter repository name [pentest-c2-dashboard]: " repo_name
repo_name=${repo_name:-pentest-c2-dashboard}

# Add remote
echo -e "${BLUE}[*]${NC} Adding GitHub remote..."
git_url="https://github.com/${github_username}/${repo_name}.git"

if git remote | grep -q "origin"; then
    echo -e "${YELLOW}[!]${NC} Remote 'origin' already exists, removing..."
    git remote remove origin
fi

git remote add origin "$git_url"
echo -e "${GREEN}[✓]${NC} Remote added: $git_url"
echo ""

# Push to GitHub
echo -e "${BLUE}[*]${NC} Pushing to GitHub..."
echo ""
echo -e "${YELLOW}[!]${NC} You will be asked for credentials:"
echo "    Username: Your GitHub username"
echo "    Password: Your Personal Access Token (NOT your GitHub password)"
echo ""
echo "If you don't have a token:"
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Click 'Generate new token' > 'Generate new token (classic)'"
echo "3. Select scopes: ✓ repo (all)"
echo "4. Generate and copy the token"
echo ""
read -p "Press Enter to continue..."
echo ""

# Set default branch to main
git branch -M main

# Push
if git push -u origin main; then
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   ✅ Successfully pushed to GitHub!                       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}[✓]${NC} Your project is now available at:"
    echo -e "    ${BLUE}https://github.com/${github_username}/${repo_name}${NC}"
    echo ""
    
    # Save credentials
    read -p "Do you want to save credentials for future pushes? [y/n]: " save_creds
    if [ "$save_creds" = "y" ]; then
        git config --global credential.helper store
        echo -e "${GREEN}[✓]${NC} Credentials will be saved after next push"
    fi
else
    echo ""
    echo -e "${RED}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   ❌ Failed to push to GitHub                            ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}[!]${NC} Common issues:"
    echo "    - Wrong username or token"
    echo "    - Repository doesn't exist"
    echo "    - No internet connection"
    echo ""
fi

echo ""
echo -e "${BLUE}[*]${NC} Setup complete!"
echo ""
echo "Next steps:"
echo "1. Visit your repository on GitHub"
echo "2. Add a description and tags"
echo "3. Consider making it Private if it contains sensitive info"
echo ""
echo "To update in the future:"
echo "  git add ."
echo "  git commit -m 'Your commit message'"
echo "  git push origin main"
echo ""
