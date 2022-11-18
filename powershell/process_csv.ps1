$folderPath = "."
Get-ChildItem $folderPath |
ForEach-Object {
    $filePath = $_.FullName
    $regex_ax = "^(137314|147306|147314|306|314)[0-9]{4}"
    $regex_az = "^CCAP1-(CHNDP|CNR|CSF|SHP)-(BLocal|BMobile|BNational|BSpecial|Emergency|PSTN|CMService|DNTrans|PSTNTrans|PhoneDN)-PT"
    $des_dev_list = "shpgw018-vg3945 shpgw011-vg3945 cnrgw001-vg4451 cnrgw002-vg4451 csfgw005-vg4451 csfgw006-vg4451 19.229.163.128 19.229.163.131 19.244.121.120 19.244.121.121 19.250.223.12 19.250.223.13"
    $csv_data = Import-Csv $filePath 
    $csv_data | ForEach-Object {
        $bf_test =  ($des_dev_list.contains($_.destDeviceName))
        if ($_.lastRedirectDn -match $regex_ax -or $bf_test) {
            $_.callingPartyNumber='*' * $_.callingPartyNumber.length 
        }
        if ($_.originalCalledPartyNumberPartition -match $regex_az -or $_.finalCalledPartyNumberPartition -match $regex_az) {
            $_.originalCalledPartyNumber='*' * $_.originalCalledPartyNumber.length 
            $_.finalCalledPartyNumber='*' * $_.finalCalledPartyNumber.length 
        }
        $_
    } | Export-Csv $filePath -NoTypeInformation
}
