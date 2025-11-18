#!/bin/bash
# Create GitHub issues from roadmap markdown files
# Usage: bash roadmap/create-issues.sh

set -e

echo "Creating GitHub issues from roadmap files..."
echo ""

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub."
    echo "Run: gh auth login"
    exit 1
fi

# Array of files with their labels
declare -A issue_labels
issue_labels["01-testing-infrastructure.md"]="priority: high,effort: medium,category: testing,can-parallelize"
issue_labels["02-ci-cd-pipeline.md"]="priority: high,effort: small,category: devops"
issue_labels["03-documentation-improvements.md"]="priority: high,effort: medium,category: documentation,can-parallelize,good-first-issue"
issue_labels["04-code-quality-fixes.md"]="priority: medium,effort: small,category: code-quality,can-parallelize,good-first-issue"
issue_labels["05-linting-configuration.md"]="priority: medium,effort: small,category: tooling,can-parallelize"
issue_labels["06-type-checking-configuration.md"]="priority: medium,effort: small,category: tooling,can-parallelize"
issue_labels["07-improve-docstrings.md"]="priority: low,effort: medium,category: documentation,can-parallelize,good-first-issue"
issue_labels["08-dependency-management.md"]="priority: low,effort: small,category: configuration,can-parallelize"
issue_labels["09-environment-configuration.md"]="priority: low,effort: small,category: configuration,can-parallelize,good-first-issue"
issue_labels["10-notebook-organization.md"]="priority: low,effort: small,category: documentation,can-parallelize,good-first-issue"
issue_labels["11-package-structure-improvements.md"]="priority: low,effort: medium,category: architecture"

# Find all markdown files except README
for file in roadmap/[0-9]*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")

        # Extract title from first heading in file
        title=$(grep -m 1 "^# " "$file" | sed 's/^# //' | sed 's/Issue: //')

        if [ -z "$title" ]; then
            # Fallback: create title from filename
            title=$(basename "$file" .md | sed 's/^[0-9]*-//' | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
        fi

        # Get labels for this file
        labels="${issue_labels[$filename]}"

        echo "Creating issue: $title"
        echo "  Labels: $labels"

        # Create the issue
        issue_url=$(gh issue create \
            --title "$title" \
            --body-file "$file" \
            --label "$labels" 2>&1)

        if [ $? -eq 0 ]; then
            echo "  ✅ Created: $issue_url"
        else
            echo "  ❌ Failed to create issue"
            echo "  Error: $issue_url"
        fi
        echo ""
    fi
done

echo "✅ All issues created!"
echo ""
echo "View issues: gh issue list"
echo "View in browser: gh issue list --web"
