$folderPath = "."
Get-ChildItem $folderPath |
ForEach-Object {
    $filePath = $_.FullName
    $regex = "^(137314|147306|147314|306|314[0-9]{4})"
    $des_dev_list = "shpgw018-vg3945 shpgw011-vg3945 cnrgw001-vg4451 cnrgw002-vg4451 csfgw005-vg4451 csfgw006-vg4451"
    $csv_data = Import-Csv $filePath 
    $csv_data | ForEach-Object {
        $bf_test =  ($des_dev_list.contains($_.destDeviceName))
        if ($_.lastRedirectDn -match $regex -or $bf_test) {
            $_.callingPartyNumber="***********"
        }
        $_
    } | Export-Csv $filePath -NoTypeInformation
}
