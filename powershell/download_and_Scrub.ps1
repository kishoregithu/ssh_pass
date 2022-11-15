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
            FindandScrub $Path
            $n = $Path.Split('\')
            $foldertype = $n[10]
            $servername = $n[5]
            $pattern = '[\\/]'
            $logdate=$DtFilesToGet.ToString('yyyy-MM-dd')
            $zipname = $foldertype+$logdate+'.zip'
            $zipname = $zipname -replace $pattern, ''
            Compress-Archive -Path $Path -DestinationPath $Path\$zipname
            UplodadToNexus $servername $zipname $Path
        
        }
        }else{
        Write-Host "No files to download"
        }
        }
        #Copy-Item -Path $Location -Destination $Path -Recurse
    }catch{
        Write-Error "Error while copying files from Remote Server" 
        Write-Host $_.
    }
    return
    
}

Function UplodadToNexus{
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
    try{
        $uplodstatus = Invoke-WebRequest @params
        Write-Host $uplodstatus
    }catch{
        Write-error "Erro while uploading to Nexus"
        Write-host $_.
    }
}

Function FindandScrub
{
    param (
        [String]$FilePath
    )
    $regexs = @("(callid=)([a-zA-Z0-9]{5})([a-zA-Z0-9]{27})", "(_ani=)([0-9]{5})([0-9]{5})", "(ani.)([0-9]{5})([0-9]{5})", "(_dnis=)([0-9]{5})([0-9]{5})", "(dnis.)([0-9]{5})([0-9]{5})", "(output\((VehicleIdentificationSerialNumber)\).)([a-zA-Z0-9]{6})([a-zA-Z0-9]{6})", "(SSN..)([0-9]{2})([0-9]{2})", "(accountNumber is* *)([0-9]{4})([0-9]{3})", "(accountNumber:,)([0-9]{4})([0-9]{3})", "([Aa]ccount *[Nn]umber is *:* )([0-9]{4})([0-9]{3})", "(sKey,)([0-9]{5})([0-9]{5})", "(ANI:::,)([0-9]{5})([0-9]{5})", "(output\((SSN)\).)([0-9]{2})([0-9]{2})", "(account[Nn]umber..)([0-9]{4})([0-9]{4})", "(account[Nn]umber..)([0-9]{5})([0-9]{4})", "(financeCode.)([0-9]{2})([0-9]{2})", "(value: )([a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4})(-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})", "(ClientId\s.\s[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4})(-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})", "(ClientSecret\s.\s.)([a-zA-Z0-9]{21})(_[a-zA-Z0-9]{5}-[a-zA-Z0-9]{11})")
    Get-ChildItem -Path $FilePath '*.txt' | ForEach-Object {
        $c = (Get-Content $_.FullName)
        foreach ($regex in $regexs) {
            $c = ($c) -replace $regex,'${1}*****$3' -join "`r`n"
        }
        [IO.File]::WriteAllText($_.FullName, $c)
    }
}

Clear-Host
#$serverName = @("\\ito095617.hosts.cloud.ford.com\cisco$","\\ito095618.hosts.cloud.ford.com\cisco$","\\ito095619.hosts.cloud.ford.com\cisco$","\\ito095620.hosts.cloud.ford.com\cisco$","\\ito095621.hosts.cloud.ford.com\cisco$","\\ito095622.hosts.cloud.ford.com\cisco$","\\ito095623.hosts.cloud.ford.com\cisco$")
$serverName = @("\\ito095622.hosts.cloud.ford.com\cisco$")
$LocalPath = 'C:\Users\krompich\ford\test'
$FoldersToCheck = "C:\Users\krompich\ford\test\*.txt"
$FoldersToSearch = @("\CVP\VXMLServer\applications\FCNA_AUTH\logs\ActivityLog","\CVP\VXMLServer\applications\FCNA_Main_NLU\logs\ActivityLog","\CVP\VXMLServer\applications\FCNA_DisambigIntent_Voice\logs\ActivityLog")

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
        }
        else{
            write-host("File exists")
        }
    }
}

