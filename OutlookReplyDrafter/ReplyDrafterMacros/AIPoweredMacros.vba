' AI-Powered Outlook VBA Macros with Backend Integration
' This connects to the same backend server as the outlook-addin
' Requires: Microsoft XML, v6.0 reference (for HTTP requests)

' Configuration
Const BACKEND_URL As String = "http://localhost:5000"

' Main AI Email Analysis Macro
Sub AnalyzeEmailWithAI()
    ' Analyzes the currently selected email using AI backend
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    Dim selectedItem As Object
    
    Set olApp = Outlook.Application
    
    ' Get the selected email
    If olApp.ActiveExplorer.Selection.Count > 0 Then
        Set selectedItem = olApp.ActiveExplorer.Selection.Item(1)
        
        If TypeOf selectedItem Is Outlook.MailItem Then
            Set olMail = selectedItem
            
            ' Call AI analysis (processing happens in background)
            AnalyzeWithBackend olMail
        Else
            MsgBox "Please select an email to analyze.", vbInformation, "No Email Selected"
        End If
    Else
        MsgBox "Please select an email to analyze.", vbInformation, "No Email Selected"
    End If
    
    Set olMail = Nothing
    Set olApp = Nothing
End Sub

' AI Email Composition Assistant
Sub ComposeEmailWithAI()
    ' Opens a new email and provides AI assistance for composition
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    Dim draftContent As String
    
    Set olApp = Outlook.Application
    Set olMail = olApp.CreateItem(olMailItem)
    
    ' Get initial draft from user
    draftContent = InputBox("Enter your initial email draft (or leave blank for a template):", _
                           "AI Email Assistant", _
                           "Hi," & vbCrLf & vbCrLf & "I wanted to reach out regarding..." & vbCrLf & vbCrLf & "Best regards")
    
    If draftContent <> "" Then
        ' Get AI-improved version
        Dim improvedContent As String
        improvedContent = ImproveEmailWithBackend(draftContent)
        
        ' Create the email with AI-improved content
        With olMail
            .Subject = "AI-Assisted Email"
            .Body = improvedContent
            .Display
        End With
    Else
        MsgBox "Email composition cancelled.", vbInformation, "Cancelled"
    End If
    
    Set olMail = Nothing
    Set olApp = Nothing
End Sub

' Smart Reply Generator
Sub GenerateSmartReply()
    ' Generates an AI reply to the currently selected email
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    Dim replyMail As Outlook.MailItem
    Dim selectedItem As Object
    
    Set olApp = Outlook.Application
    
    ' Get the selected email
    If olApp.ActiveExplorer.Selection.Count > 0 Then
        Set selectedItem = olApp.ActiveExplorer.Selection.Item(1)
        
        If TypeOf selectedItem Is Outlook.MailItem Then
            Set olMail = selectedItem
            
            ' Analyze the email and get suggested reply
            Dim aiResponse As String
            aiResponse = AnalyzeEmailForReply(olMail)
            
            ' Create reply with AI suggestion
            Set replyMail = olMail.Reply
            With replyMail
                .Body = aiResponse & vbCrLf & vbCrLf & .Body
                .Display
            End With
        Else
            MsgBox "Please select an email to reply to.", vbInformation, "No Email Selected"
        End If
    Else
        MsgBox "Please select an email to reply to.", vbInformation, "No Email Selected"
    End If
    
    Set replyMail = Nothing
    Set olMail = Nothing
    Set olApp = Nothing
End Sub

' Backend Communication Functions
Private Sub AnalyzeWithBackend(email As Outlook.MailItem)
    ' Sends email to backend for analysis and shows results
    
    Dim response As String
    response = CallAnalyzeEmailAPI(email.Subject, email.SenderEmailAddress, email.Body)
    
    If response <> "" Then
        ' Show the AI analysis results to the user
        MsgBox "AI Analysis Results:" & vbCrLf & vbCrLf & response, vbInformation, "Email Analysis"
        
        ' Add category or flag based on analysis (silent operation)
        If InStr(response, "TASK_REQUIRED") > 0 Then
            email.Categories = "AI-Task Required"
            email.FlagStatus = olFlagMarked
        ElseIf InStr(response, "EASY_REPLY") > 0 Then
            email.Categories = "AI-Easy Reply"
        Else
            email.Categories = "AI-No Action"
        End If
        
        email.Save
    Else
        MsgBox "Failed to analyze email. Please check if the backend server is running.", vbError, "Analysis Failed"
    End If
End Sub

