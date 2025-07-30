Option Explicit

' Data Collector Macro for Excel Merger
' Hotkey: Ctrl+Shift+C
' Collects data from first worksheets in all Excel files in current directory
' and merges them into the currently active worksheet
' Headers must match across all files

Sub CollectData()
    On Error GoTo ErrorHandler
    
    Dim currentWorkbook As Workbook
    Dim targetWorksheet As Worksheet
    Dim sourceWorkbook As Workbook
    Dim sourceWorksheet As Worksheet
    Dim currentDir As String
    Dim fileName As String
    Dim nextRow As Long
    Dim sourceLastRow As Long
    Dim sourceLastCol As Long
    Dim i As Long
    Dim j As Long
    Dim filesProcessed As Integer
    Dim referenceHeaders As Variant
    Dim currentHeaders As Variant
    Dim headersSet As Boolean
    
    ' Get current workbook and directory
    Set currentWorkbook = ThisWorkbook
    currentDir = currentWorkbook.Path & "\"
    
    ' Get current workbook filename to avoid processing it
    Dim currentFileName As String
    currentFileName = currentWorkbook.Name
    
    ' Use the currently active worksheet as target
    Set targetWorksheet = currentWorkbook.ActiveSheet
    
    ' Completely clear the worksheet
    targetWorksheet.Cells.Clear
    
    ' Initialize variables
    nextRow = 1
    headersSet = False
    filesProcessed = 0
    
    ' Loop through all Excel files in current directory
    fileName = Dir(currentDir & "*.xls*")
    
    Do While fileName <> ""
        ' Skip temporary files and current file to avoid processing the file the macro is running from
        If Left(fileName, 1) <> "~" And fileName <> currentFileName Then
            
            Application.StatusBar = "Processing: " & fileName
            DoEvents
            
            ' Try to open the workbook
            On Error Resume Next
            Set sourceWorkbook = Workbooks.Open(currentDir & fileName, ReadOnly:=True, UpdateLinks:=False)
            On Error GoTo ErrorHandler
            
            If Not sourceWorkbook Is Nothing Then
                ' Get the first worksheet
                On Error Resume Next
                Set sourceWorksheet = sourceWorkbook.Worksheets(1)
                On Error GoTo ErrorHandler
                
                If Not sourceWorksheet Is Nothing Then
                    ' Find last row and column with data in source worksheet
                    sourceLastRow = sourceWorksheet.Cells(sourceWorksheet.Rows.Count, 1).End(xlUp).Row
                    sourceLastCol = sourceWorksheet.Cells(1, sourceWorksheet.Columns.Count).End(xlToLeft).Column
                    
                    ' Process data if there are any rows
                    If sourceLastRow >= 1 And sourceLastCol >= 1 Then
                        
                        ' Handle headers
                        If Not headersSet Then
                            ' This is the first file - copy headers and set reference
                            For j = 1 To sourceLastCol
                                targetWorksheet.Cells(1, j).Value = sourceWorksheet.Cells(1, j).Value
                            Next j
                            ' Add source file column header
                            targetWorksheet.Cells(1, sourceLastCol + 1).Value = "Forrás fájl"
                            
                            ' Store reference headers
                            ReDim referenceHeaders(1 To sourceLastCol)
                            For j = 1 To sourceLastCol
                                referenceHeaders(j) = CStr(sourceWorksheet.Cells(1, j).Value)
                            Next j
                            
                            ' Format headers
                            With targetWorksheet.Range(targetWorksheet.Cells(1, 1), targetWorksheet.Cells(1, sourceLastCol + 1))
                                .Font.Bold = True
                                .Interior.Color = RGB(200, 200, 200)
                            End With
                            
                            headersSet = True
                            nextRow = 2
                        Else
                            ' Check if headers match
                            Dim headersMatch As Boolean
                            headersMatch = True
                            
                            If sourceLastCol <> UBound(referenceHeaders) Then
                                headersMatch = False
                            Else
                                For j = 1 To sourceLastCol
                                    If CStr(sourceWorksheet.Cells(1, j).Value) <> referenceHeaders(j) Then
                                        headersMatch = False
                                        Exit For
                                    End If
                                Next j
                            End If
                            
                            If Not headersMatch Then
                                sourceWorkbook.Close SaveChanges:=False
                                MsgBox "Header mismatch in file: " & fileName & vbCrLf & _
                                       "Expected headers must match the first processed file.", vbCritical, "Header Error"
                                GoTo NextFile
                            End If
                        End If
                        
                        ' Copy data rows (skip header row)
                        If sourceLastRow > 1 Then
                            For i = 2 To sourceLastRow
                                ' Check if row has any data
                                Dim hasData As Boolean
                                hasData = False
                                For j = 1 To sourceLastCol
                                    If sourceWorksheet.Cells(i, j).Value <> "" Then
                                        hasData = True
                                        Exit For
                                    End If
                                Next j
                                
                                ' Copy row if it has data
                                If hasData Then
                                    For j = 1 To sourceLastCol
                                        targetWorksheet.Cells(nextRow, j).Value = sourceWorksheet.Cells(i, j).Value
                                    Next j
                                    ' Add source file name
                                    targetWorksheet.Cells(nextRow, sourceLastCol + 1).Value = fileName
                                    nextRow = nextRow + 1
                                End If
                            Next i
                        End If
                        
                        filesProcessed = filesProcessed + 1
                    End If
                End If
                
                ' Close source workbook without saving
                sourceWorkbook.Close SaveChanges:=False
                Set sourceWorkbook = Nothing
                Set sourceWorksheet = Nothing
            End If
        End If
        
NextFile:
        ' Get next file
        fileName = Dir()
    Loop
    
    ' Auto-fit columns
    If headersSet Then
        targetWorksheet.Columns.AutoFit
        
        ' Add borders to data
        If nextRow > 2 Then
            With targetWorksheet.Range(targetWorksheet.Cells(1, 1), targetWorksheet.Cells(nextRow - 1, UBound(referenceHeaders) + 1))
                .Borders.LineStyle = xlContinuous
                .Borders.Weight = xlThin
            End With
        End If
    End If
    
    ' Select the target worksheet
    targetWorksheet.Select
    targetWorksheet.Cells(1, 1).Select
    
    ' Clear status bar and show completion message
    Application.StatusBar = False
    MsgBox "Data collection completed!" & vbCrLf & _
           "Files processed: " & filesProcessed & vbCrLf & _
           "Records collected: " & (nextRow - 2) & vbCrLf & _
           "Target worksheet: " & targetWorksheet.Name, vbInformation, "Collection Complete"
    
    Exit Sub
    
ErrorHandler:
    Application.StatusBar = False
    
    ' Close any open workbook if error occurred
    If Not sourceWorkbook Is Nothing Then
        sourceWorkbook.Close SaveChanges:=False
    End If
    
    MsgBox "An error occurred during data collection: " & vbCrLf & Err.Description, vbCritical, "Error"
End Sub

' Keyboard shortcut assignment (Ctrl+Shift+C)
Sub Auto_Open()
    Application.OnKey "^+C", "CollectData"
End Sub

Sub Auto_Close()
    Application.OnKey "^+C" ' Remove the shortcut when workbook closes
End Sub
