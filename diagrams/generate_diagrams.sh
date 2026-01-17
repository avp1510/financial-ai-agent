#!/bin/bash

# Script to generate all architecture diagrams
# Usage: ./generate_diagrams.sh [format]
# format: png (default), svg, or both

set -e

FORMAT=${1:-png}

echo "Generating PlantUML diagrams..."

if [ "$FORMAT" = "svg" ]; then
    echo "Generating SVG diagrams..."
    plantuml -tsvg *.puml
    echo "SVG diagrams generated successfully"
elif [ "$FORMAT" = "both" ]; then
    echo "Generating PNG diagrams..."
    plantuml *.puml
    echo "Generating SVG diagrams..."
    plantuml -tsvg *.puml
    echo "All diagrams generated successfully"
else
    echo "Generating PNG diagrams..."
    plantuml *.puml
    echo "PNG diagrams generated successfully"
fi

echo "Available diagrams:"
ls -la *.png *.svg 2>/dev/null | head -10 || echo "No diagram files found"

echo ""
echo "To view diagrams:"
echo "  PNG: Open *.png files in any image viewer"
echo "  SVG: Open *.svg files in web browser"
echo "  Online: Visit https://www.plantuml.com/plantuml/"
