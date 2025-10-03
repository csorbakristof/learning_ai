Option Explicit

' Main subroutine to collect external emails
Sub CollectExternalEmails()
    Dim senderEmail As String
    Dim domainName As String
    Dim outlookApp As Outlook.Application
    Dim nameSpace As Outlook.NameSpace
    Dim cutoffDate As Date
    
    ' Define folder names to search in
    Dim folderNames As Variant
    folderNames = Array("Sent Items", "Beérkezett üzenetek", "Archive")
    
    ' Get user inputs
    senderEmail = InputBox("Enter the sender's email address:", "Sender Email", "csorba.kristof@vik.bme.hu")
    If senderEmail = "" Then
        MsgBox "No sender email provided. Exiting macro."
        Exit Sub
    End If
    
    domainName = InputBox("Enter the internal domain name:", "Domain Name", "bme.hu")
    If domainName = "" Then
        domainName = "bme.hu"
    End If
    
    ' Initialize Outlook application
    Set outlookApp = Application
    Set nameSpace = outlookApp.GetNamespace("MAPI")
    
    ' Calculate cutoff date (3 months ago)
    cutoffDate = DateAdd("m", -3, Date)
    
    ' Main processing
    Dim externalEmails As Collection
    Set externalEmails = FindExternalEmails(nameSpace, senderEmail, domainName, cutoffDate, folderNames)
    
    If externalEmails.Count = 0 Then
        MsgBox "No external emails found matching the criteria."
        Exit Sub
    End If
    
    ' Create Excel report
    CreateExcelReport externalEmails
    
    MsgBox "External email collection completed! Excel file has been created with " & externalEmails.Count & " emails."
End Sub

' Function to find external emails matching criteria
Function FindExternalEmails(nameSpace As Outlook.NameSpace, senderEmail As String, domainName As String, cutoffDate As Date, folderNames As Variant) As Collection
    Dim externalEmails As New Collection
    Dim folder As Outlook.Folder
    Dim i As Integer
    
    ' Search through specified folders only
    For i = LBound(folderNames) To UBound(folderNames)
        Set folder = FindFolderByName(nameSpace, CStr(folderNames(i)))
        If Not folder Is Nothing Then
            SearchFolderForExternalEmails folder, externalEmails, senderEmail, domainName, cutoffDate
        End If
    Next i
    
    Set FindExternalEmails = externalEmails
End Function

' Helper function to find a folder by name across all mailboxes
Function FindFolderByName(nameSpace As Outlook.NameSpace, folderName As String) As Outlook.Folder
    Dim folders As Outlook.Folders
    Dim folder As Outlook.Folder
    Dim foundFolder As Outlook.Folder
    Dim mailboxCount As Integer
    
    Set FindFolderByName = Nothing
    
    ' Search through all mailboxes
    Set folders = nameSpace.Folders
    For mailboxCount = 1 To folders.Count
        Set folder = folders(mailboxCount)
        Set foundFolder = SearchForFolderByName(folder, folderName)
        If Not foundFolder Is Nothing Then
            Set FindFolderByName = foundFolder
            Exit Function
        End If
    Next mailboxCount
End Function

' Recursive helper to search for folder by name
Function SearchForFolderByName(parentFolder As Outlook.Folder, folderName As String) As Outlook.Folder
    Dim subFolder As Outlook.Folder
    Dim foundFolder As Outlook.Folder
    
    Set SearchForFolderByName = Nothing
    
    On Error Resume Next
    
    ' Check if current folder matches
    If LCase(parentFolder.Name) = LCase(folderName) Then
        Set SearchForFolderByName = parentFolder
        Exit Function
    End If
    
    ' Search subfolders recursively
    For Each subFolder In parentFolder.folders
        Set foundFolder = SearchForFolderByName(subFolder, folderName)
        If Not foundFolder Is Nothing Then
            Set SearchForFolderByName = foundFolder
            Exit Function
        End If
    Next subFolder
    
    On Error GoTo 0
End Function

