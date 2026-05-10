' =============================================================================
' Excel2Outlook - SingleSend and MassiveSend Features (Refactored)
' =============================================================================
' [SingleSend] - Sends personalized email for current row
' Triggered by: Ctrl+Shift+D from current row in UserList worksheet
' 
' [MassiveSend] - Sends personalized emails for all visible rows
' Triggered by: Ctrl+Shift+M from UserList worksheet
'
' Template source: "EmailTemplate" worksheet, cell A1
' File attachments: Optional "FileToAttach" column with filename (relative to workbook path)
' =============================================================================

Option Explicit

' Constants
Private Const EMAIL_TEMPLATE_WORKSHEET = "EmailTemplate"
Private Const EMAIL_TEMPLATE_CELL = "A1"
Private Const EMAIL_COLUMN = "email"
Private Const SUBJECT_COLUMN = "Subject"
Private Const FILE_TO_ATTACH_COLUMN = "FileToAttach"
Private Const EMAIL_CONFIRMATION_THRESHOLD = 20
Private Const HEADER_ROW = 1
Private Const FIRST_DATA_ROW = 2

' Global variables for Outlook application
Private outlookApp As Object
Private outlookNamespace As Object

' Data structure for email context
Private Type EmailContext
    UserListWs As Worksheet
    TemplateWs As Worksheet
    EmailTemplate As String
    ColumnHeaders As Variant
    CurrentRow As Long
End Type

' =============================================================================
' Main SingleSend Macro - Entry Point
' =============================================================================
Sub SingleSend()
    On Error GoTo ErrorHandler
    
    Dim context As EmailContext
    Dim validationErrors As String
    
    ' Validate current row (must be > 1 since row 1 contains headers)
    If ActiveCell.Row <= HEADER_ROW Then
        ShowError "Please select a data row (not the header row) before running SingleSend.", "SingleSend"
        Exit Sub
    End If
    
    ' Initialize email context
    If Not InitializeEmailContext(context, ActiveCell.Row) Then Exit Sub
    
    ' Validate the current row data
    validationErrors = ValidateRowData(context.UserListWs, context.CurrentRow, context.ColumnHeaders, context.EmailTemplate)
    If validationErrors <> "" Then
        ShowError "Validation error in row " & context.CurrentRow & ": " & validationErrors, "SingleSend"
        Exit Sub
    End If
    
    ' Initialize Outlook connection
    If Not InitializeOutlook() Then Exit Sub
    
    ' Create email draft for current row
    If CreateEmailFromRow(context.UserListWs, context.CurrentRow, context.ColumnHeaders, context.EmailTemplate) Then
        Dim emailAddress As String
        emailAddress = GetColumnValue(context.ColumnHeaders, GetRowData(context.UserListWs, context.CurrentRow), EMAIL_COLUMN)
        ShowSuccess "Email draft created successfully for " & emailAddress, "SingleSend"
    End If
    
    Exit Sub

ErrorHandler:
    ShowError "Unexpected error: " & Err.Description & vbCrLf & "Error Number: " & Err.Number, "SingleSend"
End Sub

' =============================================================================
' Main MassiveSend Macro - Entry Point
' =============================================================================
Sub MassiveSend()
    On Error GoTo ErrorHandler
    
    Dim context As EmailContext
    Dim visibleRows As Collection
    Dim totalEmails As Long
    Dim currentRow As Long
    Dim i As Long
    Dim confirmResult As VbMsgBoxResult
    Dim validationErrors As String
    
    ' Initialize email context using first visible row for structure validation
    If Not InitializeEmailContext(context, FIRST_DATA_ROW) Then Exit Sub
    
    ' Get all visible rows (excluding header row)
    Set visibleRows = GetVisibleRows(context.UserListWs)
    totalEmails = visibleRows.Count
    
    If totalEmails = 0 Then
        ShowSuccess "No visible data rows found to process.", "MassiveSend Info"
        Exit Sub
    End If
    
    ' Ask for confirmation if more than threshold
    If totalEmails > EMAIL_CONFIRMATION_THRESHOLD Then
        confirmResult = MsgBox("This will create " & totalEmails & " email drafts. " & vbCrLf & _
                              "Are you sure you want to continue?", _
                              vbYesNo + vbQuestion, "MassiveSend Confirmation")
        If confirmResult = vbNo Then
            Exit Sub
        End If
    End If
    
    ' Pre-validate ALL rows before creating any emails
    If Not PreValidateAllRows(context.UserListWs, visibleRows, context.ColumnHeaders, context.EmailTemplate) Then
        Exit Sub ' Error already shown in PreValidateAllRows
    End If
    
    ' Initialize Outlook connection
    If Not InitializeOutlook() Then Exit Sub
    
    ' Create email drafts for all visible rows
    For i = 1 To visibleRows.Count
        currentRow = visibleRows(i)
        If Not CreateEmailFromRow(context.UserListWs, currentRow, context.ColumnHeaders, context.EmailTemplate) Then
            ShowError "Failed to create email for row " & currentRow & ". Process stopped.", "MassiveSend"
            Exit Sub
        End If
    Next i
    
    ' Show success summary
    ShowSuccess totalEmails & " email drafts created successfully!", "MassiveSend Success"
    
    Exit Sub

