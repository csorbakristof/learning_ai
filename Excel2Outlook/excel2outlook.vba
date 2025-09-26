' =============================================================================
' Excel2Outlook - SingleSend and MassiveSend Features
' =============================================================================
' [SingleSend] - Sends personalized email for current row
' Triggered by: Ctrl+Shift+D from current row in UserList worksheet
' 
' [MassiveSend] - Sends personalized emails for all visible rows
' Triggered by: Ctrl+Shift+M from UserList worksheet
'
' Template source: "EmailTemplate" worksheet, cell A1
' =============================================================================

Option Explicit

' Global variables for Outlook application
Private outlookApp As Object
Private outlookNamespace As Object

' =============================================================================
' Main SingleSend Macro - Entry Point
' =============================================================================
Sub SingleSend()
    On Error GoTo ErrorHandler
    
    Dim currentRow As Long
    Dim userListWs As Worksheet
    Dim templateWs As Worksheet
    Dim emailTemplate As String
    Dim emailAddress As String
    Dim emailSubject As String
    Dim personalizedBody As String
    Dim columnHeaders As Variant
    Dim rowData As Variant
    
    ' Get current active worksheet and row
    Set userListWs = ActiveSheet
    currentRow = ActiveCell.Row
    
    ' Validate current row (must be > 1 since row 1 contains headers)
    If currentRow <= 1 Then
        MsgBox "Error: Please select a data row (not the header row) before running MassiveSend.", _
               vbCritical, "MassiveSend Error"
        Exit Sub
    End If
    
    ' Check if EmailTemplate worksheet exists
    Set templateWs = GetEmailTemplateWorksheet()
    If templateWs Is Nothing Then Exit Sub
    
    ' Get email template from EmailTemplate!A1
    emailTemplate = templateWs.Range("A1").Value
    If Trim(emailTemplate) = "" Then
        MsgBox "Error: Email template in 'EmailTemplate' worksheet, cell A1 is empty.", _
               vbCritical, "MassiveSend Error"
        Exit Sub
    End If
    
    ' Get column headers and validate required columns
    columnHeaders = GetColumnHeaders(userListWs)
    If IsEmpty(columnHeaders) Then Exit Sub
    
    ' Validate required columns exist
    If Not ValidateRequiredColumns(columnHeaders, "SingleSend") Then Exit Sub
    
    ' Get data from current row
    rowData = GetRowData(userListWs, currentRow)
    
    ' Get email address and subject
    emailAddress = GetColumnValue(columnHeaders, rowData, "email")
    emailSubject = GetColumnValue(columnHeaders, rowData, "Subject")
    
    ' Validate email and subject are not empty
    If Trim(emailAddress) = "" Then
        MsgBox "Error: Email address is empty in row " & currentRow & ".", _
               vbCritical, "MassiveSend Error"
        Exit Sub
    End If
    
    If Trim(emailSubject) = "" Then
        MsgBox "Error: Subject is empty in row " & currentRow & ".", _
               vbCritical, "MassiveSend Error"
        Exit Sub
    End If
    
    ' Process template with placeholders
    personalizedBody = ProcessTemplate(emailTemplate, columnHeaders, rowData, currentRow)
    If personalizedBody = "" Then Exit Sub ' Error already shown in ProcessTemplate
    
    ' Initialize Outlook connection
    If Not InitializeOutlook() Then Exit Sub
    
    ' Create and show email draft
    CreateEmailDraft emailAddress, emailSubject, personalizedBody
    
    MsgBox "Email draft created successfully for " & emailAddress, _
           vbInformation, "SingleSend Success"
    
    Exit Sub

ErrorHandler:
    MsgBox "Unexpected error in SingleSend: " & Err.Description & vbCrLf & _
           "Error Number: " & Err.Number, vbCritical, "SingleSend Error"
End Sub

