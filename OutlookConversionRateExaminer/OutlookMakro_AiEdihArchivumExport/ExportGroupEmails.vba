Option Explicit
' Needs: ai-edih-archivum group has to be among the "Kedvencek" and "Beérkezõ levelek" must not be there.

' Macro to export all emails from the ai-edih-archivum group folder to a text file
Sub ExportGroupEmailsToTextFile()
    Dim objOutlook As Outlook.Application
    Dim objNamespace As Outlook.NameSpace
    Dim objFolder As Outlook.MAPIFolder
    Dim objItem As Object
    Dim objMail As Outlook.MailItem
    Dim strFilePath As String
    Dim objStream As Object
    Dim strMessageBody As String
    Dim strFrom As String
    Dim strTo As String
    Dim strCc As String
    Dim strSubject As String
    Dim strOutput As String
    Dim intCount As Integer
    Dim intTotal As Integer
    
    On Error GoTo ErrorHandler
    
    ' Initialize Outlook
    Set objOutlook = Application
    Set objNamespace = objOutlook.GetNamespace("MAPI")
    
    ' Try to get the shared/group mailbox folder
    ' First, try to find the ai-edih-archivum group in the folder list
    Set objFolder = GetGroupFolder(objNamespace, "ai-edih-archivum", "Beérkezett üzenetek")
    
    If objFolder Is Nothing Then
        MsgBox "Could not find the 'ai-edih-archivum' group folder or 'Beérkezett üzenetek' subfolder." & vbCrLf & vbCrLf & _
               "Please ensure:" & vbCrLf & _
               "1. The group is added to your Outlook" & vbCrLf & _
               "2. The folder name is correct" & vbCrLf & _
               "3. You have access to the group", vbExclamation, "Folder Not Found"
        Exit Sub
    End If
    
    ' Count total emails
    intTotal = objFolder.Items.Count
    
    If intTotal = 0 Then
        MsgBox "No emails found in the folder.", vbInformation
        Exit Sub
    End If
    
    ' Set output file path (Desktop)
    strFilePath = CreateObject("WScript.Shell").SpecialFolders("Desktop") & "\AI-EDIH-ARCHIVUM_Export_" & Format(Now, "yyyymmdd_hhnnss") & ".txt"
    
    ' Create ADODB.Stream for UTF-8 encoding
    Set objStream = CreateObject("ADODB.Stream")
    objStream.Type = 2 ' adTypeText
    objStream.Charset = "UTF-8"
    objStream.Open
    
    ' Initialize counter
    intCount = 0
    
    ' Loop through all items in the folder
    For Each objItem In objFolder.Items
        ' Check if it's a mail item
        If TypeOf objItem Is Outlook.MailItem Then
            Set objMail = objItem
            intCount = intCount + 1
            
            ' Extract email fields
            strFrom = GetSafeString(objMail.SenderName) & " <" & GetSafeString(objMail.SenderEmailAddress) & ">"
            strTo = GetSafeString(objMail.To)
            strCc = GetSafeString(objMail.CC)
            strSubject = GetSafeString(objMail.Subject)
            
            ' Get message body (prefer plain text, fallback to HTML stripped)
            If Len(Trim(objMail.Body)) > 0 Then
                strMessageBody = objMail.Body
            Else
                ' If no plain text body, try to use HTML body
                strMessageBody = StripHTML(objMail.HTMLBody)
            End If
            
            ' Build output string
            strOutput = "---[New exported AI-EDIH-ARCHINUM email]---" & vbCrLf
            strOutput = strOutput & "From: " & strFrom & vbCrLf
            strOutput = strOutput & "To: " & strTo & vbCrLf
            If Len(strCc) > 0 Then
                strOutput = strOutput & "Cc: " & strCc & vbCrLf
            End If
            strOutput = strOutput & "Subject: " & strSubject & vbCrLf
            strOutput = strOutput & vbCrLf
            strOutput = strOutput & strMessageBody & vbCrLf
            strOutput = strOutput & vbCrLf
            
            ' Write to stream
            objStream.WriteText strOutput, 0
        End If
    Next objItem
    
    ' Save stream to file and close
    objStream.SaveToFile strFilePath, 2 ' adSaveCreateOverWrite
    objStream.Close
    Set objStream = Nothing
    
    ' Show completion message
    MsgBox "Export completed successfully!" & vbCrLf & vbCrLf & _
           "Total emails exported: " & intCount & vbCrLf & _
           "File saved to: " & strFilePath, vbInformation, "Export Complete"
    
    ' Clean up
    Set objMail = Nothing
    Set objFolder = Nothing
    Set objNamespace = Nothing
    Set objOutlook = Nothing
    
    Exit Sub
    
ErrorHandler:
    If Not objStream Is Nothing Then
        If objStream.State = 1 Then objStream.Close
        Set objStream = Nothing
    End If
    MsgBox "An error occurred: " & Err.Description & " (Error " & Err.Number & ")", vbCritical, "Error"
    
End Sub

