# 取得 IP
$Url = "https://api.ipify.org"

$RetryCount = 3
$Retry = 0
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
    $OutputFile = ".\ip.txt"
    if (Test-Path $OutputFile) {
        $ExistingContent = Get-Content $OutputFile
        if ($Content -eq $ExistingContent) {
            Write-Host "Content has not changed."
            exit
        } else {
            Write-Host "Content has changed. Updating file..."
            Set-Content -Path $OutputFile -Value $Content
        }
    } else {
        Write-Host "File does not exist. Creating file..."
        Set-Content -Path $OutputFile -Value $Content
    }

    # 設定 Gmail 帳戶
    $Username = "example@gmail.com"
    $Password = "password"

    # 設定 收件人和信件內容
    $Recipient = "example@gmail.com"
    $Subject = "IP has been modified!"
    $Body = "<html lang=\'zh-Hant-TW\'><head><meta charset=\'UTF-8\'><link rel=\'stylesheet\' href=\'https://fonts.googleapis.com/css2?family=Noto+Sans+TC&display=swap\'></head><style>body {vertical-align: center;font-family: \'Noto Sans TC\', \'Helvetica Neue\', Helvetica, Arial, sans-serif;font-size: 20px;}</style><body><span>&#10071;&#10071;&#10071; IP has been change to: {ip}</span></body></html>".Replace("{ip}", $Response.Content)

    # 設定 SMTP 伺服器和Port
    $SmtpServer = "smtp.gmail.com"
    $SmtpPort = 587

    # 建立郵件
    $MailMessage = New-Object System.Net.Mail.MailMessage
    $MailMessage.From = $Username
    $MailMessage.To.Add($Recipient)
    $MailMessage.Subject = $Subject
    $MailMessage.Body = $Body
    $MailMessage.IsBodyHtml = $true

    # 建立 SMTP 客戶端
    $SmtpClient = New-Object System.Net.Mail.SmtpClient($SmtpServer, $SmtpPort)
    $SmtpClient.EnableSsl = $true
    $SmtpClient.Credentials = New-Object System.Net.NetworkCredential($Username, $Password)

    # 發送郵件
    try {
        $SmtpClient.Send($MailMessage)
        Write-Host "Email sent successfully."  # 郵件發送成功提示
    }
    catch {
        Write-Host "Failed to send email. $_.Exception.Message"  # 郵件發送失敗提示
    }
}