' =============================================================================
' Main MassiveSend Macro - Entry Point
' =============================================================================
Sub MassiveSend()
    On Error GoTo ErrorHandler
    
    Dim userListWs As Worksheet
    Dim templateWs As Worksheet
    Dim emailTemplate As String
    Dim columnHeaders As Variant
    Dim visibleRows As Collection
    Dim totalEmails As Long
    Dim currentRow As Long
    Dim i As Long
    Dim confirmResult As VbMsgBoxResult
    
    ' Get current active worksheet
    Set userListWs = ActiveSheet
    
    ' Check if EmailTemplate worksheet exists
    Set templateWs = GetEmailTemplateWorksheet()
    If templateWs Is Nothing Then Exit Sub
    
    ' Get email template from EmailTemplate!A1
    emailTemplate = templateWs.Range("A1").Value
    If Trim(emailTemplate) = "" Then
        MsgBox "Error: Email template in 'EmailTemplate' worksheet, cell A1 is empty.", _
               vbCritical, "MassiveSend Error"
        Exit Sub
    End If
    
    ' Get column headers and validate required columns
    columnHeaders = GetColumnHeaders(userListWs)
    If IsEmpty(columnHeaders) Then Exit Sub
    
    ' Validate required columns exist
    If Not ValidateRequiredColumns(columnHeaders, "MassiveSend") Then Exit Sub
    
    ' Get all visible rows (excluding header row)
    Set visibleRows = GetVisibleRows(userListWs)
    totalEmails = visibleRows.Count
    
    If totalEmails = 0 Then
        MsgBox "No visible data rows found to process.", _
               vbInformation, "MassiveSend Info"
        Exit Sub
    End If
    
    ' Ask for confirmation if more than 20 emails
    If totalEmails > 20 Then
        confirmResult = MsgBox("This will create " & totalEmails & " email drafts. " & vbCrLf & _
                              "Are you sure you want to continue?", _
                              vbYesNo + vbQuestion, "MassiveSend Confirmation")
        If confirmResult = vbNo Then
            Exit Sub
        End If
    End If
    
    ' Pre-validate ALL rows before creating any emails
    If Not PreValidateAllRows(userListWs, visibleRows, columnHeaders, emailTemplate) Then
        Exit Sub ' Error already shown in PreValidateAllRows
    End If
    
    ' Initialize Outlook connection
    If Not InitializeOutlook() Then Exit Sub
    
    ' Create email drafts for all visible rows
    For i = 1 To visibleRows.Count
        currentRow = visibleRows(i)
        CreateEmailForRow userListWs, currentRow, columnHeaders, emailTemplate
    Next i
    
    ' Show success summary
    MsgBox totalEmails & " email drafts created successfully!", _
           vbInformation, "MassiveSend Success"
    
    Exit Sub

ErrorHandler:
    MsgBox "Unexpected error in MassiveSend: " & Err.Description & vbCrLf & _
           "Error Number: " & Err.Number, vbCritical, "MassiveSend Error"
End Sub

' =============================================================================
' Get EmailTemplate worksheet
' =============================================================================
Private Function GetEmailTemplateWorksheet() As Worksheet
    Dim ws As Worksheet
    
    ' Look for "EmailTemplate" worksheet (case-sensitive)
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name = "EmailTemplate" Then
            Set GetEmailTemplateWorksheet = ws
            Exit Function
        End If
    Next ws
    
    ' Not found - show error
    MsgBox "Error: Worksheet named 'EmailTemplate' not found. " & vbCrLf & _
           "Please create a worksheet named exactly 'EmailTemplate' with the email template in cell A1.", _
           vbCritical, "MassiveSend Error"
    
    Set GetEmailTemplateWorksheet = Nothing
End Function

