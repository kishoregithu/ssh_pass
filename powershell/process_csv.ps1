$filePath = 
Import-Csv $filePath | Select-Object $desiredColumnsSystem | Sort RESOURCEID -Unique | ForEach-Object {
            If ($_.USER_NAME -match $Regex) {
                $_.USER_NAME = $_.USER_NAME -replace $Regex,''
            }
            $_
        } |
        Export-Csv -Path $System –NoTypeInformation
