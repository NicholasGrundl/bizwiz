#!/bin/bash
# Create GitHub labels for the BizWiz roadmap
# Usage: bash roadmap/create-labels.sh

set -e

echo "Creating GitHub labels for BizWiz roadmap..."
echo ""

# Priority labels
echo "Creating priority labels..."
gh label create "priority: high" --color d73a4a --description "High priority issues" --force 2>/dev/null || echo "  - priority: high (already exists)"
gh label create "priority: medium" --color fbca04 --description "Medium priority issues" --force 2>/dev/null || echo "  - priority: medium (already exists)"
gh label create "priority: low" --color 0e8a16 --description "Low priority issues" --force 2>/dev/null || echo "  - priority: low (already exists)"

# Effort labels
echo "Creating effort labels..."
gh label create "effort: small" --color c2e0c6 --description "< 1 day effort" --force 2>/dev/null || echo "  - effort: small (already exists)"
gh label create "effort: medium" --color bfd4f2 --description "1-2 days effort" --force 2>/dev/null || echo "  - effort: medium (already exists)"
gh label create "effort: large" --color f9d0c4 --description "> 2 days effort" --force 2>/dev/null || echo "  - effort: large (already exists)"

# Category labels
echo "Creating category labels..."
gh label create "category: testing" --color 0075ca --description "Testing related" --force 2>/dev/null || echo "  - category: testing (already exists)"
gh label create "category: documentation" --color 0075ca --description "Documentation improvements" --force 2>/dev/null || echo "  - category: documentation (already exists)"
gh label create "category: devops" --color 5319e7 --description "CI/CD and DevOps" --force 2>/dev/null || echo "  - category: devops (already exists)"
gh label create "category: code-quality" --color a2eeef --description "Code quality improvements" --force 2>/dev/null || echo "  - category: code-quality (already exists)"
gh label create "category: tooling" --color d876e3 --description "Development tooling" --force 2>/dev/null || echo "  - category: tooling (already exists)"
gh label create "category: configuration" --color bfdadc --description "Configuration and setup" --force 2>/dev/null || echo "  - category: configuration (already exists)"
gh label create "category: architecture" --color e99695 --description "Architectural changes" --force 2>/dev/null || echo "  - category: architecture (already exists)"

# Other labels
echo "Creating other labels..."
gh label create "can-parallelize" --color ededed --description "Can work on in parallel" --force 2>/dev/null || echo "  - can-parallelize (already exists)"
gh label create "good-first-issue" --color 7057ff --description "Good for newcomers" --force 2>/dev/null || echo "  - good-first-issue (already exists)"

echo ""
echo "✅ All labels created successfully!"
echo ""
echo "View labels: gh label list"