ErrorHandler:
    ShowError "Unexpected error: " & Err.Description & vbCrLf & "Error Number: " & Err.Number, "MassiveSend"
End Sub

' =============================================================================
' Get EmailTemplate worksheet
' =============================================================================
Private Function GetEmailTemplateWorksheet() As Worksheet
    Dim ws As Worksheet
    
    ' Look for "EmailTemplate" worksheet (case-sensitive)
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name = EMAIL_TEMPLATE_WORKSHEET Then
            Set GetEmailTemplateWorksheet = ws
            Exit Function
        End If
    Next ws
    
    ' Not found - show error using standardized function
    ShowError "Worksheet named '" & EMAIL_TEMPLATE_WORKSHEET & "' not found. " & vbCrLf & _
              "Please create a worksheet named exactly '" & EMAIL_TEMPLATE_WORKSHEET & "' with the email template in cell " & EMAIL_TEMPLATE_CELL & ".", _
              "Template Error"
    
    Set GetEmailTemplateWorksheet = Nothing
End Function

' =============================================================================
' Get column headers from row 1
' =============================================================================
Private Function GetColumnHeaders(ws As Worksheet) As Variant
    Dim lastCol As Long
    Dim headers As Variant
    
    ' Find last column with data in row 1
    lastCol = ws.Cells(HEADER_ROW, ws.Columns.Count).End(xlToLeft).Column
    
    If lastCol = 1 And Trim(ws.Cells(HEADER_ROW, 1).Value) = "" Then
        ShowError "No column headers found in row " & HEADER_ROW & " of the current worksheet.", "Header Error"
        GetColumnHeaders = Empty
        Exit Function
    End If
    
    ' Get headers as array
    headers = ws.Range(ws.Cells(HEADER_ROW, 1), ws.Cells(HEADER_ROW, lastCol)).Value
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
            If Trim(columnHeaders(1, i)) = EMAIL_COLUMN Then foundEmail = True
            If Trim(columnHeaders(1, i)) = SUBJECT_COLUMN Then foundSubject = True
        Next i
    Else
        ' Single cell case
        If Trim(columnHeaders) = EMAIL_COLUMN Then foundEmail = True
        If Trim(columnHeaders) = SUBJECT_COLUMN Then foundSubject = True
    End If
    
    ' Report missing columns using standardized error function
    If Not foundEmail And Not foundSubject Then
        ShowError "Required columns '" & EMAIL_COLUMN & "' and '" & SUBJECT_COLUMN & "' are missing from row " & HEADER_ROW & ". " & vbCrLf & _
                  "Column names are case-sensitive and must match exactly.", featureName
        ValidateRequiredColumns = False
    ElseIf Not foundEmail Then
        ShowError "Required column '" & EMAIL_COLUMN & "' is missing from row " & HEADER_ROW & ". " & vbCrLf & _
                  "Column name is case-sensitive and must match exactly.", featureName
        ValidateRequiredColumns = False
    ElseIf Not foundSubject Then
        ShowError "Required column '" & SUBJECT_COLUMN & "' is missing from row " & HEADER_ROW & ". " & vbCrLf & _
                  "Column name is case-sensitive and must match exactly.", featureName
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
    
    ' Find last column with data in headers row
    lastCol = ws.Cells(HEADER_ROW, ws.Columns.Count).End(xlToLeft).Column
    
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
        ShowError "Missing or empty placeholder values in row " & currentRow & ":" & vbCrLf & _
                  missingPlaceholders & vbCrLf & vbCrLf & _
                  "Please ensure all placeholder columns exist and have values.", "Template Processing"
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
    
    ' Collect visible rows (starting from first data row, skipping headers)
    For i = FIRST_DATA_ROW To lastRow
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
    Dim validationResult As String
    Dim templateValidationResult As String
    Dim errorMessages As String
    
    errorMessages = ""
    
    ' Validate each visible row using centralized validation
    For i = 1 To visibleRows.Count
        currentRow = visibleRows(i)
        
        ' Use centralized row validation (includes file attachment checks)
        validationResult = ValidateRowData(ws, currentRow, columnHeaders, emailTemplate)
        If validationResult <> "" Then
            errorMessages = errorMessages & "Row " & currentRow & ": " & validationResult & vbCrLf
        End If
        
        ' Additional template placeholder validation
        templateValidationResult = ValidateTemplatePlaceholders(emailTemplate, columnHeaders, GetRowData(ws, currentRow), currentRow)
        If templateValidationResult <> "" Then
            errorMessages = errorMessages & "Row " & currentRow & ": " & templateValidationResult & vbCrLf
        End If
    Next i
    
    ' Show errors if any found
    If errorMessages <> "" Then
        ShowError "Validation errors found. No emails will be created:" & vbCrLf & vbCrLf & _
                  errorMessages, "MassiveSend Validation"
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
    ShowError "Could not start or connect to Microsoft Outlook. " & vbCrLf & _
              "Please ensure Outlook is installed and accessible." & vbCrLf & vbCrLf & _
              "Error details: " & Err.Description, "Outlook Connection"
    InitializeOutlook = False
