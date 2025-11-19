' ==============================================================================
' AUT Kiírás És Bírálati Sablon Generáló
' ==============================================================================
Option Explicit

' ==============================================================================
' Workbook Event Handlers - Register Hotkeys
' ==============================================================================
' NOTE: This code should be placed in ThisWorkbook module:
'
' Private Sub Workbook_Open()
'     Application.OnKey "^+C", "CollectStudents"
'     Application.OnKey "^+G", "GenerateDocuments"
' End Sub

' ==============================================================================
' [CollectStudents] Main Entry Point
' ==============================================================================
Public Sub CollectStudents()
    On Error GoTo ErrorHandler
    
    ' Clear the target worksheet
    Call ClearGeneraltHallgatoiLista
    
    ' [CollectTerhelesExportData] - Collect data from Terhelés export
    Call CollectTerhelesExportData
    
    ' [CollectZvSegedData] - Collect additional information from ZV segéd export
    Call CollectZvSegedData
    
    ' [CleanUpList] - Remove invalid rows
    Call CleanUpList
    
    MsgBox "A hallgatói lista sikeresen létrehozva!", vbInformation, "Kész"
    Exit Sub
    
ErrorHandler:
    MsgBox "Hiba történt a hallgatói lista létrehozása során:" & vbCrLf & vbCrLf & _
           "Hiba: " & Err.Description & vbCrLf & _
           "Hibakód: " & Err.Number, vbCritical, "Hiba"
End Sub

' ==============================================================================
' [CollectTerhelesExportData] Collect data from Terhelés export
' ==============================================================================
Private Sub CollectTerhelesExportData()
    Dim terhelesFile As String
    Dim terhelesWb As Workbook
    Dim konzultacioWs As Worksheet
    Dim targetWs As Worksheet
    Dim sourceRow As Long, targetRow As Long
    Dim lastRow As Long
    Dim konzulensValue As String
    Dim bracketPos As Long
    
    On Error GoTo ErrorHandler
    
    ' Find the Terhelés file in the same directory
    terhelesFile = FindFileStartingWith(ThisWorkbook.Path, "Terhelés")
    If terhelesFile = "" Then
        Err.Raise vbObjectError + 1, , "Nem található 'Terhelés' kezdetű Excel fájl a munkakönyvvel azonos könyvtárban."
    End If
    
    ' Open the Terhelés workbook
    Set terhelesWb = Workbooks.Open(terhelesFile, ReadOnly:=True)
    
    ' Find the worksheet containing "konzultáció"
    Set konzultacioWs = FindWorksheetContaining(terhelesWb, "konzultáció")
    If konzultacioWs Is Nothing Then
        terhelesWb.Close False
        Err.Raise vbObjectError + 2, , "Nem található 'konzultáció' szöveget tartalmazó munkalap a Terhelés fájlban."
    End If
    
    ' Get target worksheet
    Set targetWs = ThisWorkbook.Worksheets("GeneráltHallgatóiLista")
    
    ' Find last row in source
    lastRow = konzultacioWs.Cells(konzultacioWs.Rows.Count, "A").End(xlUp).Row
    
    ' Copy data row by row (starting from row 2, assuming row 1 is header)
    targetRow = 2
    For sourceRow = 2 To lastRow
        ' Hallgató neve
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Hallgató neve")).Value = _
            konzultacioWs.Cells(sourceRow, GetColumnNumber(konzultacioWs, "Hallgató neve")).Value
        
        ' Neptun kód
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Neptun kód")).Value = _
            konzultacioWs.Cells(sourceRow, GetColumnNumber(konzultacioWs, "Hallg. nept")).Value
        
        ' Tárgykód
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Tárgykód")).Value = _
            konzultacioWs.Cells(sourceRow, GetColumnNumber(konzultacioWs, "Tárgy nept")).Value
        
        ' Dolgozat megnevezése - using formula
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Dolgozat megnevezése")).Formula = _
            "=IFERROR(VLOOKUP($C" & targetRow & ",'Tantárgyi adatok'!B:F,2,FALSE),""nincs"")"
        
        ' Szak megnevezése - using formula (index 3 to get column D)
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Szak megnevezése")).Formula = _
            "=IFERROR(VLOOKUP($C" & targetRow & ",'Tantárgyi adatok'!B:F,3,FALSE),""nincs"")"
        
        ' Konzulens neve - remove text in brackets
        konzulensValue = CStr(konzultacioWs.Cells(sourceRow, GetColumnNumber(konzultacioWs, "Konzulens")).Value)
        bracketPos = InStr(konzulensValue, "(")
        If bracketPos > 0 Then
            konzulensValue = Trim(Left(konzulensValue, bracketPos - 1))
        End If
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Konzulens neve")).Value = konzulensValue
        
        ' Degree level - using formula (index 4 to get column E)
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Degree level")).Formula = _
            "=IFERROR(VLOOKUP($C" & targetRow & ",'Tantárgyi adatok'!B:F,4,FALSE),""nincs"")"
        
        ' Program name - using formula (index 5 to get column F)
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Program name")).Formula = _
            "=IFERROR(VLOOKUP($C" & targetRow & ",'Tantárgyi adatok'!B:F,5,FALSE),""nincs"")"
        
        targetRow = targetRow + 1
    Next sourceRow
    
    ' Close the Terhelés workbook
    terhelesWb.Close False
    
    Exit Sub
    
