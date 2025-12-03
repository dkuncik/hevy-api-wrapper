#!/usr/bin/env pwsh
# Check if Python code needs formatting

Write-Host "🔍 Checking code formatting..." -ForegroundColor Cyan

$exitCode = 0

Write-Host "`n📦 Checking isort..." -ForegroundColor Yellow
poetry run isort --check-only src/ tests/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ isort check failed" -ForegroundColor Red
    $exitCode = 1
} else {
    Write-Host "✅ isort check passed" -ForegroundColor Green
}

Write-Host "`n🖤 Checking black..." -ForegroundColor Yellow
poetry run black --check src/ tests/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ black check failed" -ForegroundColor Red
    $exitCode = 1
} else {
    Write-Host "✅ black check passed" -ForegroundColor Green
}

if ($exitCode -ne 0) {
    Write-Host "`n💡 Run './scripts/format.ps1' to fix formatting issues" -ForegroundColor Yellow
    exit $exitCode
} else {
    Write-Host "`n✅ All formatting checks passed!" -ForegroundColor Green
}