End Function

' =============================================================================
' Create email draft in Outlook
' =============================================================================
Private Sub CreateEmailDraft(emailAddress As String, emailSubject As String, emailBody As String, Optional columnHeaders As Variant, Optional rowData As Variant)
    Dim mailItem As Object
    
    On Error GoTo ErrorHandler
    
    ' Create new mail item
    Set mailItem = outlookApp.CreateItem(0) ' olMailItem = 0
    
    ' Set email properties
    With mailItem
        .To = emailAddress
        .Subject = emailSubject
        .Body = emailBody
        
        ' Attach file if column headers and row data are provided
        If Not IsMissing(columnHeaders) And Not IsMissing(rowData) Then
            AttachFileToEmail mailItem, columnHeaders, rowData
        End If
        
        .Display ' Show email draft (don't send automatically)
    End With
    
    Exit Sub
    
ErrorHandler:
    ShowError "Error creating email draft: " & Err.Description, "Email Creation"
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
    ShowSuccess "Keyboard shortcuts registered:" & vbCrLf & _
                "Ctrl+Shift+D for SingleSend" & vbCrLf & _
                "Ctrl+Shift+M for MassiveSend", "Shortcuts Registered"
End Sub

Sub UnregisterShortcuts()
    Application.OnKey "^+d"
    Application.OnKey "^+m"
    ShowSuccess "All keyboard shortcuts unregistered.", "Shortcuts Unregistered"
End Sub

' =============================================================================
' Enhanced Helper Functions for Refactored Code
' =============================================================================

' Initialize EmailContext structure with validation
Private Function InitializeEmailContext(ByRef context As EmailContext, currentRow As Long) As Boolean
    On Error GoTo ErrorHandler
    
    ' Initialize basic properties
    Set context.UserListWs = ActiveSheet
    context.CurrentRow = currentRow
    
    ' Get and validate email template worksheet
    Set context.TemplateWs = GetEmailTemplateWorksheet()
    If context.TemplateWs Is Nothing Then
        InitializeEmailContext = False
        Exit Function
    End If
    
    ' Get email template from EmailTemplate!A1
    context.EmailTemplate = context.TemplateWs.Range(EMAIL_TEMPLATE_CELL).Value
    If Trim(context.EmailTemplate) = "" Then
        ShowError "Email template in '" & EMAIL_TEMPLATE_WORKSHEET & "' worksheet, cell " & EMAIL_TEMPLATE_CELL & " is empty.", "Template Error"
        InitializeEmailContext = False
        Exit Function
    End If
    
    ' Get column headers and validate required columns
    context.ColumnHeaders = GetColumnHeaders(context.UserListWs)
    If IsEmpty(context.ColumnHeaders) Then
        InitializeEmailContext = False
        Exit Function
    End If
    
    ' Validate required columns exist
    If Not ValidateRequiredColumns(context.ColumnHeaders, "Email Context") Then
        InitializeEmailContext = False
        Exit Function
    End If
    
    InitializeEmailContext = True
    Exit Function
    
