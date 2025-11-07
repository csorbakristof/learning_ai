' GENDOCX macro - Template Generator
' This macro generates Word documents for selected students from the StudentData worksheet
' Shortcut: Ctrl+Shift+G

Sub TemplateGenerator()
    On Error GoTo ErrorHandler
    
    ' Declare variables
    Dim studentDataWS As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim studentName As String
    Dim targy As String
    Dim temaCime As String
    Dim kivalasztva As String
    Dim wordApp As Object
    Dim wordDoc As Object
    Dim templatePath As String
    Dim newDocPath As String
    Dim currentDate As String
    Dim szakdolgozatDiplomaterv As String
    Dim szak As String
    Dim processedCount As Long
    
    ' Check if StudentData worksheet exists
    On Error Resume Next
    Set studentDataWS = ThisWorkbook.Worksheets("StudentData")
    On Error GoTo ErrorHandler
    
    If studentDataWS Is Nothing Then
        MsgBox "A StudentData munkalap nem található. Először futtassa az InitStudentList makrót!", vbCritical
        Exit Sub
    End If
    
    ' Check if template file exists
    templatePath = ThisWorkbook.Path & "\ReviewAndGradeTemplate.docm"
    If Dir(templatePath) = "" Then
        MsgBox "A ReviewAndGradeTemplate.docm sablon nem található a következő helyen: " & templatePath, vbCritical
        Exit Sub
    End If
    
    ' Get current date in Hungarian format
    currentDate = Format(Date, "yyyy. mmmm d.")
    currentDate = Replace(currentDate, "January", "január")
    currentDate = Replace(currentDate, "February", "február")
    currentDate = Replace(currentDate, "March", "március")
    currentDate = Replace(currentDate, "April", "április")
    currentDate = Replace(currentDate, "May", "május")
    currentDate = Replace(currentDate, "June", "június")
    currentDate = Replace(currentDate, "July", "július")
    currentDate = Replace(currentDate, "August", "augusztus")
    currentDate = Replace(currentDate, "September", "szeptember")
    currentDate = Replace(currentDate, "October", "október")
    currentDate = Replace(currentDate, "November", "november")
    currentDate = Replace(currentDate, "December", "december")
    
    ' Create Word application
    Set wordApp = CreateObject("Word.Application")
    wordApp.Visible = True
    
    ' Find last row with data
    lastRow = studentDataWS.Cells(studentDataWS.Rows.Count, 3).End(xlUp).Row
    
    Application.ScreenUpdating = False
    processedCount = 0
    
    ' Process each row in StudentData
    For i = 2 To lastRow ' Start from row 2 (skip header)
        ' Check if student is selected (Kiválasztva column is not empty)
        kivalasztva = Trim(studentDataWS.Cells(i, 6).Value)
        
        If kivalasztva <> "" Then
            ' Get student data
            targy = Trim(studentDataWS.Cells(i, 1).Value)
            studentName = Trim(studentDataWS.Cells(i, 3).Value)
            temaCime = Trim(studentDataWS.Cells(i, 5).Value)
            
            ' Skip if essential data is missing
            If studentName = "" Or targy = "" Then
                MsgBox "Hiányzó adatok a(z) " & i & ". sorban. Kihagyva.", vbWarning
                GoTo NextStudent
            End If
            
            ' Determine SzakdolgozatDiplomaterv
            If InStr(LCase(targy), "szakdolgozat") > 0 Then
                szakdolgozatDiplomaterv = "Szakdolgozat"
            ElseIf InStr(LCase(targy), "diplomaterv") > 0 Then
                szakdolgozatDiplomaterv = "Diplomaterv"
            Else
                szakdolgozatDiplomaterv = "Szakdolgozat" ' Default value
            End If
            
            ' Determine Szak (major)
            If InStr(LCase(targy), "info") > 0 Then
                szak = "mérnökinformatikus"
            ElseIf InStr(LCase(targy), "vill") > 0 Then
                szak = "villamosmérnök"
            ElseIf InStr(LCase(targy), "mecha") > 0 Then
                szak = "mechatronikus mérnök"
            Else
                szak = "mérnökinformatikus" ' Default value
            End If
            
            ' Create new document path
            newDocPath = ThisWorkbook.Path & "\Review_" & CleanFileName(studentName) & ".docm"
            
            ' Copy template file
            If Dir(newDocPath) <> "" Then
                Kill newDocPath ' Delete if exists
            End If
            FileCopy templatePath, newDocPath
            
            ' Open the new document
            Set wordDoc = wordApp.Documents.Open(newDocPath)
            
            ' Replace placeholders
            Call ReplaceText(wordDoc, "<<SzakdolgozatDiplomaterv>>", szakdolgozatDiplomaterv)
            Call ReplaceText(wordDoc, "<<StudentName>>", studentName)
            Call ReplaceText(wordDoc, "<<Szak>>", szak)
            Call ReplaceText(wordDoc, "<<cím>>", temaCime)
            Call ReplaceText(wordDoc, "<<dátum>>", currentDate)
            
            ' Save and close the document
            wordDoc.Save
            wordDoc.Close
            
            processedCount = processedCount + 1
            
        End If
        
NextStudent:
    Next i
    
    ' Close Word application
    wordApp.Quit
    Set wordApp = Nothing
    Set wordDoc = Nothing
    
    Application.ScreenUpdating = True
    
    If processedCount > 0 Then
        MsgBox "Sikeresen létrehozva " & processedCount & " dokumentum.", vbInformation
    Else
        MsgBox "Nem található kiválasztott hallgató. Jelölje meg a hallgatókat a 'Kiválasztva' oszlopban!", vbWarning
    End If
    
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    If Not wordApp Is Nothing Then
        wordApp.Quit
    End If
    Set wordApp = Nothing
    Set wordDoc = Nothing
    MsgBox "Hiba történt a dokumentumok generálása során: " & Err.Description, vbCritical
End Sub

' Helper function to replace text in Word document
Private Sub ReplaceText(doc As Object, findText As String, replaceText As String)
    Dim findRange As Object
    Set findRange = doc.Content
    
    With findRange.Find
        .Text = findText
        .Replacement.Text = replaceText
        .Forward = True
        .Wrap = 1 ' wdFindContinue
        .Format = False
        .MatchCase = False
        .MatchWholeWord = False
        .MatchWildcards = False
        .MatchSoundsLike = False
        .MatchAllWordForms = False
        .Execute Replace:=2 ' wdReplaceAll
    End With
End Sub

' Helper function to clean filename from invalid characters
Private Function CleanFileName(fileName As String) As String
    Dim invalidChars As String
    Dim i As Integer
    Dim cleanName As String
    
    invalidChars = "\/:*?""<>|"
    cleanName = fileName
    
    For i = 1 To Len(invalidChars)
        cleanName = Replace(cleanName, Mid(invalidChars, i, 1), "_")
    Next i
    
    ' Also replace spaces with underscores for cleaner filenames
    cleanName = Replace(cleanName, " ", "_")
    
    CleanFileName = cleanName
End Function

' Keyboard shortcut assignment for GENDOCX
Sub AssignGenDocxShortcut()
    Application.OnKey "^+G", "TemplateGenerator"
End Sub

' Remove keyboard shortcut for GENDOCX
Sub RemoveGenDocxShortcut()
    Application.OnKey "^+G"
End Sub
