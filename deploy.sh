#!/usr/bin/env bash
# ============================================================================
#  জাপানি চা পানি — GitHub-এ পুশ করার সহজ স্ক্রিপ্ট
#
#  ব্যবহার:
#      bash deploy.sh https://github.com/আপনার-ইউজারনেম/রিপো-নাম.git
#
#  আগে GitHub-এ একটা খালি রিপো খুলে নিন (README ছাড়া), তারপর উপরের কমান্ড চালান।
# ============================================================================
set -e

REPO="$1"

if [ -z "$REPO" ]; then
  echo "❌ রিপোর ঠিকানা দেননি।"
  echo "   ব্যবহার: bash deploy.sh https://github.com/USERNAME/REPO.git"
  exit 1
fi

cd "$(dirname "$0")"

# git সেটআপ না থাকলে বসিয়ে নেওয়া
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "→ git repo তৈরি করা হচ্ছে"; git init -q -b main; }
git config user.name  >/dev/null 2>&1 || git config user.name "জাপানি চা পানি"
git config user.email >/dev/null 2>&1 || git config user.email "shop@japanichaapani.local"

git add -A
git diff --cached --quiet || git commit -q -m "জাপানি চা পানি ওয়েবসাইট"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REPO"
else
  git remote add origin "$REPO"
fi

echo "→ পুশ করা হচ্ছে: $REPO"
git push -u origin main

echo
echo "✅ হয়ে গেছে!"
echo
echo "এখন GitHub-এ এই দুটি কাজ করুন (একবারই):"
echo "  1) Settings → Pages → Source: GitHub Actions  (অটো ডিপ্লয়ের জন্য)"
echo "  2) Actions ট্যাবে ডিপ্লয় শেষ হলে লিংক পাবেন:"
echo "     https://<ইউজারনেম>.github.io/<রিপো-নাম>/"
