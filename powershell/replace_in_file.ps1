
$RegexPatterns = @("callid=[a-zA-Z0-9]{32}","_ani=[0-9]{10}", 
"_dnis=[0-9]{10}","dnis.[0-9]{10}",
"(^?ani.)([0-9]{5})([0-9]{5})",
"(ani.)([0-9]{5})([0-9]{5})",
"(output\((VehicleIdentificationSerialNumber)\).)([a-zA-Z0-9]{5})([a-zA-Z0-9]{7})",
"Customer output\((VechicleIndentificationSerialNumber)\).[a-zA-Z0-9]{12}",
"output\((SSN)\).[0-9]{4}",
"SSN:,[0-9]{4}",
"accountNumber is* *\d{7}",
"accountNumber:,\d{7}",
"[Aa]ccount *[Nn]umber is *:* \d{7}",
"sKey,[0-9]{10}",
"ANI:::,[0-9]{10}",
"output\((SSN)\).[0-9]{4}", 
"account[Nn]umber..\d{8,9}", 
"financeCode.\d{4}",
"value: [a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}",
"ClientId\s.\s[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}",
"ClientSecret\s.\s.[a-zA-Z0-9]{21}_[a-zA-Z0-9]{5}-[a-zA-Z0-9]{11}","callid=[a-zA-Z0-9]{32}")


$regexA = '(callid=)([a-zA-Z0-9]{5})([a-zA-Z0-9]{27})'
$regexB = '(_ani=)([0-9]{5})([0-9]{5})'

$regexs = @('(callid=)([a-zA-Z0-9]{5})([a-zA-Z0-9]{27})','(_ani=)([0-9]{5})([0-9]{5})')
Get-ChildItem -Path C:\temp\test\ '*.txt' | ForEach-Object {
  $c = (Get-Content $_.FullName)
  foreach ($regex in $regexs) {
    $c = ($c) -replace $regex,'${1}*****$3'
  }
  [IO.File]::WriteAllText($_.FullName, $c)
}