' =============================================================================
' Get column headers from row 1
' =============================================================================
Private Function GetColumnHeaders(ws As Worksheet) As Variant
    Dim lastCol As Long
    Dim headers As Variant
    
    ' Find last column with data in row 1
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    
    If lastCol = 1 And Trim(ws.Cells(1, 1).Value) = "" Then
        MsgBox "Error: No column headers found in row 1 of the current worksheet.", _
               vbCritical, "MassiveSend Error"
        GetColumnHeaders = Empty
        Exit Function
    End If
    
    ' Get headers as array
    headers = ws.Range(ws.Cells(1, 1), ws.Cells(1, lastCol)).Value
    GetColumnHeaders = headers
End Function

' =============================================================================
' Validate required columns exist
' =============================================================================
Private Function ValidateRequiredColumns(columnHeaders As Variant, featureName As String) As Boolean
    Dim i As Long
    Dim foundEmail As Boolean
    Dim foundSubject As Boolean
    
    foundEmail = False
    foundSubject = False
    
    ' Check if headers is a 2D array (single row)
    If UBound(columnHeaders, 1) = 1 Then
        ' Single row array - check columns
        For i = 1 To UBound(columnHeaders, 2)
            If Trim(columnHeaders(1, i)) = "email" Then foundEmail = True
            If Trim(columnHeaders(1, i)) = "Subject" Then foundSubject = True
        Next i
    Else
        ' Single cell case
        If Trim(columnHeaders) = "email" Then foundEmail = True
        If Trim(columnHeaders) = "Subject" Then foundSubject = True
    End If
    
    ' Report missing columns
    If Not foundEmail And Not foundSubject Then
        MsgBox "Error: Required columns 'email' and 'Subject' are missing from row 1. " & vbCrLf & _
               "Column names are case-sensitive and must match exactly.", _
               vbCritical, featureName & " Error"
        ValidateRequiredColumns = False
    ElseIf Not foundEmail Then
        MsgBox "Error: Required column 'email' is missing from row 1. " & vbCrLf & _
               "Column name is case-sensitive and must match exactly.", _
               vbCritical, featureName & " Error"
        ValidateRequiredColumns = False
    ElseIf Not foundSubject Then
        MsgBox "Error: Required column 'Subject' is missing from row 1. " & vbCrLf & _
               "Column name is case-sensitive and must match exactly.", _
               vbCritical, featureName & " Error"
        ValidateRequiredColumns = False
    Else
        ValidateRequiredColumns = True
    End If
End Function

' =============================================================================
' Get data from specific row
' =============================================================================
Private Function GetRowData(ws As Worksheet, rowNum As Long) As Variant
    Dim lastCol As Long
    
    ' Find last column with data in row 1 (headers)
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    
    ' Get row data as array
    GetRowData = ws.Range(ws.Cells(rowNum, 1), ws.Cells(rowNum, lastCol)).Value
End Function

' =============================================================================
' Get value from specific column
' =============================================================================
Private Function GetColumnValue(columnHeaders As Variant, rowData As Variant, columnName As String) As String
    Dim i As Long
    
    ' Handle single cell case
    If Not IsArray(columnHeaders) Then
        If Trim(columnHeaders) = columnName Then
            GetColumnValue = Trim(CStr(rowData))
        Else
            GetColumnValue = ""
        End If
        Exit Function
    End If
    
    ' Handle array case
    For i = 1 To UBound(columnHeaders, 2)
        If Trim(columnHeaders(1, i)) = columnName Then
            If UBound(rowData, 2) >= i Then
                GetColumnValue = Trim(CStr(rowData(1, i)))
            Else
                GetColumnValue = ""
            End If
            Exit Function
        End If
    Next i
    
    GetColumnValue = ""
End Function

