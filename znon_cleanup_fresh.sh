#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ZNON-Ledger

echo "→ Resetting repository state..."
git fetch origin
git reset --hard origin/main

GLOSSARY="core/GLOSSARY.md"
README="README.md"

echo "→ Cleaning Glossary..."

# 1. Remove injected command/script lines at top
sed -i '/^# Paste in the Multimodal Extension Addendum section/,+10d' "$GLOSSARY"
sed -i '/^#5 – Stage and commit the changes/,+10d' "$GLOSSARY"

# 2. Normalize Audit Parity header
sed -i 's/[0-9][0-9]\/[0-9][0-9]/53\/53/' "$GLOSSARY"
sed -i 's/43\/43/53\/53/' "$GLOSSARY"

# 3. Remove duplicate Multimodal Addendum blocks, keep first only
awk '
BEGIN {keep=1}
/^## V\. Multimodal Extension Addendum/ { 
  if (seen++) keep=0 
}
keep {print}
/^620\. Multimodal Integrity Index/ {
  keep=1
}
' "$GLOSSARY" > /tmp/glossary_clean.md
mv /tmp/glossary_clean.md "$GLOSSARY"

# 4. Trim blank lines and tidy spacing
sed -i '/^[[:space:]]*$/N;/^\n$/D' "$GLOSSARY"

echo "→ Cleaning README..."
# Remove automation noise at bottom
sed -i '/### Updated Glossary/,+5d' "$README"
sed -i '/Includes Multimodal Extension Addendum/,+3d' "$README"

echo "→ Committing results..."
git add "$GLOSSARY" "$README"
git commit -m "Canonically clean Glossary & README (53/53 Audit Parity, remove dup Addendum, strip injected text)"
git push origin main

echo "✅ ZNON cleanup complete – repository normalized and pushed."

