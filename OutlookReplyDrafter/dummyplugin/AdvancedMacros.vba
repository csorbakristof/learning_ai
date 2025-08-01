' Advanced Outlook VBA Macros: Multiple Email Templates
' This provides more sophisticated email drafting capabilities

' Advanced Hello World Email Drafter with Options
Sub DraftHelloWorldEmailAdvanced()
    ' This version prompts user for options and creates customized emails
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    Dim userChoice As Integer
    Dim customMessage As String
    
    Set olApp = Outlook.Application
    
    ' Prompt user for email type
    userChoice = MsgBox("Choose email type:" & vbCrLf & vbCrLf & _
                       "YES = Simple Hello World" & vbCrLf & _
                       "NO = Custom Message" & vbCrLf & _
                       "CANCEL = Formatted Hello World", _
                       vbYesNoCancel + vbQuestion, "Email Type Selection")
    
    Set olMail = olApp.CreateItem(olMailItem)
    
    Select Case userChoice
        Case vbYes ' Simple Hello World
            With olMail
                .Subject = "Hello World from Outlook Macro"
                .Body = "Hello world!"
                .Display
            End With
            
        Case vbNo ' Custom Message
            customMessage = InputBox("Enter your custom message:", "Custom Email", "Hello world!")
            If customMessage <> "" Then
                With olMail
                    .Subject = "Custom Message from Outlook Macro"
                    .Body = customMessage & vbCrLf & vbCrLf & "Sent via Outlook VBA Macro"
                    .Display
                End With
            Else
                MsgBox "Email creation cancelled.", vbInformation
                Exit Sub
            End If
            
        Case vbCancel ' Formatted Hello World
            With olMail
                .Subject = "Formatted Hello World"
                .HTMLBody = CreateFormattedHelloWorldHTML()
                .Display
            End With
            
        Case Else
            MsgBox "Email creation cancelled.", vbInformation
            Exit Sub
    End Select
    
    MsgBox "Email drafted successfully!", vbInformation, "Success"
    
    Set olMail = Nothing
    Set olApp = Nothing
End Sub

' Helper function to create formatted HTML content
Private Function CreateFormattedHelloWorldHTML() As String
    Dim htmlContent As String
    
    htmlContent = "<html><head><style>" & _
                 "body { font-family: Arial, sans-serif; margin: 20px; }" & _
                 ".header { color: #0078d4; font-size: 24px; font-weight: bold; }" & _
                 ".content { font-size: 14px; line-height: 1.6; }" & _
                 ".highlight { background-color: #fff2cc; padding: 10px; border-left: 4px solid #0078d4; }" & _
                 ".footer { font-size: 12px; color: #666; margin-top: 20px; }" & _
                 "</style></head><body>" & _
                 "<div class='header'>🌍 Hello World!</div>" & _
                 "<div class='content'>" & _
                 "<p>This is a <strong>formatted email</strong> created using an Outlook VBA macro.</p>" & _
                 "<div class='highlight'>" & _
                 "<p><strong>Key Features:</strong></p>" & _
                 "<ul>" & _
                 "<li>✅ No external server required</li>" & _
                 "<li>✅ Works with corporate domain policies</li>" & _
                 "<li>✅ Fully customizable</li>" & _
                 "<li>✅ Instant email drafting</li>" & _
                 "</ul>" & _
                 "</div>" & _
                 "<p>You can modify this macro to create any type of email template you need!</p>" & _
                 "</div>" & _
                 "<div class='footer'>" & _
                 "<hr>" & _
                 "<p><em>Generated on: " & Format(Now(), "dddd, mmmm dd, yyyy 'at' hh:mm AM/PM") & "</em></p>" & _
                 "<p><em>Powered by Outlook VBA Macros</em></p>" & _
                 "</div>" & _
                 "</body></html>"
    
    CreateFormattedHelloWorldHTML = htmlContent
End Function

' Quick Email Templates
Sub DraftMeetingRequest()
    ' Creates a meeting request email draft
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    
    Set olApp = Outlook.Application
    Set olMail = olApp.CreateItem(olMailItem)
    
    With olMail
        .Subject = "Meeting Request - Hello World Discussion"
        .Body = "Hi," & vbCrLf & vbCrLf & _
               "I'd like to schedule a meeting to discuss our Hello World project." & vbCrLf & vbCrLf & _
               "Proposed agenda:" & vbCrLf & _
               "- Project overview" & vbCrLf & _
               "- Technical implementation" & vbCrLf & _
               "- Next steps" & vbCrLf & vbCrLf & _
               "Please let me know your availability." & vbCrLf & vbCrLf & _
               "Best regards"
        .Display
    End With
    
    Set olMail = Nothing
    Set olApp = Nothing
End Sub

Sub DraftFollowUpEmail()
    ' Creates a follow-up email draft
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    
    Set olApp = Outlook.Application
    Set olMail = olApp.CreateItem(olMailItem)
    
    With olMail
        .Subject = "Follow-up: Hello World Project"
        .Body = "Hi," & vbCrLf & vbCrLf & _
               "I wanted to follow up on our Hello World project discussion." & vbCrLf & vbCrLf & _
               "Action items:" & vbCrLf & _
               "□ Review implementation approach" & vbCrLf & _
               "□ Set up development environment" & vbCrLf & _
               "□ Schedule next meeting" & vbCrLf & vbCrLf & _
               "Please let me know if you have any questions." & vbCrLf & vbCrLf & _
               "Thanks!"
        .Display
    End With
    
    Set olMail = Nothing
    Set olApp = Nothing
End Sub

' Utility macro to show all available custom macros
Sub ShowAvailableMacros()
    Dim macroList As String
    
    macroList = "Available Custom Macros:" & vbCrLf & vbCrLf & _
               "📧 DraftHelloWorldEmail - Basic hello world email" & vbCrLf & _
               "🎨 DraftHelloWorldEmailFormatted - HTML formatted version" & vbCrLf & _
               "⚙️ DraftHelloWorldEmailAdvanced - Interactive version with options" & vbCrLf & _
               "📅 DraftMeetingRequest - Meeting request template" & vbCrLf & _
               "📝 DraftFollowUpEmail - Follow-up email template" & vbCrLf & _
               "🔧 TestMacro - Test if VBA is working" & vbCrLf & vbCrLf & _
               "To add these to your ribbon:" & vbCrLf & _
               "File → Options → Customize Ribbon → Choose commands from: Macros"
    
    MsgBox macroList, vbInformation, "Available Macros"
End Sub