ErrorHandler:
    ShowError "Error initializing email context: " & Err.Description, "Initialization Error"
    InitializeEmailContext = False
End Function

' Validate row data for required fields
Private Function ValidateRowData(ws As Worksheet, rowNum As Long, columnHeaders As Variant, emailTemplate As String) As String
    Dim rowData As Variant
    Dim emailAddress As String
    Dim emailSubject As String
    Dim errors As String
    
    ' Get row data
    rowData = GetRowData(ws, rowNum)
    
    ' Check email address
    emailAddress = GetColumnValue(columnHeaders, rowData, EMAIL_COLUMN)
    If Trim(emailAddress) = "" Then
        errors = errors & "Email address is empty. "
    End If
    
    ' Check subject
    emailSubject = GetColumnValue(columnHeaders, rowData, SUBJECT_COLUMN)
    If Trim(emailSubject) = "" Then
        errors = errors & "Subject is empty. "
    End If
    
    ' Check file attachment (optional column)
    If HasColumn(columnHeaders, FILE_TO_ATTACH_COLUMN) Then
        Dim fileToAttach As String
        fileToAttach = GetColumnValue(columnHeaders, rowData, FILE_TO_ATTACH_COLUMN)
        If Trim(fileToAttach) <> "" Then
            Dim fullFilePath As String
            fullFilePath = ThisWorkbook.Path & "\" & fileToAttach
            If Not FileExists(fullFilePath) Then
                errors = errors & "Attachment file '" & fileToAttach & "' not found. "
            End If
        End If
    End If
    
    ' Additional template validation could be added here
    
    ValidateRowData = Trim(errors)
End Function

' Create email from row data using consolidated logic
Private Function CreateEmailFromRow(ws As Worksheet, rowNum As Long, columnHeaders As Variant, emailTemplate As String) As Boolean
    On Error GoTo ErrorHandler
    
    Dim rowData As Variant
    Dim emailAddress As String
    Dim emailSubject As String
    Dim personalizedBody As String
    
    ' Get row data
    rowData = GetRowData(ws, rowNum)
    
    ' Extract email details
    emailAddress = GetColumnValue(columnHeaders, rowData, EMAIL_COLUMN)
    emailSubject = GetColumnValue(columnHeaders, rowData, SUBJECT_COLUMN)
    
    ' Process template with placeholders
    personalizedBody = ProcessTemplate(emailTemplate, columnHeaders, rowData, rowNum)
    If personalizedBody = "" Then
        CreateEmailFromRow = False
        Exit Function
    End If
    
    ' Create email draft with file attachment support
    CreateEmailDraft emailAddress, emailSubject, personalizedBody, columnHeaders, rowData
    CreateEmailFromRow = True
    Exit Function
    
ErrorHandler:
    ShowError "Error creating email for row " & rowNum & ": " & Err.Description, "Email Creation Error"
    CreateEmailFromRow = False
End Function

' Standardized error display
Private Sub ShowError(message As String, title As String)
    MsgBox "Error: " & message, vbCritical, title
End Sub

' Standardized success display
Private Sub ShowSuccess(message As String, title As String)
    MsgBox message, vbInformation, title
End Sub

' Check if file exists
Private Function FileExists(filePath As String) As Boolean
    FileExists = (Dir(filePath) <> "")
End Function

' Attach file to email if specified
Private Sub AttachFileToEmail(emailItem As Object, columnHeaders As Variant, rowData As Variant)
    On Error GoTo ErrorHandler
    
    ' Check if FileToAttach column exists
    If Not HasColumn(columnHeaders, FILE_TO_ATTACH_COLUMN) Then Exit Sub
    
    ' Get file attachment value
    Dim fileToAttach As String
    fileToAttach = GetColumnValue(columnHeaders, rowData, FILE_TO_ATTACH_COLUMN)
    
    ' If no file specified, exit
    If Trim(fileToAttach) = "" Then Exit Sub
    
    ' Build full file path
    Dim fullFilePath As String
    fullFilePath = ThisWorkbook.Path & "\" & fileToAttach
    
    ' Attach file (validation already done in ValidateRowData)
    emailItem.Attachments.Add fullFilePath
    
    Exit Sub
    
ErrorHandler:
    ShowError "Error attaching file '" & fileToAttach & "': " & Err.Description, "File Attachment Error"
End Sub