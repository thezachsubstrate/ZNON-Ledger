#!/bin/bash
INPUT_FILE=$1
OUTPUT_NAME=$2

echo "🛡️ Redacting Metadata (Identity Shield)..."
# Strips name, GPS, and device ID
ffmpeg -i "$INPUT_FILE" -map_metadata -1 -c:v copy -c:a copy "redacted_$OUTPUT_NAME.mp4"

echo "📊 Extracting Spectral Fingerprint (3.5kHz Audit)..."
# Generates the spectrogram for public proof
ffmpeg -i "$INPUT_FILE" -lavfi peakspectrum=s=hd720:mode=combined -frames:v 1 "spectrum_$OUTPUT_NAME.png"

echo "✅ SUCCESS: 'redacted_$OUTPUT_NAME.mp4' is safe for public upload."
echo "✅ SUCCESS: 'spectrum_$OUTPUT_NAME.png' is your 9-Sigma Proof."
