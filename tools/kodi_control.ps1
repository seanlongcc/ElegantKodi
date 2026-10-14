param([Parameter(Mandatory=$true)][string]$Action)
# Use Kodi's loopback EventServer, not Windows input injection.
$client = [System.Net.Sockets.UdpClient]::new()
function Send-Packet([int]$Type, [byte[]]$Payload) {
    [byte[]]$header = 0x58,0x42,0x4d,0x43,2,0,0,$Type,0,0,0,1,0,0,0,1,0,0,0,0,0x45,0x46,0,0,0,0,0,0,0,0,0,0
    $header[16] = [byte]([math]::Floor($Payload.Length / 256))
    $header[17] = [byte]($Payload.Length % 256)
    [byte[]]$packet = $header + $Payload
    [void]$client.Send($packet, $packet.Length, '127.0.0.1', 9777)
}
$name = [System.Text.Encoding]::UTF8.GetBytes('ElegantFin development')
Send-Packet 1 ([byte[]]($name + [byte[]](0,0,0,0,0,0,0,0,0,0,0,0)))
Start-Sleep -Milliseconds 150
Send-Packet 10 ([byte[]]([byte[]](1) + [System.Text.Encoding]::UTF8.GetBytes($Action) + [byte[]](0)))
$client.Dispose()
Write-Output "Sent Kodi action: $Action"