' Recursive function to search folders for external emails
Sub SearchFolderForExternalEmails(folder As Outlook.Folder, externalEmails As Collection, senderEmail As String, domainName As String, cutoffDate As Date)
    Dim items As Outlook.Items
    Dim mailItem As Outlook.MailItem
    Dim i As Integer
    Dim subFolder As Outlook.Folder
    Dim emailDirection As String
    
    On Error Resume Next
    
    ' Search items in current folder
    Set items = folder.items
    For i = 1 To items.Count
        If TypeOf items(i) Is Outlook.MailItem Then
            Set mailItem = items(i)
            
            ' Check if email is within cutoff date
            If mailItem.ReceivedTime >= cutoffDate Then
                ' Determine email direction
                emailDirection = GetEmailDirection(mailItem, senderEmail)
                
                ' Check if email meets criteria
                If ShouldIncludeEmail(mailItem, emailDirection, senderEmail, domainName) Then
                    ' Create email info array and add to collection
                    Dim emailInfo As Variant
                    emailInfo = CreateEmailInfo(mailItem, emailDirection)
                    externalEmails.Add emailInfo
                End If
            End If
        End If
    Next i
    
    ' Recursively search subfolders
    For Each subFolder In folder.folders
        SearchFolderForExternalEmails subFolder, externalEmails, senderEmail, domainName, cutoffDate
    Next subFolder
    
    On Error GoTo 0
End Sub

' Determine if email is "sent" or "received" based on sender
Function GetEmailDirection(mailItem As Outlook.MailItem, senderEmail As String) As String
    If LCase(GetSenderEmailAddress(mailItem)) = LCase(senderEmail) Then
        GetEmailDirection = "sent"
    Else
        GetEmailDirection = "received"
    End If
End Function

' Check if email should be included based on criteria
Function ShouldIncludeEmail(mailItem As Outlook.MailItem, emailDirection As String, senderEmail As String, domainName As String) As Boolean
    ShouldIncludeEmail = False
    
    If emailDirection = "sent" Then
        ' For sent emails: must have external recipients and contain "EDIH"
        If HasExternalRecipients(mailItem, domainName) And ContainsEDIH(mailItem) Then
            ShouldIncludeEmail = True
        End If
    ElseIf emailDirection = "received" Then
        ' For received emails: must be from external sender
        If IsExternalSender(mailItem, domainName) Then
            ShouldIncludeEmail = True
        End If
    End If
End Function

' Check if email has external recipients (To field only)
Function HasExternalRecipients(mailItem As Outlook.MailItem, domainName As String) As Boolean
    Dim recipient As Outlook.Recipient
    Dim recipientAddress As String
    
    HasExternalRecipients = False
    
    ' Check TO recipients only
    For Each recipient In mailItem.recipients
        If recipient.Type = olTo Then ' Only check To recipients, not CC or BCC
            recipientAddress = GetRecipientEmailAddress(recipient)
            If Not IsInternalDomain(recipientAddress, domainName) Then
                HasExternalRecipients = True
                Exit Function
            End If
        End If
    Next recipient
End Function

' Check if email contains "EDIH" in body
Function ContainsEDIH(mailItem As Outlook.MailItem) As Boolean
    ContainsEDIH = InStr(1, mailItem.Body, "EDIH", vbTextCompare) > 0
End Function

' Check if sender is from external domain
Function IsExternalSender(mailItem As Outlook.MailItem, domainName As String) As Boolean
    Dim senderAddress As String
    senderAddress = GetSenderEmailAddress(mailItem)
    IsExternalSender = Not IsInternalDomain(senderAddress, domainName)
End Function

' Helper function to check if an email address is from internal domain (including subdomains)
Function IsInternalDomain(emailAddress As String, domainName As String) As Boolean
    Dim atPosition As Integer
    Dim domain As String
    
    IsInternalDomain = False
    
    If emailAddress = "" Then Exit Function
    
    atPosition = InStrRev(emailAddress, "@")
    If atPosition > 0 Then
        domain = LCase(Mid(emailAddress, atPosition + 1))
        domainName = LCase(domainName)
        
        ' Check if domain ends with the specified domain (to include subdomains)
        If domain = domainName Or Right(domain, Len(domainName) + 1) = "." & domainName Then
            IsInternalDomain = True
        End If
    End If
End Function

' Get sender email address from mail item
Function GetSenderEmailAddress(mailItem As Outlook.MailItem) As String
    Dim senderAddress As String
    
    On Error Resume Next
    
    ' Try to get SMTP address first
    If mailItem.SenderEmailType = "EX" Then
        senderAddress = mailItem.Sender.GetExchangeUser().PrimarySmtpAddress
    Else
        senderAddress = mailItem.SenderEmailAddress
    End If
    
    ' Fallback to sender email address if SMTP not available
    If senderAddress = "" Then
        senderAddress = mailItem.SenderEmailAddress
    End If
    
    On Error GoTo 0
    GetSenderEmailAddress = senderAddress
