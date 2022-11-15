

Clear-Host
Remove-Variable * -ErrorAction SilentlyContinue
Function Downloads{
    param(
        [String]$Location,
        [String]$Path,
        [String]$ServerName
    
    )
try{

$DtFilesToGet = (Get-date).AddDays(-2).Date
$Files = Get-ChildItem  $Location
#$Files = [System.IO.Directory]::GetFiles($Location, "*.txt")
#$Files = Copy-Item -Path $Location -Destination $Path -Recurse 
$flag=$false
if($Files.Length -gt 0){
Write-host "Downloading Files from the server" $ServerName
foreach ($item in $Files) 
{ 
$filepath=$Location+'\'+$item
    if ($item.LastWriteTime.Date -eq $DtFilesToGet)
      {
          Copy-Item -Path $filepath -Destination $Path -Recurse
          #Write-Host "Copying... $File"
          $flag=$True
      }
      else 
      {
          #Write-Host "$File Ignored"
      }

}
if($flag -eq $True){

$matched = Get-Matches $Path\*.txt
if($matched -gt 0){
 $n = $Path.Split('\')
 $foldertype = $n[10]
 $servername = $n[5]

$pattern = '[\\/]'
$logdate=$DtFilesToGet.ToString('yyyy-MM-dd')
$zipname = $foldertype+$logdate+'.zip'
$zipname = $zipname -replace $pattern, ''
#Write-Host $Path
#Get-Matches $Path\*.txt
#sleep 3
Compress-Archive -Path $Path -DestinationPath $Path\$zipname
# Write-Host $y++ -ForegroundColor DarkRed 
UplodadToNexus $servername $zipname $Path
}else{
#Write-Host "No matches found"
}
 }else{
 Write-Host "No files to download"
 }
 }
#Copy-Item -Path $Location -Destination $Path -Recurse
}catch{
Write-Error "Error while copying files from Remote Server" 
Write-Host $_.

return
}


}Function UplodadToNexus{
param(
[string]$servername,
[String]$uploadarchive,
[String]$folderloc
)
cd $folderloc
$packageName = $uploadarchive
$publishUrl="https://www.nexus.ford.com/repository/GUCCEA_private_raw_repository\Application\$servername\$packageName"
$username="YHVJrS-w"
$password="Bz7xrO5MsAUrpXlTyty9cY41Al940NhwVLfb_yoIJnhl"
$params = @{
  UseBasicParsing = $true
  Uri             = $publishUrl
  Method          = "PUT"
  InFile          = $packageName
  Headers         = @{
    ContentType   = "multipart/form-data"
    Authorization = "Basic $([System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("$username`:$password")))" 
  }
  Verbose         = $true
}
try{
$uplodstatus = Invoke-WebRequest @params
Write-Host $uplodstatus
}catch{
Write-error "Erro while uploading to Nexus"
Write-host $_.
}
}

Function MaskValues{
    param(

    [String]$val,
    [String]$sep,
    [String]$key
        )
    $k=""
$n=$val.Split($sep)

$maskdata = $n[1]
#Write-Host $maskdata
if($maskdata.length -ge 28){
    $k=$maskdata -replace $maskdata.Substring(0,12),'*************'
}elseif ($maskdata.length -ge 10) {
    $k=$maskdata -replace $maskdata.Substring(0,4),'****'
}
elseif ($maskdata.length -ge 8) {
    $k=$maskdata -replace $maskdata.Substring(0,4),'****'
}elseif ($maskdata.length -ge 8) {
    $k=$maskdata -replace $maskdata.Substring(0,13),'****'
}elseif ($maskdata.length -ge 36) {
    $k=$maskdata -replace $maskdata.Substring(0,3),'***'
}elseif ($maskdata.length -ge 3) {
    $k=$maskdata -replace $maskdata.Substring(0,2),'**'
}

$t=$n[0]+$sep+$k
return $t
}
Function Get-Matches
{
    Param(
        [Parameter(Mandatory,Position=0)]
        [String] $FoldersToCheck
    )

#$RegexPattern= @("callid=[a-zA-Z0-9]{32}")
$RegexPattern = @("callid=[a-zA-Z0-9]{32}","_ani=[0-9]{10}", "_dnis=[0-9]{10}","dnis.[0-9]{10}","^?ani.[0-9]{10}","ani.[0-9]{10}","output\((VehicleIdentificationSerialNumber)\).[a-zA-Z0-9]{12}","Customer output\((VechicleIndentificationSerialNumber)\).[a-zA-Z0-9]{12}","output\((SSN)\).[0-9]{4}","SSN:,[0-9]{4}","accountNumber is* *\d{7}","accountNumber:,\d{7}","[Aa]ccount *[Nn]umber is *:* \d{7}","sKey,[0-9]{10}","ANI:::,[0-9]{10}","output\((SSN)\).[0-9]{4}", "account[Nn]umber..\d{8,9}", "financeCode.\d{4}","value: [a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}","ClientId\s.\s[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}","ClientSecret\s.\s.[a-zA-Z0-9]{21}_[a-zA-Z0-9]{5}-[a-zA-Z0-9]{11}","callid=[a-zA-Z0-9]{32}")
#$RegexPattern= @("callid=[a-zA-Z0-9]{32}","_ani=[0-9]{10}", "_dnis=[0-9]{10}","dnis.[0-9]{10}","ani.[0-9]{10}","output\((VehicleIdentificationSerialNumber)\).[a-zA-Z0-9]{12}","Customer output\((VechicleIndentificationSerialNumber)\).[a-zA-Z0-9]{12}","output\((SSN)\).[0-9]{4}","SSN:,[0-9]{4}","accountNumber is* *\d{7}","accountNumber:,\d{7}","[Aa]ccount *[Nn]umber is *:* \d{7}","sKey,[0-9]{10}","ANI:::,[0-9]{10}","output\((SSN)\).[0-9]{4}", "account[Nn]umber..\d{8,9}", "financeCode.\d{4}","value: [a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}","ClientId\s.\s[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}","ClientSecret\s.\s.[a-zA-Z0-9]{21}_[a-zA-Z0-9]{5}-[a-zA-Z0-9]{11}","callid=[a-zA-Z0-9]{32}")
#$RegexPattern= @("dnis.[0-9]{10}","^?ani.[0-9]{10}","ani.[0-9]{10}","output\((VehicleIdentificationSerialNumber)\).[a-zA-Z0-9]{12}","Customer output\((VechicleIndentificationSerialNumber)\).[a-zA-Z0-9]{12}","output\((SSN)\).[0-9]{4}","SSN:,[0-9]{4}","ANI:::,[0-9]{10}","output\((SSN)\).[0-9]{4}","financeCode.\d{4}","ClientId\s.\s[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}","ClientSecret\s.\s.[a-zA-Z0-9]{21}_[a-zA-Z0-9]{5}-[a-zA-Z0-9]{11}")
#$RegexPattern= @("accountNumber is* *\d{7}","[Aa]ccount *[Nn]umber is *:* \d{7}","ani,*[0-9]{10}", "_ani=[0-9]{10}", "_dnis=[0-9]{10}", "dnis.[0-9]{10}", "sKey,[0-9]{10}", "ani=[0-9]{10}", "ANI:::,[0-9]{10}", "account[Nn]umber..\d{8,9}", "financeCode.\d{4}", "Customer output\((SSN)\).[0-9]{4")  
#$RegexPattern= @("Customer output\((SSN)\).[0-9]{4}")  
#$RegexPattern= @("accountNumber is* *\d{7}","callid=([0-9A-Z]{32,32})","[Aa]ccount *[Nn]umber is *:* \d{7}","\[(.*)\]","\((.*)\)","ani,*[0-9]{10}", "_ani=[0-9]{10}","_dnis=[0-9]{10}", "dnis=[0-9]{10}", "ani=[0-9]{10}", "ANI:::,[0-9]{10}", "account[Nn]umber..\d{8,9}")
#Get-ChildItem $FoldersToCheck -Recurse | ForEach {
write-host ('get-matches')
       # $FilePath = $_
        Get-ChildItem $FoldersToCheck -Recurse | ForEach {
         $FilePath = $_
        FindandScrub $FilePath
        write-host ($FilePath)
#       foreach($_ in $RegexPattern){
#        
#           FindandScrub $_ $FilePath
#        }     
   }
 
}
Function FindandScrub
{
    param (
    #    [String]$RegexPattern,
        [String]$FilePath
       
    )
$regexs = @('(callid=)([a-zA-Z0-9]{5})([a-zA-Z0-9]{27})','(_ani=)([0-9]{5})([0-9]{5})','(ani.)([0-9]{5})([0-9]{5})')
Get-ChildItem -Path $FilePath '*.txt' | ForEach-Object {
  $c = (Get-Content $_.FullName)
  foreach ($regex in $regexs) {
    $c = ($c) -replace $regex,'${1}*****$3' -join "`r`n"
  }
  [IO.File]::WriteAllText($_.FullName, $c)
}
}

#$new = [Environment]::NewLine
#   # $getMatches = (Get-Content -Path $FilePath) | Where-Object { findstr.exe /mprc:. $_.FullName } | select-string $RegexPattern
##$getMatches=  (Get-Content -Path $FilePath) -match $RegexPattern | select-string -pattern $RegexPattern -CaseSensitive
##$getMatches = @(Get-Content -Path $FilePath -Raw) -match $RegexPattern | select-string -pattern $RegexPattern -AllMatches
##$getMatches = $content | Select-String -Pattern $RegexPattern 
#$getMatches = @($content) -match $RegexPattern|Select-String -Pattern $RegexPattern -AllMatches
#$getMatches.Matches.Value 
#Write-Host 'Found'$getMatches.Matches.Count' for reg exp' $RegexPattern 
#if($getMatches.Matches.Count -gt 0){
#$getMatches.Matches|Foreach{
#$matchedvalue=$_.Value
# if($matchedvalue.IndexOf('=') -ne -1){
#
#  $scrubedvalue= MaskValues $matchedvalue '=' $matchedvalue.Length.ToString()
#       
#   }elseif($matchedvalue.IndexOf(',') -ne -1){
#  $scrubedvalue= MaskValues $matchedvalue ',' $matchedvalue.Length.ToString()
#   }elseif($matchedvalue.IndexOf(':') -ne -1){
#  $scrubedvalue= MaskValues $matchedvalue ':' $matchedvalue.Length.ToString()
#   }
#
#
#   (Get-Content $Filepath).replace($matchedvalue, $scrubedvalue) | Set-Content $FilePath
#    #$content.replace($matchedvalue, $scrubedvalue) 
#    
#    # [System.IO.File]::WriteAllText($FilePath,$content)
#  
#}
#}
#}


Clear-Host

#$serverName = @("\\ito095617.hosts.cloud.ford.com\cisco$","\\ito095618.hosts.cloud.ford.com\cisco$","\\ito095619.hosts.cloud.ford.com\cisco$","\\ito095620.hosts.cloud.ford.com\cisco$","\\ito095621.hosts.cloud.ford.com\cisco$","\\ito095622.hosts.cloud.ford.com\cisco$","\\ito095623.hosts.cloud.ford.com\cisco$")
$serverName = @("\\ito095622.hosts.cloud.ford.com\cisco$")
$LocalPath = 'C:\Users\krompich\ford\test'
$FoldersToCheck = "C:\Users\krompich\ford\test\*.txt"
$FoldersToSearch = @("\CVP\VXMLServer\applications\FCNA_AUTH\logs\ActivityLog","\CVP\VXMLServer\applications\FCNA_Main_NLU\logs\ActivityLog","\CVP\VXMLServer\applications\FCNA_DisambigIntent_Voice\logs\ActivityLog")
#$FoldersToSearch = @("\CVP\VXMLServer\applications\FCNA_AUTH\logs\ActivityLog")
$serverName | ForEach {
    $serverName = $_
    $FoldersToSearch | ForEach{

        $remotepath = $serverName+$_
        $netorkpath='filesystem::'+$remotepath
        Write-Host $netorkpath
         $checkpath=Test-Path $netorkpath
        
        if($checkpath){
        $dirlocalPath = $LocalPath+$remotepath
     
        $checklocal = Test-Path -Path $dirlocalPath
        $checklocal=$true
        if($checklocal){
           $newfolder= New-Item -Path $LocalPath -Name $remotepath -ItemType "directory" 
           Downloads $remotepath $newfolder $serverName
           write-host ('downloads finished')
        }
        else{
        #Write-Host "Folders exists locally, Please delete and try again"
        #Remove-Item $remotepath
        #
        #$newfolder= New-Item -Path $LocalPath -Name $remotepath -ItemType "directory" 
        #Downloads $remotepath $newfolder $serverName

        }
        }
       

    }#\\ito095567.hosts.cloud.ford.com\cisco$\CVP\VXMLServer\applications\FCNA_AUTH\logs\ActivityLog
}

