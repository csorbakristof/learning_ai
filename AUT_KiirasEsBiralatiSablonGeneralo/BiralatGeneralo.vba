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
            "=IFERROR(VLOOKUP($C" & targetRow & ",'Tantárgyi adatok'!B:D,2,FALSE),""nincs"")"
        
        ' Szak megnevezése - using formula (index 3 to get column D)
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Szak megnevezése")).Formula = _
            "=IFERROR(VLOOKUP($C" & targetRow & ",'Tantárgyi adatok'!B:D,3,FALSE),""nincs"")"
        
        ' Konzulens neve - remove text in brackets
        konzulensValue = CStr(konzultacioWs.Cells(sourceRow, GetColumnNumber(konzultacioWs, "Konzulens")).Value)
        bracketPos = InStr(konzulensValue, "(")
        If bracketPos > 0 Then
            konzulensValue = Trim(Left(konzulensValue, bracketPos - 1))
        End If
        targetWs.Cells(targetRow, GetColumnNumber(targetWs, "Konzulens neve")).Value = konzulensValue
        
        ' Konzulens beosztása - leave empty for now
        
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
    
    neptunColZv = GetColumnNumber(zvWs, "Neptun kód")
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