End Function

' Get recipient email address
Function GetRecipientEmailAddress(recipient As Outlook.Recipient) As String
    Dim emailAddress As String
    
    On Error Resume Next
    
    ' Try to get SMTP address first
    If recipient.AddressEntry.Type = "EX" Then
        emailAddress = recipient.AddressEntry.GetExchangeUser().PrimarySmtpAddress
    Else
        emailAddress = recipient.Address
    End If
    
    ' Fallback to display address if SMTP not available
    If emailAddress = "" Then
        emailAddress = recipient.Address
    End If
    
    On Error GoTo 0
    GetRecipientEmailAddress = emailAddress
End Function

' Get TO recipients as comma-separated string
Function GetToRecipientsString(mailItem As Outlook.MailItem, domainName As String) As String
    Dim recipient As Outlook.Recipient
    Dim recipientAddress As String
    Dim recipientsString As String
    
    recipientsString = ""
    
    ' Get all TO recipients
    For Each recipient In mailItem.recipients
        If recipient.Type = olTo Then ' Only To recipients
            recipientAddress = GetRecipientEmailAddress(recipient)
            If recipientsString <> "" Then
                recipientsString = recipientsString & "; "
            End If
            recipientsString = recipientsString & recipientAddress
        End If
    Next recipient
    
    GetToRecipientsString = recipientsString
End Function

' Create Excel report with external emails
Sub CreateExcelReport(externalEmails As Collection)
    Dim excelApp As Object
    Dim workbook As Object
    Dim worksheet As Object
    Dim row As Integer
    Dim emailInfo As Variant
    
    ' Create Excel application
    Set excelApp = CreateObject("Excel.Application")
    excelApp.Visible = True
    
    ' Create new workbook
    Set workbook = excelApp.Workbooks.Add
    Set worksheet = workbook.Worksheets(1)
    
    ' Set up headers
    worksheet.Cells(1, 1).Value = "Sender email address"
    worksheet.Cells(1, 2).Value = "Recipients email addresses"
    worksheet.Cells(1, 3).Value = "Subject"
    worksheet.Cells(1, 4).Value = "Date of sending/receiving"
    worksheet.Cells(1, 5).Value = "Conversation ID"
    worksheet.Cells(1, 6).Value = "Direction"
    
    ' Format headers
    With worksheet.Range("A1:F1")
        .Font.Bold = True
        .Interior.Color = RGB(200, 200, 200)
    End With
    
    ' Process each external email
    row = 2
    Dim emailCount As Long
    For emailCount = 1 To externalEmails.Count
        emailInfo = externalEmails(emailCount)
        
        ' Fill Excel row
        worksheet.Cells(row, 1).Value = emailInfo(0) ' SenderAddress
        worksheet.Cells(row, 2).Value = emailInfo(1) ' RecipientsString
        worksheet.Cells(row, 3).Value = emailInfo(2) ' Subject
        worksheet.Cells(row, 4).Value = Format(emailInfo(3), "yyyy-mm-dd hh:mm") ' EmailDate
        worksheet.Cells(row, 5).Value = emailInfo(4) ' ConversationID
        worksheet.Cells(row, 6).Value = emailInfo(5) ' Direction
        
        row = row + 1
    Next emailCount
    
    ' Auto-fit columns
    worksheet.Columns("A:F").AutoFit
    
    ' Add summary
    worksheet.Cells(row + 1, 1).Value = "Total External Emails:"
    worksheet.Cells(row + 1, 2).Value = externalEmails.Count
    
    ' Format summary
    With worksheet.Range("A" & (row + 1) & ":B" & (row + 1))
        .Font.Bold = True
    End With
End Sub

' Create email info array
Function CreateEmailInfo(mailItem As Outlook.MailItem, direction As String) As Variant
    Dim emailInfo(5) As Variant
    
    emailInfo(0) = GetSenderEmailAddress(mailItem)
    emailInfo(1) = GetToRecipientsString(mailItem, "")
    emailInfo(2) = mailItem.Subject
    emailInfo(3) = mailItem.ReceivedTime
    emailInfo(4) = mailItem.ConversationID
    emailInfo(5) = direction
    
    CreateEmailInfo = emailInfo
End Function