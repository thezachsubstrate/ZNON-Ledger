#!/bin/bash
TERM_NAME=$1
DEFINITION=$2
CATEGORY=$3

# Append to the MedStrate specific glossary
sed -i '$d' substrate/modules/medstrate/GLOSSARY.znon
echo "  ," >> substrate/modules/medstrate/GLOSSARY.znon
echo "  {" >> substrate/modules/medstrate/GLOSSARY.znon
echo "    \"term\": \"$TERM_NAME\"," >> substrate/modules/medstrate/GLOSSARY.znon
echo "    \"definition\": \"$DEFINITION\"," >> substrate/modules/medstrate/GLOSSARY.znon
echo "    \"category\": \"$CATEGORY\"," >> substrate/modules/medstrate/GLOSSARY.znon
echo "    \"jurisdiction\": \"MEDSTRATE\"" >> substrate/modules/medstrate/GLOSSARY.znon
echo "  }" >> substrate/modules/medstrate/GLOSSARY.znon
echo "]" >> substrate/modules/medstrate/GLOSSARY.znon

./automanifest.sh
git add .
git commit -m "MedStrate Update: Added $TERM_NAME to Clinical Glossary"
git push