Private Function ImproveEmailWithBackend(draft As String) As String
    ' Sends draft to backend for improvement
    
    Dim response As String
    response = CallComposeEmailAPI(draft)
    
    If response <> "" Then
        ' Show the AI improvement results to the user
        MsgBox "AI Email Improvement:" & vbCrLf & vbCrLf & _
               "Original:" & vbCrLf & Left(draft, 100) & "..." & vbCrLf & vbCrLf & _
               "AI Improved:" & vbCrLf & Left(response, 150) & "...", _
               vbInformation, "Email Enhanced"
        
        ImproveEmailWithBackend = response
    Else
        MsgBox "Failed to improve email. Using original draft.", vbWarning, "Improvement Failed"
        ImproveEmailWithBackend = draft
    End If
End Function

Private Function AnalyzeEmailForReply(email As Outlook.MailItem) As String
    ' Analyzes email and extracts reply suggestion
    
    Dim response As String
    response = CallAnalyzeEmailAPI(email.Subject, email.SenderEmailAddress, email.Body)
    
    If response <> "" Then
        ' Show the AI analysis to the user before creating reply
        MsgBox "AI Reply Analysis:" & vbCrLf & vbCrLf & response, vbInformation, "Smart Reply Generation"
        
        ' Extract reply suggestion from response
        ' This is a simple extraction - you might want to improve this
        If InStr(response, "Reply:") > 0 Then
            AnalyzeEmailForReply = Mid(response, InStr(response, "Reply:") + 6)
        Else
            AnalyzeEmailForReply = "Thank you for your email. I'll review this and get back to you soon." & vbCrLf & vbCrLf & _
                                  "AI Analysis: " & response
        End If
    Else
        AnalyzeEmailForReply = "Thank you for your email. I'll get back to you soon."
    End If
End Function

' HTTP API Call Functions
Private Function CallAnalyzeEmailAPI(subject As String, sender As String, body As String) As String
    ' Calls the /analyze-email endpoint
    
    Dim http As Object
    Dim url As String
    Dim jsonData As String
    Dim response As String
    
    Set http = CreateObject("MSXML2.XMLHTTP.6.0")
    url = BACKEND_URL & "/analyze-email"
    
    ' Create JSON payload
    jsonData = "{" & _
              """subject"": """ & EscapeJson(subject) & """," & _
              """sender"": """ & EscapeJson(sender) & """," & _
              """body"": """ & EscapeJson(body) & """" & _
              "}"
    
    On Error GoTo ErrorHandler
    
    ' Make the HTTP request
    http.Open "POST", url, False
    http.setRequestHeader "Content-Type", "application/json"
    http.send jsonData
    
    If http.Status = 200 Then
        ' Parse JSON response (simple extraction)
        response = http.responseText
        response = ExtractJsonValue(response, "response")
        CallAnalyzeEmailAPI = response
    Else
        CallAnalyzeEmailAPI = ""
    End If
    
    Set http = Nothing
    Exit Function
    
ErrorHandler:
    CallAnalyzeEmailAPI = ""
    Set http = Nothing
End Function

Private Function CallComposeEmailAPI(draft As String) As String
    ' Calls the /compose-email endpoint
    
    Dim http As Object
    Dim url As String
    Dim jsonData As String
    Dim response As String
    
    Set http = CreateObject("MSXML2.XMLHTTP.6.0")
    url = BACKEND_URL & "/compose-email"
    
    ' Create JSON payload
    jsonData = "{" & _
              """draft"": """ & EscapeJson(draft) & """" & _
              "}"
    
    On Error GoTo ErrorHandler
    
    ' Make the HTTP request
    http.Open "POST", url, False
    http.setRequestHeader "Content-Type", "application/json"
    http.send jsonData
    
    If http.Status = 200 Then
        ' Parse JSON response (simple extraction)
        response = http.responseText
        response = ExtractJsonValue(response, "response")
        CallComposeEmailAPI = response
    Else
        CallComposeEmailAPI = ""
    End If
    
    Set http = Nothing
    Exit Function
    
ErrorHandler:
    CallComposeEmailAPI = ""
    Set http = Nothing
End Function

