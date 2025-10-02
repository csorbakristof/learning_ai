Option Explicit

' Main subroutine to track email conversion rates
Sub TrackEmailConversionRate()
    Dim senderEmail As String
    Dim domainName As String
    Dim outlookApp As Outlook.Application
    Dim nameSpace As Outlook.NameSpace
    Dim cutoffDate As Date
    
    ' Get user inputs
    senderEmail = InputBox("Enter the sender's email address:", "Sender Email", "")
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
    Dim outgoingEmails As Collection
    Set outgoingEmails = FindOutgoingEmails(nameSpace, senderEmail, domainName, cutoffDate)
    
    If outgoingEmails.Count = 0 Then
        MsgBox "No outgoing emails found matching the criteria."
        Exit Sub
    End If
    
    ' Process responses and create Excel report
    CreateExcelReport outgoingEmails, nameSpace, domainName
    
    MsgBox "Email conversion tracking completed! Excel file has been created and is ready for saving."
End Sub

' Function to find outgoing emails matching criteria
Function FindOutgoingEmails(nameSpace As Outlook.NameSpace, senderEmail As String, domainName As String, cutoffDate As Date) As Collection
    Dim outgoingEmails As New Collection
    Dim folders As Outlook.Folders
    Dim folder As Outlook.Folder
    Dim items As Outlook.Items
    Dim mailItem As Outlook.MailItem
    Dim i As Integer
    
    ' Get all folders in the mailbox
    Set folders = nameSpace.Folders
    
    ' Search through all folders recursively
    Dim folderCount As Integer
    For folderCount = 1 To folders.Count
        Set folder = folders(folderCount)
        SearchFolderForOutgoingEmails folder, outgoingEmails, senderEmail, domainName, cutoffDate
    Next folderCount
    
    Set FindOutgoingEmails = outgoingEmails
End Function

' Recursive function to search folders and subfolders
Sub SearchFolderForOutgoingEmails(folder As Outlook.Folder, outgoingEmails As Collection, senderEmail As String, domainName As String, cutoffDate As Date)
    Dim items As Outlook.Items
    Dim mailItem As Outlook.MailItem
    Dim i As Integer
    Dim subFolder As Outlook.Folder
    
    On Error Resume Next
    
    ' Search items in current folder
    Set items = folder.items
    For i = 1 To items.Count
        If TypeOf items(i) Is Outlook.MailItem Then
            Set mailItem = items(i)
            
            ' Check if email matches criteria
            If LCase(mailItem.SenderEmailAddress) = LCase(senderEmail) And _
               mailItem.ReceivedTime >= cutoffDate And _
               InStr(1, mailItem.Body, "EDIH", vbTextCompare) > 0 And _
               IsExternalRecipient(mailItem, domainName) Then
                
                outgoingEmails.Add mailItem
            End If
        End If
    Next i
    
    ' Recursively search subfolders
    For Each subFolder In folder.folders
        SearchFolderForOutgoingEmails subFolder, outgoingEmails, senderEmail, domainName, cutoffDate
    Next subFolder
    
    On Error GoTo 0
End Sub

' Function to count responses for a given original email
Function CountResponsesForEmail(nameSpace As Outlook.NameSpace, originalEmail As Outlook.MailItem, domainName As String) As Integer
    Dim responseCount As Integer
    Dim folders As Outlook.Folders
    Dim folder As Outlook.Folder
    Dim conversationID As String
    
    responseCount = 0
    conversationID = originalEmail.ConversationID
    
    ' Search all folders for responses
    Set folders = nameSpace.Folders
    Dim folderCount As Integer
    For folderCount = 1 To folders.Count
        Set folder = folders(folderCount)
        responseCount = responseCount + SearchFolderForResponses(folder, conversationID, domainName, originalEmail.ReceivedTime)
    Next folderCount
    
    CountResponsesForEmail = responseCount
End Function

' Recursive function to search for responses in folders
Function SearchFolderForResponses(folder As Outlook.Folder, conversationID As String, domainName As String, originalEmailDate As Date) As Integer
    Dim responseCount As Integer
    Dim items As Outlook.Items
    Dim mailItem As Outlook.MailItem
    Dim i As Integer
    Dim subFolder As Outlook.Folder
    
    responseCount = 0
    On Error Resume Next
    
    ' Search items in current folder
    Set items = folder.items
    For i = 1 To items.Count
        If TypeOf items(i) Is Outlook.MailItem Then
            Set mailItem = items(i)
            
            ' Check if this is a response from external domain
            If mailItem.ConversationID = conversationID And _
               mailItem.ReceivedTime > originalEmailDate And _
               Not IsInternalDomain(mailItem.SenderEmailAddress, domainName) Then
                
                responseCount = responseCount + 1
            End If
        End If
    Next i
    
    ' Recursively search subfolders
    For Each subFolder In folder.folders
        responseCount = responseCount + SearchFolderForResponses(subFolder, conversationID, domainName, originalEmailDate)
    Next subFolder
    
    On Error GoTo 0
    SearchFolderForResponses = responseCount