ErrorHandler:
    If Not terhelesWb Is Nothing Then
        terhelesWb.Close False
    End If
    Err.Raise Err.Number, Err.Source, Err.Description
End Sub

' ==============================================================================
' [CollectZvSegedData] Collect additional information from ZV segéd export
' ==============================================================================
Private Sub CollectZvSegedData()
    Dim zvFile As String
    Dim zvWb As Workbook
    Dim zvWs As Worksheet
    Dim targetWs As Worksheet
    Dim targetRow As Long, zvRow As Long
    Dim lastTargetRow As Long, lastZvRow As Long
    Dim targetNeptun As String, zvNeptun As String
    Dim kulfoldiValue As String
    Dim neptunColTarget As Long, neptunColZv As Long
    Dim temaCimeCol As Long, temaAngolCol As Long, kulfoldiCol As Long
    Dim magyCimCol As Long, angolCimCol As Long, biralNyelvCol As Long
    
    On Error GoTo ErrorHandler
    
    ' Check if the reviewTemplates_reports.xlsx file exists
    zvFile = ThisWorkbook.Path & "\reviewTemplates_reports.xlsx"
    If Dir(zvFile) = "" Then
        Err.Raise vbObjectError + 3, , "A 'reviewTemplates_reports.xlsx' fájl nem található a munkakönyvvel azonos könyvtárban."
    End If
    
    ' Open the file
    Set zvWb = Workbooks.Open(zvFile, ReadOnly:=True)
    Set zvWs = zvWb.Worksheets(1)
    
    ' Get target worksheet
    Set targetWs = ThisWorkbook.Worksheets("GeneráltHallgatóiLista")
    
    ' Get column numbers
    neptunColTarget = GetColumnNumber(targetWs, "Neptun kód")
    magyCimCol = GetColumnNumber(targetWs, "Dolgozat címe magyarul")
    angolCimCol = GetColumnNumber(targetWs, "Dolgozat címe angolul")
    biralNyelvCol = GetColumnNumber(targetWs, "Bírálat nyelve")
    
    neptunColZv = GetColumnNumber(zvWs, "Hallgató Neptun")
    temaCimeCol = GetColumnNumber(zvWs, "Téma címe")
    temaAngolCol = GetColumnNumber(zvWs, "Téma angol címe")
    kulfoldiCol = GetColumnNumber(zvWs, "Külföldi")
    
    ' Find last rows
    lastTargetRow = targetWs.Cells(targetWs.Rows.Count, "A").End(xlUp).Row
    lastZvRow = zvWs.Cells(zvWs.Rows.Count, neptunColZv).End(xlUp).Row
    
    ' For each row in GeneráltHallgatóiLista, find matching row in ZV file
    For targetRow = 2 To lastTargetRow
        targetNeptun = Trim(CStr(targetWs.Cells(targetRow, neptunColTarget).Value))
        
        ' Search for matching Neptun kód in ZV file
        For zvRow = 2 To lastZvRow
            zvNeptun = Trim(CStr(zvWs.Cells(zvRow, neptunColZv).Value))
            
            If targetNeptun = zvNeptun Then
                ' Match found - copy values
                
                ' Dolgozat címe magyarul
                targetWs.Cells(targetRow, magyCimCol).Value = _
                    zvWs.Cells(zvRow, temaCimeCol).Value
                
                ' Dolgozat címe angolul
                targetWs.Cells(targetRow, angolCimCol).Value = _
                    zvWs.Cells(zvRow, temaAngolCol).Value
                
                ' Bírálat nyelve
                kulfoldiValue = CStr(zvWs.Cells(zvRow, kulfoldiCol).Value)
                If kulfoldiValue = "True" Then
                    targetWs.Cells(targetRow, biralNyelvCol).Value = "angol"
                Else
                    targetWs.Cells(targetRow, biralNyelvCol).Value = "magyar"
                End If
                
                Exit For ' Found match, no need to continue searching
            End If
        Next zvRow
    Next targetRow
    
    ' Collect students with missing "Terhelés" entry
    Call CollectStudentsWithoutAutPortalEntry(zvWs, targetWs, neptunColZv, lastZvRow)
    
    ' Close the ZV file
    zvWb.Close False
    
    Exit Sub
    
