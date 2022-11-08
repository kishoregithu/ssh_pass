
$RegexPatterns = @("callid=[a-zA-Z0-9]{32}","_ani=[0-9]{10}", "_dnis=[0-9]{10}","dnis.[0-9]{10}","^?ani.[0-9]{10}","ani.[0-9]{10}","output\((VehicleIdentificationSerialNumber)\).[a-zA-Z0-9]{12}","Customer output\((VechicleIndentificationSerialNumber)\).[a-zA-Z0-9]{12}","output\((SSN)\).[0-9]{4}","SSN:,[0-9]{4}","accountNumber is* *\d{7}","accountNumber:,\d{7}","[Aa]ccount *[Nn]umber is *:* \d{7}","sKey,[0-9]{10}","ANI:::,[0-9]{10}","output\((SSN)\).[0-9]{4}", "account[Nn]umber..\d{8,9}", "financeCode.\d{4}","value: [a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}","ClientId\s.\s[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}","ClientSecret\s.\s.[a-zA-Z0-9]{21}_[a-zA-Z0-9]{5}-[a-zA-Z0-9]{11}","callid=[a-zA-Z0-9]{32}")

foreach ($pattern in $RegexPatterns)
{
$Content = Get-Content  $fileName 
$Matches = $Content  | Select-String -Pattern $RegexPattern -AllMatches
foreach ($Match in $Matches)
{
$Replace = $Match -replace '=[a-zA-Z0-9]{5}' '=*****'
$Content -replace $Match,$Replace
}
}
