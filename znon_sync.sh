#!/bin/bash
# 1. Update the Glossary
TERM_NAME=$1
DEFINITION=$2

echo "Appending $TERM_NAME to Glossary..."
cat <<NEW_TERM >> substrate/meaning_layer/GLOSSARY.znon
{
  "term": "$TERM_NAME",
  "definition": "$DEFINITION",
  "timestamp": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
}
NEW_TERM

# 2. Run the existing auto-manifest to anchor everything
./automanifest.sh

# 3. Final Push to GitHub
git add .
git commit -m "ZNON Update: Added $TERM_NAME to Substrate"
git push