' =============================================================================
' Process template with placeholders
' =============================================================================
Private Function ProcessTemplate(template As String, columnHeaders As Variant, rowData As Variant, currentRow As Long) As String
    Dim result As String
    Dim placeholder As String
    Dim startPos As Long
    Dim endPos As Long
    Dim columnName As String
    Dim replacementValue As String
    Dim missingPlaceholders As String
    
    result = template
    missingPlaceholders = ""
    
    ' Find and replace all placeholders [ColumnName]
    startPos = InStr(result, "[")
    Do While startPos > 0
        endPos = InStr(startPos, result, "]")
        If endPos > 0 Then
            ' Extract placeholder and column name
            placeholder = Mid(result, startPos, endPos - startPos + 1)
            columnName = Mid(placeholder, 2, Len(placeholder) - 2)
            
            ' Get replacement value
            replacementValue = GetColumnValue(columnHeaders, rowData, columnName)
            
            ' Check if column exists and has value
            If HasColumn(columnHeaders, columnName) Then
                If Trim(replacementValue) = "" Then
                    ' Column exists but value is empty
                    If missingPlaceholders <> "" Then missingPlaceholders = missingPlaceholders & ", "
                    missingPlaceholders = missingPlaceholders & columnName & " (empty)"
                Else
                    ' Replace placeholder with value
                    result = Replace(result, placeholder, replacementValue)
                End If
            Else
                ' Column doesn't exist
                If missingPlaceholders <> "" Then missingPlaceholders = missingPlaceholders & ", "
                missingPlaceholders = missingPlaceholders & columnName & " (missing column)"
            End If
            
            ' Find next placeholder
            startPos = InStr(startPos + 1, result, "[")
        Else
            ' No closing bracket found
            startPos = InStr(startPos + 1, result, "[")
        End If
    Loop
    
    ' Report errors if any missing placeholders
    If missingPlaceholders <> "" Then
        MsgBox "Error: Missing or empty placeholder values in row " & currentRow & ":" & vbCrLf & _
               missingPlaceholders & vbCrLf & vbCrLf & _
               "Please ensure all placeholder columns exist and have values.", _
               vbCritical, "MassiveSend Error"
        ProcessTemplate = ""
        Exit Function
    End If
    
    ProcessTemplate = result
End Function

' =============================================================================
' Get all visible rows (excluding header row)
' =============================================================================
Private Function GetVisibleRows(ws As Worksheet) As Collection
    Dim visibleRows As New Collection
    Dim lastRow As Long
    Dim i As Long
    
    ' Find last row with data
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    
    ' Collect visible rows (starting from row 2, skipping headers)
    For i = 2 To lastRow
        If Not ws.Rows(i).Hidden Then
            visibleRows.Add i
        End If
    Next i
    
    Set GetVisibleRows = visibleRows
End Function

' =============================================================================
' Pre-validate all rows before creating any emails
' =============================================================================
Private Function PreValidateAllRows(ws As Worksheet, visibleRows As Collection, columnHeaders As Variant, emailTemplate As String) As Boolean
    Dim i As Long
    Dim currentRow As Long
    Dim rowData As Variant
    Dim emailAddress As String
    Dim emailSubject As String
    Dim validationResult As String
    Dim errorMessages As String
    
    errorMessages = ""
    
    ' Validate each visible row
    For i = 1 To visibleRows.Count
        currentRow = visibleRows(i)
        rowData = GetRowData(ws, currentRow)
        
        ' Validate email address
        emailAddress = GetColumnValue(columnHeaders, rowData, "email")
        If Trim(emailAddress) = "" Then
            errorMessages = errorMessages & "Row " & currentRow & ": Email address is empty" & vbCrLf
        End If
        
        ' Validate subject
        emailSubject = GetColumnValue(columnHeaders, rowData, "Subject")
        If Trim(emailSubject) = "" Then
            errorMessages = errorMessages & "Row " & currentRow & ": Subject is empty" & vbCrLf
        End If
        
        ' Validate template placeholders for this row
        validationResult = ValidateTemplatePlaceholders(emailTemplate, columnHeaders, rowData, currentRow)
        If validationResult <> "" Then
            errorMessages = errorMessages & "Row " & currentRow & ": " & validationResult & vbCrLf
        End If
    Next i
    
    ' Show errors if any found
    If errorMessages <> "" Then
        MsgBox "Validation errors found. No emails will be created:" & vbCrLf & vbCrLf & _
               errorMessages, vbCritical, "MassiveSend Validation Error"
        PreValidateAllRows = False
    Else
        PreValidateAllRows = True
    End If
