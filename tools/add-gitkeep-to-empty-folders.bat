@echo off
REM Filename: add-gitkeep-to-empty-folders.bat
REM Add .gitkeep files to all empty directories in the repository

powershell -ExecutionPolicy Bypass -Command ^
"Write-Host 'Scanning for empty directories...' -ForegroundColor Cyan; ^
$emptyDirs = Get-ChildItem -Path . -Recurse -Directory ^| Where-Object { ^
    (Get-ChildItem $_.FullName -Force ^| Where-Object { $_.Name -ne '.gitkeep' }).Count -eq 0 ^
}; ^
if ($emptyDirs.Count -eq 0) { ^
    Write-Host 'No empty directories found that need .gitkeep files.' -ForegroundColor Yellow; ^
} else { ^
    Write-Host \"Found $($emptyDirs.Count) empty directory(ies). Adding .gitkeep files...\" -ForegroundColor Green; ^
    foreach ($dir in $emptyDirs) { ^
        $gitkeepPath = Join-Path $dir.FullName '.gitkeep'; ^
        if (-not (Test-Path $gitkeepPath)) { ^
            New-Item -ItemType File -Path $gitkeepPath -Force ^| Out-Null; ^
            $relativePath = Resolve-Path -Relative $dir.FullName; ^
            Write-Host \"  Added .gitkeep to: $relativePath\" -ForegroundColor White; ^
        } else { ^
            $relativePath = Resolve-Path -Relative $dir.FullName; ^
            Write-Host \"  .gitkeep already exists in: $relativePath\" -ForegroundColor Gray; ^
        } ^
    } ^
    Write-Host \"`nAll empty directories now have .gitkeep files!\" -ForegroundColor Green; ^
}; ^
Write-Host \"`nYou can now run:\" -ForegroundColor Yellow; ^
Write-Host \"  git add .\" -ForegroundColor White; ^
Write-Host \"  git commit -m 'Add .gitkeep files to maintain folder structure'\" -ForegroundColor White; ^
Write-Host \"  git push origin main\" -ForegroundColor White"

pause