ErrorHandler:
    If Not zvWb Is Nothing Then
        zvWb.Close False
    End If
    Err.Raise Err.Number, Err.Source, Err.Description
End Sub

' ==============================================================================
' Collect students with missing "Terhelés" entry
' ==============================================================================
Private Sub CollectStudentsWithoutAutPortalEntry(zvWs As Worksheet, targetWs As Worksheet, neptunColZv As Long, lastZvRow As Long)
    Dim missingWs As Worksheet
    Dim zvRow As Long, targetRow As Long
    Dim zvNeptun As String, targetNeptun As String
    Dim found As Boolean
    Dim lastTargetRow As Long
    Dim missingRow As Long
    Dim studentNameCol As Long, advisorNameCol As Long
    
    On Error GoTo ErrorHandler
    
    ' Get or create the StudentsWithoutAutPortalEntry worksheet
    On Error Resume Next
    Set missingWs = ThisWorkbook.Worksheets("StudentsWithoutAutPortalEntry")
    On Error GoTo ErrorHandler
    
    If missingWs Is Nothing Then
        Set missingWs = ThisWorkbook.Worksheets.Add
        missingWs.Name = "StudentsWithoutAutPortalEntry"
    End If
    
    ' Clear the worksheet completely
    missingWs.Cells.ClearContents
    
    ' Create headers (always)
    missingWs.Cells(1, 1).Value = "Hallgató neve"
    missingWs.Cells(1, 2).Value = "Neptun kód"
    missingWs.Cells(1, 3).Value = "Konzulens neve"
    
    ' Get column numbers from ZV file
    studentNameCol = GetColumnNumber(zvWs, "Hallgató")
    advisorNameCol = GetColumnNumber(zvWs, "Témavezető")
    
    ' Find last row in target worksheet
    lastTargetRow = targetWs.Cells(targetWs.Rows.Count, "A").End(xlUp).Row
    
    ' Start writing from row 2 in missing students worksheet
    missingRow = 2
    
    ' For each student in ZV file, check if they exist in GeneráltHallgatóiLista
    For zvRow = 2 To lastZvRow
        zvNeptun = Trim(CStr(zvWs.Cells(zvRow, neptunColZv).Value))
        
        If zvNeptun <> "" Then
            ' Search for this Neptun code in GeneráltHallgatóiLista
            found = False
            For targetRow = 2 To lastTargetRow
                targetNeptun = Trim(CStr(targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Neptun kód")).Value))
                If targetNeptun = zvNeptun Then
                    found = True
                    Exit For
                End If
            Next targetRow
            
            ' If not found, add to missing students list
            If Not found Then
                missingWs.Cells(missingRow, 1).Value = zvWs.Cells(zvRow, studentNameCol).Value
                missingWs.Cells(missingRow, 2).Value = zvNeptun
                missingWs.Cells(missingRow, 3).Value = zvWs.Cells(zvRow, advisorNameCol).Value
                missingRow = missingRow + 1
            End If
        End If
    Next zvRow
    
    Exit Sub
    
ErrorHandler:
    Err.Raise Err.Number, Err.Source, Err.Description
End Sub

' ==============================================================================
' [CleanUpList] Remove invalid rows from the list
' ==============================================================================
Private Sub CleanUpList()
    Dim targetWs As Worksheet
    Dim currentRow As Long
    Dim lastRow As Long
    Dim dolgozatMegnevCol As Long
    Dim dolgozatCimMagyCol As Long
    Dim megnevValue As String
    Dim cimMagyValue As String
    Dim shouldDelete As Boolean
    
    On Error GoTo ErrorHandler
    
    ' Get target worksheet
    Set targetWs = ThisWorkbook.Worksheets("GeneráltHallgatóiLista")
    
    ' Get column numbers
    dolgozatMegnevCol = GetColumnNumber(targetWs, "Dolgozat megnevezése")
    dolgozatCimMagyCol = GetColumnNumber(targetWs, "Dolgozat címe magyarul")
    
    ' Find last row - use UsedRange to account for all columns
    If targetWs.UsedRange.Rows.Count > 0 Then
        lastRow = targetWs.UsedRange.Rows.Count + targetWs.UsedRange.Row - 1
    Else
        lastRow = 1 
    End If
    
    ' Loop through rows from bottom to top (to avoid issues when deleting rows)
    For currentRow = lastRow To 2 Step -1
        shouldDelete = False
        
        ' Check "Dolgozat megnevezése"
        megnevValue = Trim(CStr(targetWs.Cells(currentRow, dolgozatMegnevCol).Value))
        If megnevValue = "" Or megnevValue = "0" Or LCase(megnevValue) = "nincs" Then
            shouldDelete = True
        End If
        
        ' Check "Dolgozat címe magyarul"
        cimMagyValue = Trim(CStr(targetWs.Cells(currentRow, dolgozatCimMagyCol).Value))
        If cimMagyValue = "" Then
            shouldDelete = True
        End If
        
        ' Delete row if any condition is met
        If shouldDelete Then
            targetWs.Rows(currentRow).Delete
        End If
    Next currentRow
    
    Exit Sub
    
ErrorHandler:
    Err.Raise Err.Number, Err.Source, Err.Description
End Sub

' ==============================================================================
' Helper Functions
' ==============================================================================

' Clear the GeneráltHallgatóiLista worksheet (keeping header)
Private Sub ClearGeneraltHallgatoiLista()
    Dim ws As Worksheet
    
    On Error GoTo ErrorHandler
    
    Set ws = ThisWorkbook.Worksheets("GeneráltHallgatóiLista")
    
    If ws.Cells(ws.Rows.Count, "A").End(xlUp).Row > 1 Then
        ws.Rows("2:" & ws.Rows.Count).ClearContents
    End If
    
    Exit Sub
    
ErrorHandler:
    Err.Raise vbObjectError + 5, , "A 'GeneráltHallgatóiLista' munkalap nem található a munkakönyvben."
End Sub

' Find a file starting with a specific prefix in a directory
Private Function FindFileStartingWith(folderPath As String, prefix As String) As String
    Dim fileName As String
    
    fileName = Dir(folderPath & "\" & prefix & "*.xls*")
    If fileName <> "" Then
        FindFileStartingWith = folderPath & "\" & fileName
    Else
        FindFileStartingWith = ""
    End If
End Function

' Find a worksheet containing specific text in its name
Private Function FindWorksheetContaining(wb As Workbook, searchText As String) As Worksheet
    Dim ws As Worksheet
    
    For Each ws In wb.Worksheets
        If InStr(1, ws.Name, searchText, vbTextCompare) > 0 Then
            Set FindWorksheetContaining = ws
            Exit Function
        End If
    Next ws
    
    Set FindWorksheetContaining = Nothing
End Function

' Get column number by header name
Private Function GetColumnNumber(ws As Worksheet, headerName As String) As Long
    Dim col As Long
    Dim lastCol As Long
    
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    
    For col = 1 To lastCol
        If Trim(CStr(ws.Cells(1, col).Value)) = headerName Then
            GetColumnNumber = col
            Exit Function
        End If
    Next col
    
    ' If not found, raise error
    Err.Raise vbObjectError + 4, , "Nem található '" & headerName & "' nevű oszlop a(z) '" & ws.Name & "' munkalapon."
End Function

' Convert string to filesystem friendly format (PascalCase, no accents)
Private Function MakeFilesystemFriendly(inputStr As String) As String
    Dim result As String
    Dim i As Long
    Dim char As String
    Dim prevWasSpace As Boolean
    
    result = ""
    prevWasSpace = True
    
    ' Replace accented characters
    inputStr = Replace(inputStr, "á", "a")
    inputStr = Replace(inputStr, "Á", "A")
    inputStr = Replace(inputStr, "é", "e")
    inputStr = Replace(inputStr, "É", "E")
    inputStr = Replace(inputStr, "í", "i")
    inputStr = Replace(inputStr, "Í", "I")
    inputStr = Replace(inputStr, "ó", "o")
    inputStr = Replace(inputStr, "Ó", "O")
    inputStr = Replace(inputStr, "ö", "o")
    inputStr = Replace(inputStr, "Ö", "O")
    inputStr = Replace(inputStr, "ő", "o")
    inputStr = Replace(inputStr, "Ő", "O")
    inputStr = Replace(inputStr, "ú", "u")
    inputStr = Replace(inputStr, "Ú", "U")
    inputStr = Replace(inputStr, "ü", "u")
    inputStr = Replace(inputStr, "Ü", "U")
    inputStr = Replace(inputStr, "ű", "u")
    inputStr = Replace(inputStr, "Ű", "U")
    
    ' Build PascalCase string
    For i = 1 To Len(inputStr)
        char = Mid(inputStr, i, 1)
        
        If char = " " Or char = "-" Or char = "_" Then
            prevWasSpace = True
        Else
            If prevWasSpace Then
                result = result & UCase(char)
                prevWasSpace = False
            Else
                result = result & LCase(char)
            End If
        End If
    Next i
    
    MakeFilesystemFriendly = result
End Function

' ==============================================================================
' [GenerateDocuments] Main Entry Point
' ==============================================================================
Public Sub GenerateDocuments()
    Dim studentWs As Worksheet
    Dim templateWs As Worksheet
    Dim studentRow As Long, templateRow As Long
    Dim lastStudentRow As Long, lastTemplateRow As Long
    Dim studentName As String, advisorName As String
    Dim outputDir As String
    Dim templateFile As String, outputFile As String
    Dim reviewLanguage As String
    Dim templateColumn As String
    Dim wordApp As Object
    Dim processedCount As Long
    Dim errorOccurred As Boolean
    Dim errorMessage As String
    
    On Error GoTo ErrorHandler
    
    errorOccurred = False
    processedCount = 0
    
    ' Get worksheets
    Set studentWs = ThisWorkbook.Worksheets("GeneráltHallgatóiLista")
    Set templateWs = ThisWorkbook.Worksheets("TemplatesAndFiles")
    
    ' Find last rows
    lastStudentRow = studentWs.Cells(studentWs.Rows.Count, "A").End(xlUp).Row
    lastTemplateRow = templateWs.Cells(templateWs.Rows.Count, "A").End(xlUp).Row
    
    ' Start a new Word instance
    Set wordApp = CreateObject("Word.Application")
    wordApp.Visible = False
    
    ' Process each student
    For studentRow = 2 To lastStudentRow
        Application.StatusBar = "Dokumentumok generálása: " & (studentRow - 1) & "/" & (lastStudentRow - 1) & " hallgató..."
        
        ' Get student information
        studentName = CStr(studentWs.Cells(studentRow, GetColumnNumber(studentWs, "Hallgató neve")).Value)
        advisorName = CStr(studentWs.Cells(studentRow, GetColumnNumber(studentWs, "Konzulens neve")).Value)
        reviewLanguage = CStr(studentWs.Cells(studentRow, GetColumnNumber(studentWs, "Bírálat nyelve")).Value)
        
        ' Check if required fields are present
        If Trim(studentName) = "" Or Trim(advisorName) = "" Then
            errorMessage = "Hiba a(z) " & studentRow & ". sorban: Hiányzó hallgató vagy konzulens név."
            GoTo CleanupAndExit
        End If
        
        ' Create output directory structure: output/konzulensnev
        outputDir = ThisWorkbook.Path & "\output\" & MakeFilesystemFriendly(advisorName)
        
        ' Create "output" directory if it doesn't exist
        If Dir(ThisWorkbook.Path & "\output", vbDirectory) = "" Then
            MkDir ThisWorkbook.Path & "\output"
        End If
        
        ' Create advisor-specific subdirectory if it doesn't exist
        If Dir(outputDir, vbDirectory) = "" Then
            MkDir outputDir
        End If
        
        ' Process each template
        For templateRow = 2 To lastTemplateRow
            ' Check if this template should be generated (Kell? 0/1 column)
            If CStr(templateWs.Cells(templateRow, GetColumnNumber(templateWs, "Kell? 0/1")).Value) = "1" Then
                ' Determine which template to use
                If LCase(Trim(reviewLanguage)) = "angol" Then
                    templateColumn = "Angol sablon"
                Else
                    templateColumn = "Magyar sablon"
                End If
                
                templateFile = ThisWorkbook.Path & "\" & CStr(templateWs.Cells(templateRow, GetColumnNumber(templateWs, templateColumn)).Value)
                outputFile = outputDir & "\" & Replace(CStr(templateWs.Cells(templateRow, GetColumnNumber(templateWs, "Kimeneti fájl sablon")).Value), "name", MakeFilesystemFriendly(studentName))
                
                ' Check if template exists
                If Dir(templateFile) = "" Then
                    errorMessage = "A sablon fájl nem található: " & templateFile
                    GoTo CleanupAndExit
                End If
                
                ' Generate the document
                Call GenerateSingleDocument(wordApp, studentWs, studentRow, templateFile, outputFile)
                processedCount = processedCount + 1
            End If
        Next templateRow
    Next studentRow
    
CleanupAndExit:
    ' Close Word
    If Not wordApp Is Nothing Then
        wordApp.Quit
        Set wordApp = Nothing
    End If
    
    Application.StatusBar = False
    
    ' Show summary
    If errorMessage <> "" Then
        MsgBox "Hiba történt a dokumentumok generálása során:" & vbCrLf & vbCrLf & errorMessage & vbCrLf & vbCrLf & _
               "Sikeresen feldolgozott dokumentumok: " & processedCount, vbCritical, "Hiba"
    Else
        MsgBox "Dokumentumok generálása sikeresen befejezve!" & vbCrLf & vbCrLf & _
               "Feldolgozott dokumentumok: " & processedCount, vbInformation, "Kész"
    End If
    
    Exit Sub
    
ErrorHandler:
    Application.StatusBar = False
    If Not wordApp Is Nothing Then
        wordApp.Quit
        Set wordApp = Nothing
    End If
    MsgBox "Hiba történt a dokumentumok generálása során:" & vbCrLf & vbCrLf & _
           "Hiba: " & Err.Description & vbCrLf & _
           "Hibakód: " & Err.Number, vbCritical, "Hiba"
End Sub

' ==============================================================================
' Generate a Single Document
' ==============================================================================
Private Sub GenerateSingleDocument(wordApp As Object, studentWs As Worksheet, studentRow As Long, templateFile As String, outputFile As String)
    Dim wordDoc As Object
    Dim col As Long
    Dim headerName As String
    Dim cellValue As String
    Dim placeholder As String
    Dim placeholders As Object
    Dim findRange As Object
    Dim lastCol As Long
    
    On Error GoTo ErrorHandler
    
    ' Open template
    Set wordDoc = wordApp.Documents.Open(templateFile)
    
    ' Get last column in student worksheet
    lastCol = studentWs.Cells(1, studentWs.Columns.Count).End(xlToLeft).Column
    
    ' First pass: Check for required placeholders and collect them
    Set placeholders = CreateObject("Scripting.Dictionary")
    placeholders.CompareMode = 1 ' vbTextCompare (case-insensitive)
    
    For col = 1 To lastCol
        headerName = Trim(CStr(studentWs.Cells(1, col).Value))
        If headerName <> "" Then
            placeholder = "[" & headerName & "]"
            ' Check if this placeholder exists in the document (case-insensitive)
            With wordDoc.Content.Find
                .ClearFormatting
                .Text = placeholder
                .Forward = True
                .Wrap = 0 ' wdFindStop
                .Format = False
                .MatchCase = False
                .MatchWholeWord = False
                
                If .Execute Then
                    ' Placeholder found, check if value is present
                    cellValue = Trim(CStr(studentWs.Cells(studentRow, col).Value))
                    If cellValue = "" Then
                        wordDoc.Close False
                        Err.Raise vbObjectError + 6, , "Hiányzó érték a(z) '" & headerName & "' oszlopban a(z) " & studentRow & ". sorban."
                    End If
                    If Not placeholders.Exists(headerName) Then
                        placeholders.Add headerName, cellValue
                    End If
                End If
            End With
        End If
    Next col
    
    ' Check for placeholders in document that don't exist in worksheet
    Call CheckForUnknownPlaceholders(wordDoc, studentWs, templateFile)
    
    ' Second pass: Replace all placeholders (case-insensitive)
    For col = 1 To lastCol
        headerName = Trim(CStr(studentWs.Cells(1, col).Value))
        If headerName <> "" And placeholders.Exists(headerName) Then
            placeholder = "[" & headerName & "]"
            cellValue = placeholders(headerName)
            
            ' Replace all occurrences (case-insensitive)
            With wordDoc.Content.Find
                .ClearFormatting
                .Replacement.ClearFormatting
                .Text = placeholder
                .Replacement.Text = cellValue
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
        End If
    Next col
    
    ' Save and close the document
    wordDoc.SaveAs2 outputFile
    wordDoc.Close False
    Set wordDoc = Nothing
    
    Exit Sub
    
ErrorHandler:
    If Not wordDoc Is Nothing Then
        wordDoc.Close False
        Set wordDoc = Nothing
    End If
    Err.Raise Err.Number, Err.Source, Err.Description
End Sub

' ==============================================================================
' Check for placeholders in document that don't exist in worksheet
' ==============================================================================
Private Sub CheckForUnknownPlaceholders(wordDoc As Object, studentWs As Worksheet, templateFile As String)
    Dim docText As String
    Dim pos As Long
    Dim startPos As Long
    Dim endPos As Long
    Dim placeholderName As String
    Dim foundInWorksheet As Boolean
    Dim col As Long
    Dim lastCol As Long
    Dim headerName As String
    Dim unknownPlaceholders As String
    
    On Error GoTo ErrorHandler
    
    ' Get all text from document
    docText = wordDoc.Content.Text
    
    ' Get last column in student worksheet
    lastCol = studentWs.Cells(1, studentWs.Columns.Count).End(xlToLeft).Column
    
    ' Search for all [xxx] patterns
    pos = 1
    unknownPlaceholders = ""
    
    Do While pos <= Len(docText)
        startPos = InStr(pos, docText, "[")
        If startPos = 0 Then Exit Do
        
        endPos = InStr(startPos, docText, "]")
        If endPos = 0 Then Exit Do
        
        ' Extract placeholder name (without brackets)
        placeholderName = Mid(docText, startPos + 1, endPos - startPos - 1)
        
        ' Check if this placeholder name exists as a column in worksheet (case-insensitive)
        foundInWorksheet = False
        For col = 1 To lastCol
            headerName = Trim(CStr(studentWs.Cells(1, col).Value))
            If StrComp(headerName, placeholderName, vbTextCompare) = 0 Then
                foundInWorksheet = True
                Exit For
            End If
        Next col
        
        ' If not found, add to error list
        If Not foundInWorksheet Then
            If InStr(unknownPlaceholders, "[" & placeholderName & "]") = 0 Then
                If unknownPlaceholders <> "" Then unknownPlaceholders = unknownPlaceholders & ", "
                unknownPlaceholders = unknownPlaceholders & "[" & placeholderName & "]"
            End If
        End If
        
        pos = endPos + 1
    Loop
    
    ' If unknown placeholders found, raise error
    If unknownPlaceholders <> "" Then
        Err.Raise vbObjectError + 7, , "A következő helyőrzők a sablonban találhatók, de nem léteznek oszlopként a 'GeneráltHallgatóiLista' munkalapon: " & _
                  unknownPlaceholders & vbCrLf & vbCrLf & "Sablon fájl: " & templateFile
    End If
    
    Exit Sub
    
ErrorHandler:
    Err.Raise Err.Number, Err.Source, Err.Description
End Sub