End Function

' =============================================================================
' Validate template placeholders for a specific row
' =============================================================================
Private Function ValidateTemplatePlaceholders(template As String, columnHeaders As Variant, rowData As Variant, currentRow As Long) As String
    Dim startPos As Long
    Dim endPos As Long
    Dim columnName As String
    Dim replacementValue As String
    Dim missingPlaceholders As String
    
    missingPlaceholders = ""
    
    ' Find all placeholders [ColumnName]
    startPos = InStr(template, "[")
    Do While startPos > 0
        endPos = InStr(startPos, template, "]")
        If endPos > 0 Then
            ' Extract column name
            columnName = Mid(template, startPos + 1, endPos - startPos - 1)
            
            ' Get replacement value
            replacementValue = GetColumnValue(columnHeaders, rowData, columnName)
            
            ' Check if column exists and has value
            If HasColumn(columnHeaders, columnName) Then
                If Trim(replacementValue) = "" Then
                    ' Column exists but value is empty
                    If missingPlaceholders <> "" Then missingPlaceholders = missingPlaceholders & ", "
                    missingPlaceholders = missingPlaceholders & columnName & " (empty)"
                End If
            Else
                ' Column doesn't exist
                If missingPlaceholders <> "" Then missingPlaceholders = missingPlaceholders & ", "
                missingPlaceholders = missingPlaceholders & columnName & " (missing column)"
            End If
            
            ' Find next placeholder
            startPos = InStr(startPos + 1, template, "[")
        Else
            ' No closing bracket found
            startPos = InStr(startPos + 1, template, "[")
        End If
    Loop
    
    ValidateTemplatePlaceholders = missingPlaceholders
End Function

' =============================================================================
' Create email draft for a specific row
' =============================================================================
Private Sub CreateEmailForRow(ws As Worksheet, rowNum As Long, columnHeaders As Variant, emailTemplate As String)
    Dim rowData As Variant
    Dim emailAddress As String
    Dim emailSubject As String
    Dim personalizedBody As String
    
    ' Get data from row
    rowData = GetRowData(ws, rowNum)
    
    ' Get email address and subject
    emailAddress = GetColumnValue(columnHeaders, rowData, "email")
    emailSubject = GetColumnValue(columnHeaders, rowData, "Subject")
    
    ' Process template with placeholders
    personalizedBody = ProcessTemplateForRow(emailTemplate, columnHeaders, rowData)
    
    ' Create email draft
    CreateEmailDraft emailAddress, emailSubject, personalizedBody
End Sub

' =============================================================================
' Process template for a specific row (simplified version without error checking)
' =============================================================================
Private Function ProcessTemplateForRow(template As String, columnHeaders As Variant, rowData As Variant) As String
    Dim result As String
    Dim placeholder As String
    Dim startPos As Long
    Dim endPos As Long
    Dim columnName As String
    Dim replacementValue As String
    
    result = template
    
    ' Find and replace all placeholders [ColumnName]
    startPos = InStr(result, "[")
    Do While startPos > 0
        endPos = InStr(startPos, result, "]")
        If endPos > 0 Then
            ' Extract placeholder and column name
            placeholder = Mid(result, startPos, endPos - startPos + 1)
            columnName = Mid(placeholder, 2, Len(placeholder) - 2)
            
            ' Get replacement value
            replacementValue = GetColumnValue(columnHeaders, rowData, columnName)
            
            ' Replace placeholder with value
            result = Replace(result, placeholder, replacementValue)
            
            ' Find next placeholder
            startPos = InStr(startPos + 1, result, "[")
        Else
            ' No closing bracket found
            startPos = InStr(startPos + 1, result, "[")
        End If
    Loop
    
    ProcessTemplateForRow = result
