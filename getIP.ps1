# 先找出 VPN 連線
$VpnAdapters = Get-NetAdapter | Where-Object { $_.Name -like "*VPN*" }

# 斷開找到的每個 VPN 網線
foreach ($Adapter in $VpnAdapters) {
    Disable-NetAdapter -Name $Adapter.Name -Confirm:$False
    Write-Host "The network $($Adapter.Name) terminated"
}

# 取得 IP
$Url = "https://api.ipify.org"

# 重試次數
$RetryCount = 3
$Retry = 0
# 是否成功
$Success = $false

while (-not $Success -and $Retry -lt $RetryCount) {
    try {
        $Response = Invoke-WebRequest -Uri $Url -UseBasicParsing
        $Content = $Response.Content
        $Success = $true
    }
    catch {
        $Retry++
    }
}

if ($Success) {
    $ScriptPath = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
    $OutputFile = "${ScriptPath}\ip.txt"

    # 檢查有沒有之前的 IP 紀錄檔
    if (Test-Path $OutputFile) {
        $ExistingContent = Get-Content $OutputFile
        # 存在且相同就直接結束
        if ($Content -eq $ExistingContent) {
            Write-Host "IP has not changed."
            exit
        }
        # 如果不相同將 IP 覆寫掉
        else {
            Write-Host "IP has changed. Updating file..."
            Set-Content -Path $OutputFile -Value $Content
        }
    }
    # 如果沒有直接產生檔案及將 IP 寫進去
    else {
        Write-Host "File does not exist. Creating file..."
        Set-Content -Path $OutputFile -Value $Content
    }

    # 設定 Gmail 帳戶
    $Username = "example@gmail.com"
    $Password = "password"

    # 設定 收件人和信件內容
    $Recipient = "example@gmail.com"
    $Subject = "IP has been modified!"
    $Body = "<html lang='zh-Hant-TW'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1'><link href='https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500&display=swap' rel='stylesheet'><style>body {font-family: 'Noto Sans TC', sans-serif;padding: 20px;}.alert {position: relative;color: #055160;background-color: #cff4fc;border-color: #9eeaf9;padding: 1rem 1rem;margin-bottom: 1rem;border: 1px solid transparent;border-radius: .375rem;}.alert-heading {color: inherit;}.text-danger {color: rgba(220, 53, 69, 1) !important;}.fw-bold {font-weight: bold;}h4, .h4{margin-top: 0;margin-bottom: 0.5rem;font-weight: 500;line-height: 1.2;color: inherit;font-size: calc(1.275rem + 0.3vw);}hr {margin: 1rem 0;color: inherit;border: 0;border-top: 1px solid;opacity: 0.25;}</style></head><body><div class='alert' role='alert'><h4 class='alert-heading'>IP 通知</h4><hr><div>您的 IP 地址已經更改為：<span class='text-danger fw-bold'>{ip}</span></div></div></body></html>".Replace("{ip}", $Response.Content)
    $HTMLView = [System.Net.Mail.AlternateView]::CreateAlternateViewFromString($Body, [System.Text.Encoding]::UTF8, "text/html")

    # 設定 SMTP 伺服器和Port
    $SmtpServer = "smtp.gmail.com"
    $SmtpPort = 587

    # 建立郵件
    $MailMessage = New-Object System.Net.Mail.MailMessage
    $MailMessage.From = $Username
    $MailMessage.To.Add($Recipient)
    $MailMessage.Subject = $Subject
    $MailMessage.AlternateViews.Add($HTMLView)
    
    # 建立 SMTP 客戶端
    $SmtpClient = New-Object System.Net.Mail.SmtpClient($SmtpServer, $SmtpPort)
    $SmtpClient.EnableSsl = $true
    $SmtpClient.Credentials = New-Object System.Net.NetworkCredential($Username, $Password)

    # 發送郵件
    try {
        $SmtpClient.Send($MailMessage)
        # 郵件發送成功提示
        Write-Host "Email sent successfully."
    }
    catch {
        # 郵件發送失敗提示
        Write-Host "Failed to send email. $_.Exception.Message"
    }
}

exit