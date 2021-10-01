$envs = Get-Content "./server/.env"
$envs | foreach {
    $env = $_ -split '='
    $key = $env[0]
    $value = $env[1]
    [Environment]::SetEnvironmentVariable($key ,$value)
}
WRITE-HOST "All .env values added !"
.\.virtualenv\Scripts\activate.ps1
python run.py