End Function

' =============================================================================
' Check if column exists in headers
' =============================================================================
Private Function HasColumn(columnHeaders As Variant, columnName As String) As Boolean
    Dim i As Long
    
    ' Handle single cell case
    If Not IsArray(columnHeaders) Then
        HasColumn = (Trim(columnHeaders) = columnName)
        Exit Function
    End If
    
    ' Handle array case
    For i = 1 To UBound(columnHeaders, 2)
        If Trim(columnHeaders(1, i)) = columnName Then
            HasColumn = True
            Exit Function
        End If
    Next i
    
    HasColumn = False
End Function

' =============================================================================
' Initialize Outlook application
' =============================================================================
Private Function InitializeOutlook() As Boolean
    On Error GoTo ErrorHandler
    
    ' Try to get existing Outlook application
    Set outlookApp = GetObject(, "Outlook.Application")
    Set outlookNamespace = outlookApp.GetNamespace("MAPI")
    
    InitializeOutlook = True
    Exit Function
    
ErrorHandler:
    ' Outlook not running, try to start it
    On Error GoTo StartError
    Set outlookApp = CreateObject("Outlook.Application")
    Set outlookNamespace = outlookApp.GetNamespace("MAPI")
    
    InitializeOutlook = True
    Exit Function
    
StartError:
    MsgBox "Error: Could not start or connect to Microsoft Outlook. " & vbCrLf & _
           "Please ensure Outlook is installed and accessible." & vbCrLf & vbCrLf & _
           "Error details: " & Err.Description, _
           vbCritical, "MassiveSend Error"
    InitializeOutlook = False
End Function

' =============================================================================
' Create email draft in Outlook
' =============================================================================
Private Sub CreateEmailDraft(emailAddress As String, emailSubject As String, emailBody As String)
    Dim mailItem As Object
    
    On Error GoTo ErrorHandler
    
    ' Create new mail item
    Set mailItem = outlookApp.CreateItem(0) ' olMailItem = 0
    
    ' Set email properties
    With mailItem
        .To = emailAddress
        .Subject = emailSubject
        .Body = emailBody
        .Display ' Show email draft (don't send automatically)
    End With
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Error creating email draft: " & Err.Description, _
           vbCritical, "MassiveSend Error"
End Sub

' =============================================================================
' Workbook Events - Register Keyboard Shortcut
' =============================================================================
' Note: This code should be placed in ThisWorkbook module

Private Sub Workbook_Open()
    ' Register Ctrl+Shift+D shortcut for SingleSend
    Application.OnKey "^+d", "SingleSend"
    
    ' Register Ctrl+Shift+M shortcut for MassiveSend
    Application.OnKey "^+m", "MassiveSend"
End Sub

Private Sub Workbook_BeforeClose(Cancel As Boolean)
    ' Unregister shortcuts when closing workbook
    Application.OnKey "^+d"
    Application.OnKey "^+m"
End Sub

' =============================================================================
' Alternative shortcut registration (can be called manually)
' =============================================================================
Sub RegisterShortcuts()
    Application.OnKey "^+d", "SingleSend"
    Application.OnKey "^+m", "MassiveSend"
    MsgBox "Keyboard shortcuts registered:" & vbCrLf & _
           "Ctrl+Shift+D for SingleSend" & vbCrLf & _
           "Ctrl+Shift+M for MassiveSend", _
           vbInformation, "Shortcuts Registered"
End Sub

Sub UnregisterShortcuts()
    Application.OnKey "^+d"
    Application.OnKey "^+m"
    MsgBox "All keyboard shortcuts unregistered.", _
           vbInformation, "Shortcuts Unregistered"
End Sub