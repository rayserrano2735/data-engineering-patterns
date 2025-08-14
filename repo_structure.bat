@echo off
REM Create dbt-patterns folder structure with .gitkeep files

powershell -ExecutionPolicy Bypass -Command ^
"$folders = @('dbt-patterns\macros', 'dbt-patterns\models\staging', 'dbt-patterns\models\intermediate', 'dbt-patterns\models\marts', 'dbt-patterns\tests'); ^
foreach ($folder in $folders) { ^
    New-Item -ItemType Directory -Path $folder -Force ^| Out-Null; ^
    New-Item -ItemType File -Path \"$folder\.gitkeep\" -Force ^| Out-Null; ^
    Write-Host \"Created: $folder with .gitkeep\" -ForegroundColor Green; ^
}; ^
Write-Host \"`nFolder structure created successfully!\" -ForegroundColor Cyan; ^
Write-Host \"You can now run:\" -ForegroundColor Yellow; ^
Write-Host \"  git add dbt-patterns/\" -ForegroundColor White; ^
Write-Host \"  git commit -m 'Add dbt patterns folder structure'\" -ForegroundColor White; ^
Write-Host \"  git push origin main\" -ForegroundColor White"

pause