' Utility Functions
Private Function EscapeJson(text As String) As String
    ' Simple JSON escaping
    text = Replace(text, "\", "\\")
    text = Replace(text, """", "\""")
    text = Replace(text, vbCrLf, "\n")
    text = Replace(text, vbCr, "\n")
    text = Replace(text, vbLf, "\n")
    text = Replace(text, vbTab, "\t")
    EscapeJson = text
End Function

Private Function ExtractJsonValue(jsonText As String, key As String) As String
    ' Simple JSON value extraction
    Dim startPos As Long
    Dim endPos As Long
    Dim searchKey As String
    
    searchKey = """" & key & """:"
    startPos = InStr(jsonText, searchKey)
    
    If startPos > 0 Then
        startPos = startPos + Len(searchKey)
        ' Skip whitespace and opening quote
        Do While Mid(jsonText, startPos, 1) = " "
            startPos = startPos + 1
        Loop
        If Mid(jsonText, startPos, 1) = """" Then
            startPos = startPos + 1
        End If
        
        ' Find closing quote
        endPos = startPos
        Do While endPos <= Len(jsonText)
            If Mid(jsonText, endPos, 1) = """" And Mid(jsonText, endPos - 1, 1) <> "\" Then
                Exit Do
            End If
            endPos = endPos + 1
        Loop
        
        ExtractJsonValue = Mid(jsonText, startPos, endPos - startPos)
        ' Unescape basic JSON escape sequences
        ExtractJsonValue = Replace(ExtractJsonValue, "\n", vbCrLf)
        ExtractJsonValue = Replace(ExtractJsonValue, "\""", """")
        ExtractJsonValue = Replace(ExtractJsonValue, "\\", "\")
    Else
        ExtractJsonValue = ""
    End If
End Function

' Test Backend Connection
Sub TestBackendConnection()
    ' Tests if the backend server is accessible
    
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP.6.0")
    
    On Error GoTo ErrorHandler
    
    http.Open "GET", BACKEND_URL, False
    http.send
    
    If http.Status = 200 Or http.Status = 404 Then
        MsgBox "✅ Backend server is running at " & BACKEND_URL, vbInformation, "Connection Test"
    Else
        MsgBox "⚠️ Backend server responded with status: " & http.Status, vbWarning, "Connection Test"
    End If
    
    Set http = Nothing
    Exit Sub
    
ErrorHandler:
    MsgBox "❌ Cannot connect to backend server at " & BACKEND_URL & vbCrLf & vbCrLf & _
           "Please ensure:" & vbCrLf & _
           "1. Backend server is running (npm start in backend folder)" & vbCrLf & _
           "2. Server is accessible on port 5000" & vbCrLf & _
           "3. No firewall blocking the connection", vbError, "Connection Failed"
    Set http = Nothing
End Sub

' Show Available AI Macros
Sub ShowAIMacros()
    Dim macroList As String
    
    macroList = "Available AI-Powered Macros:" & vbCrLf & vbCrLf & _
               "🤖 AnalyzeEmailWithAI - Analyze selected email with AI (silent)" & vbCrLf & _
               "📋 ShowLastAnalysis - Show detailed analysis of selected email" & vbCrLf & _
               "✍️ ComposeEmailWithAI - AI-assisted email composition" & vbCrLf & _
               "💬 GenerateSmartReply - Generate AI reply to selected email" & vbCrLf & _
               "🔧 TestBackendConnection - Test connection to AI backend" & vbCrLf & vbCrLf & _
               "Requirements:" & vbCrLf & _
               "• Backend server running on " & BACKEND_URL & vbCrLf & _
               "• Internet connection for OpenAI API" & vbCrLf & vbCrLf & _
               "To add these to your ribbon:" & vbCrLf & _
               "File → Options → Customize Ribbon → Choose commands from: Macros"
    
    MsgBox macroList, vbInformation, "AI Macros"
End Sub

' Show Detailed Analysis for Selected Email
Sub ShowLastAnalysis()
    ' Shows the full AI analysis for the currently selected email
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    Dim selectedItem As Object
    
    Set olApp = Outlook.Application
    
    ' Get the selected email
    If olApp.ActiveExplorer.Selection.Count > 0 Then
        Set selectedItem = olApp.ActiveExplorer.Selection.Item(1)
        
        If TypeOf selectedItem Is Outlook.MailItem Then
            Set olMail = selectedItem
            
            Dim response As String
            response = CallAnalyzeEmailAPI(olMail.Subject, olMail.SenderEmailAddress, olMail.Body)
            
            If response <> "" Then
                ' Show detailed analysis in message box
                MsgBox "Detailed AI Analysis:" & vbCrLf & vbCrLf & response, vbInformation, "Email Analysis Details"
            Else
                MsgBox "Failed to get AI analysis. Please check if the backend server is running.", vbError, "Analysis Failed"
            End If
        Else
            MsgBox "Please select an email to analyze.", vbInformation, "No Email Selected"
        End If
    Else
        MsgBox "Please select an email to analyze.", vbInformation, "No Email Selected"
    End If
    
    Set olMail = Nothing
    Set olApp = Nothing
End Sub