End Function

' Create Excel report with outgoing emails and response counts
Sub CreateExcelReport(outgoingEmails As Collection, nameSpace As Outlook.NameSpace, domainName As String)
    Dim excelApp As Object
    Dim workbook As Object
    Dim worksheet As Object
    Dim row As Integer
    Dim mailItem As Outlook.MailItem
    Dim responseCount As Integer
    Dim recipients As String
    
    ' Create Excel application
    Set excelApp = CreateObject("Excel.Application")
    excelApp.Visible = True
    
    ' Create new workbook
    Set workbook = excelApp.Workbooks.Add
    Set worksheet = workbook.Worksheets(1)
    
    ' Set up headers
    worksheet.Cells(1, 1).Value = "Date"
    worksheet.Cells(1, 2).Value = "Sender"
    worksheet.Cells(1, 3).Value = "Subject"
    worksheet.Cells(1, 4).Value = "Recipient"
    worksheet.Cells(1, 5).Value = "Response Count"
    
    ' Format headers
    With worksheet.Range("A1:E1")
        .Font.Bold = True
        .Interior.Color = RGB(200, 200, 200)
    End With
    
    ' Process each outgoing email
    row = 2
    Dim emailCount As Long
    For emailCount = 1 To outgoingEmails.Count
        Set mailItem = outgoingEmails(emailCount)
        
        ' Get external recipients
        recipients = GetExternalRecipients(mailItem, domainName)
        
        ' Count responses
        responseCount = CountResponsesForEmail(nameSpace, mailItem, domainName)
        
        ' Fill Excel row
        worksheet.Cells(row, 1).Value = Format(mailItem.ReceivedTime, "yyyy-mm-dd hh:mm")
        worksheet.Cells(row, 2).Value = mailItem.SenderEmailAddress
        worksheet.Cells(row, 3).Value = mailItem.Subject
        worksheet.Cells(row, 4).Value = recipients
        worksheet.Cells(row, 5).Value = responseCount
        
        row = row + 1
    Next emailCount
    
    ' Auto-fit columns
    worksheet.Columns("A:E").AutoFit
    
    ' Add summary
    worksheet.Cells(row + 1, 1).Value = "Total Emails Sent:"
    worksheet.Cells(row + 1, 2).Value = outgoingEmails.Count
    worksheet.Cells(row + 2, 1).Value = "Total Responses:"
    worksheet.Cells(row + 2, 2).Value = Application.WorksheetFunction.Sum(worksheet.Range("E2:E" & (row - 1)))
    
    ' Format summary
    With worksheet.Range("A" & (row + 1) & ":B" & (row + 2))
        .Font.Bold = True
    End With
End Sub

' Helper function to check if an email has external recipients
Function IsExternalRecipient(mailItem As Outlook.MailItem, domainName As String) As Boolean
    Dim recipient As Outlook.Recipient
    Dim recipientAddress As String
    
    IsExternalRecipient = False
    
    ' Check TO recipients
    For Each recipient In mailItem.recipients
        recipientAddress = GetEmailAddress(recipient)
        If Not IsInternalDomain(recipientAddress, domainName) Then
            IsExternalRecipient = True
            Exit Function
        End If
    Next recipient
End Function

' Helper function to get external recipients as a string
Function GetExternalRecipients(mailItem As Outlook.MailItem, domainName As String) As String
    Dim recipient As Outlook.Recipient
    Dim recipientAddress As String
    Dim externalRecipients As String
    
    externalRecipients = ""
    
    ' Check all recipients
    For Each recipient In mailItem.recipients
        recipientAddress = GetEmailAddress(recipient)
        If Not IsInternalDomain(recipientAddress, domainName) Then
            If externalRecipients <> "" Then
                externalRecipients = externalRecipients & "; "
            End If
            externalRecipients = externalRecipients & recipientAddress
        End If
    Next recipient
    
    GetExternalRecipients = externalRecipients
End Function

' Helper function to check if an email address is from internal domain
Function IsInternalDomain(emailAddress As String, domainName As String) As Boolean
    Dim atPosition As Integer
    Dim domain As String
    
    IsInternalDomain = False
    
    If emailAddress = "" Then Exit Function
    
    atPosition = InStrRev(emailAddress, "@")
    If atPosition > 0 Then
        domain = Mid(emailAddress, atPosition + 1)
        IsInternalDomain = (LCase(domain) = LCase(domainName))
    End If
End Function

' Helper function to get email address from recipient
Function GetEmailAddress(recipient As Outlook.Recipient) As String
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
    GetEmailAddress = emailAddress
End Function