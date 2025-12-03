#!/usr/bin/env pwsh
# Format all Python code with black and isort

Write-Host "🎨 Formatting Python code..." -ForegroundColor Cyan

Write-Host "`n📦 Running isort..." -ForegroundColor Yellow
poetry run isort src/ tests/

Write-Host "`n🖤 Running black..." -ForegroundColor Yellow
poetry run black src/ tests/

Write-Host "`n✅ Code formatting complete!" -ForegroundColor Green
Write-Host "Run 'git diff' to see the changes." -ForegroundColor Gray
