$filePath = test.csv
Import-Csv $filePath | ForEach-Object {
    if ($_.Enabled -eq 'True') {
        $_.Enabled = 'A'
    }
    $_
} | Export-Csv .\test-modified.csv -NoTypeInformation
