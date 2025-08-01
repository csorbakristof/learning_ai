' Outlook VBA Macro: Hello World Email Drafter
' This macro adds a button to Outlook that drafts a "Hello World" email

' Module: HelloWorldMacro
' Instructions:
' 1. Open Outlook
' 2. Press Alt+F11 to open VBA Editor
' 3. Right-click on "Project1 (VbaProject.OTM)" in the left panel
' 4. Insert > Module
' 5. Paste this code into the new module
' 6. Save (Ctrl+S)
' 7. Close VBA Editor
' 8. In Outlook: File > Options > Customize Ribbon
' 9. In "Choose commands from" dropdown, select "Macros"
' 10. Find "DraftHelloWorldEmail" and add it to a ribbon tab
' 11. Click OK

Sub DraftHelloWorldEmail()
    ' This subroutine creates a new email with "Hello World" content
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    
    ' Get the Outlook application
    Set olApp = Outlook.Application
    
    ' Create a new mail item
    Set olMail = olApp.CreateItem(olMailItem)
    
    ' Set the email properties
    With olMail
        .Subject = "Hello World from Outlook Macro"
        .Body = "Hello world!" & vbCrLf & vbCrLf & "This email was drafted using an Outlook VBA macro."
        .Display ' Display the email (doesn't send it)
    End With
    
    ' Show a confirmation message
    MsgBox "Hello World email has been drafted!", vbInformation, "Macro Success"
    
    ' Clean up objects
    Set olMail = Nothing
    Set olApp = Nothing
    
End Sub

' Optional: Auto-run macro when Outlook starts
' Uncomment the lines below if you want the macro to be available immediately
'
'Private Sub Application_Startup()
'    ' This runs when Outlook starts
'    MsgBox "Hello World Macro is ready! Look for the button in your ribbon.", vbInformation, "Macro Loaded"
'End Sub

' Alternative version: Draft email with more formatting
Sub DraftHelloWorldEmailFormatted()
    ' This version creates a more formatted email
    
    Dim olApp As Outlook.Application
    Dim olMail As Outlook.MailItem
    
    Set olApp = Outlook.Application
    Set olMail = olApp.CreateItem(olMailItem)
    
    With olMail
        .Subject = "Hello World from Outlook Macro"
        .HTMLBody = "<html><body>" & _
                   "<h2 style='color: blue;'>Hello World!</h2>" & _
                   "<p>This email was drafted using an <strong>Outlook VBA macro</strong>.</p>" & _
                   "<p>Features:</p>" & _
                   "<ul>" & _
                   "<li>✓ No server required</li>" & _
                   "<li>✓ Works with domain policies</li>" & _
                   "<li>✓ Runs locally in Outlook</li>" & _
                   "</ul>" & _
                   "<p><em>Created on: " & Now() & "</em></p>" & _
                   "</body></html>"
        .Display
    End With
    
    MsgBox "Formatted Hello World email has been drafted!", vbInformation, "Macro Success"
    
    Set olMail = Nothing
    Set olApp = Nothing
    
End Sub

' Quick test macro to verify VBA is working
Sub TestMacro()
    MsgBox "VBA Macros are working in Outlook!", vbInformation, "Test Success"
End Sub