' Function to find the group folder
Private Function GetGroupFolder(objNamespace As Outlook.NameSpace, strGroupName As String, strSubfolderName As String) As Outlook.MAPIFolder
    Dim objFolder As Outlook.MAPIFolder
    Dim objSubfolder As Outlook.MAPIFolder
    Dim objStore As Outlook.Store
    Dim objExplorer As Outlook.Explorer
    Dim objNavigationGroups As Outlook.NavigationGroups
    Dim objNavigationGroup As Outlook.NavigationGroup
    Dim objNavigationFolder As Outlook.NavigationFolder
    
    On Error Resume Next
    
    ' Try method 1: Look through Favorites (Kedvencek) in Navigation Pane
    Set objExplorer = Application.ActiveExplorer
    If Not objExplorer Is Nothing Then
        Dim objMailModule As Outlook.MailModule
        Set objMailModule = objExplorer.NavigationPane.Modules.GetNavigationModule(olModuleMail)
        
        If Not objMailModule Is Nothing Then
            Set objNavigationGroups = objMailModule.NavigationGroups
            
            ' Look through all navigation groups (including Favorites/Kedvencek)
            For Each objNavigationGroup In objNavigationGroups
                For Each objNavigationFolder In objNavigationGroup.NavigationFolders
                    Set objFolder = objNavigationFolder.Folder
                    
                    ' Check if this is the group we're looking for
                    If LCase(objFolder.Name) = LCase(strGroupName) Or _
                       LCase(objFolder.Name) = LCase(strSubfolderName) Then
                        ' If it's the subfolder directly, use it
                        If LCase(objFolder.Name) = LCase(strSubfolderName) Then
                            Set GetGroupFolder = objFolder
                            Exit Function
                        End If
                        
                        ' If it's the group, look for subfolder
                        For Each objSubfolder In objFolder.Folders
                            If LCase(objSubfolder.Name) = LCase(strSubfolderName) Then
                                Set GetGroupFolder = objSubfolder
                                Exit Function
                            End If
                        Next objSubfolder
                        
                        ' If subfolder not found, use the main folder
                        Set GetGroupFolder = objFolder
                        Exit Function
                    End If
                    
                    ' Also check parent folder if current folder matches group name
                    If Not objFolder.Parent Is Nothing Then
                        If TypeOf objFolder.Parent Is Outlook.MAPIFolder Then
                            Dim objParentFolder As Outlook.MAPIFolder
                            Set objParentFolder = objFolder.Parent
                            If LCase(objParentFolder.Name) = LCase(strGroupName) Then
                                If LCase(objFolder.Name) = LCase(strSubfolderName) Then
                                    Set GetGroupFolder = objFolder
                                    Exit Function
                                End If
                            End If
                        End If
                    End If
                Next objNavigationFolder
            Next objNavigationGroup
        End If
    End If
    
    ' Try method 2: Look through all folders in namespace
    For Each objFolder In objNamespace.Folders
        If LCase(objFolder.Name) = LCase(strGroupName) Then
            ' Found the group, now look for the subfolder
            For Each objSubfolder In objFolder.Folders
                If LCase(objSubfolder.Name) = LCase(strSubfolderName) Then
                    Set GetGroupFolder = objSubfolder
                    Exit Function
                End If
            Next objSubfolder
            
            ' If subfolder not found, try using the main folder
            Set GetGroupFolder = objFolder
            Exit Function
        End If
    Next objFolder
    
    ' Try method 3: Look through stores (for Office 365 groups)
    For Each objStore In objNamespace.Stores
        If LCase(objStore.DisplayName) = LCase(strGroupName) Then
            Set objFolder = objStore.GetRootFolder
            For Each objSubfolder In objFolder.Folders
                If LCase(objSubfolder.Name) = LCase(strSubfolderName) Then
                    Set GetGroupFolder = objSubfolder
                    Exit Function
                End If
            Next objSubfolder
        End If
    Next objStore
    
    Set GetGroupFolder = Nothing
End Function

' Function to safely get string values (handle null/empty)
Private Function GetSafeString(varValue As Variant) As String
    If IsNull(varValue) Then
        GetSafeString = ""
    ElseIf IsEmpty(varValue) Then
        GetSafeString = ""
    Else
        GetSafeString = CStr(varValue)
    End If
End Function

' Function to strip HTML tags from text
Private Function StripHTML(strHTML As String) As String
    Dim objRegex As Object
    Dim strText As String
    
    On Error Resume Next
    
    strText = strHTML
    
    ' Create RegEx object
    Set objRegex = CreateObject("VBScript.RegExp")
    
    With objRegex
        .Global = True
        .IgnoreCase = True
        .MultiLine = True
        
        ' Remove script and style tags with their content
        .Pattern = "<(script|style)[^>]*>.*?</(script|style)>"
        strText = .Replace(strText, "")
        
        ' Remove HTML tags
        .Pattern = "<[^>]+>"
        strText = .Replace(strText, "")
        
        ' Replace common HTML entities
        strText = Replace(strText, "&nbsp;", " ")
        strText = Replace(strText, "&amp;", "&")
        strText = Replace(strText, "&lt;", "<")
        strText = Replace(strText, "&gt;", ">")
        strText = Replace(strText, "&quot;", """")
        strText = Replace(strText, "&#39;", "'")
        strText = Replace(strText, "&apos;", "'")
        
        ' Replace multiple spaces with single space
        .Pattern = " {2,}"
        strText = .Replace(strText, " ")
    End With
    
    Set objRegex = Nothing
    
    StripHTML = Trim(strText)
End Function
