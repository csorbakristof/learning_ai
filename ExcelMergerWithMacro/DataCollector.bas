Option Explicit

' Data Collector Macro for Excel Merger
' Hotkey: Ctrl+Shift+C
' Collects data from "Adatgyujto" worksheets in all Excel files in current directory
' and merges them into the "Gyujtes" worksheet

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
    Dim i As Long
    Dim filesProcessed As Integer
    
    ' Get current workbook and directory
    Set currentWorkbook = ThisWorkbook
    currentDir = currentWorkbook.Path & "\"
    
    ' Get current workbook filename to avoid processing it
    Dim currentFileName As String
    currentFileName = currentWorkbook.Name
    
    ' Check if "Gyujtes" worksheet exists, create if not
    On Error Resume Next
    Set targetWorksheet = currentWorkbook.Worksheets("Gyujtes")
    On Error GoTo ErrorHandler
    
    If targetWorksheet Is Nothing Then
        Set targetWorksheet = currentWorkbook.Worksheets.Add
        targetWorksheet.Name = "Gyujtes"
        ' Add headers
        targetWorksheet.Cells(1, 1).Value = "Név"
        targetWorksheet.Cells(1, 2).Value = "Választott szám"
        targetWorksheet.Cells(1, 3).Value = "Forrás fájl" ' Source file column
        
        ' Format headers
        With targetWorksheet.Range("A1:C1")
            .Font.Bold = True
            .Interior.Color = RGB(200, 200, 200)
        End With
    End If
    
    ' Clear existing data (keep headers)
    If targetWorksheet.Cells(2, 1).Value <> "" Then
        targetWorksheet.Range("A2:C" & targetWorksheet.Cells(targetWorksheet.Rows.Count, 1).End(xlUp).Row).Clear
    End If
    
    ' Find next available row in target worksheet
    nextRow = 2 ' Start from row 2 (after headers)
    
    ' Initialize counter
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
                ' Check if "Adatgyujto" worksheet exists
                On Error Resume Next
                Set sourceWorksheet = sourceWorkbook.Worksheets("Adatgyujto")
                On Error GoTo ErrorHandler
                
                If Not sourceWorksheet Is Nothing Then
                    ' Find last row with data in source worksheet
                    sourceLastRow = sourceWorksheet.Cells(sourceWorksheet.Rows.Count, 1).End(xlUp).Row
                    
                    ' Copy data if there are rows beyond the header
                    If sourceLastRow > 1 Then
                        For i = 2 To sourceLastRow
                            ' Only copy rows that have data in both columns
                            If sourceWorksheet.Cells(i, 1).Value <> "" And sourceWorksheet.Cells(i, 2).Value <> "" Then
                                targetWorksheet.Cells(nextRow, 1).Value = sourceWorksheet.Cells(i, 1).Value ' Name
                                targetWorksheet.Cells(nextRow, 2).Value = sourceWorksheet.Cells(i, 2).Value ' Number
                                targetWorksheet.Cells(nextRow, 3).Value = fileName ' Source file
                                nextRow = nextRow + 1
                            End If
                        Next i
                        filesProcessed = filesProcessed + 1
                    End If
                End If
                
                ' Close source workbook without saving
                sourceWorkbook.Close SaveChanges:=False
                Set sourceWorkbook = Nothing
                Set sourceWorksheet = Nothing
            End If
        End If
        
        ' Get next file
        fileName = Dir()
    Loop
    
    ' Auto-fit columns
    targetWorksheet.Columns("A:C").AutoFit
    
    ' Add borders to data
    If nextRow > 2 Then
        With targetWorksheet.Range("A1:C" & (nextRow - 1))
            .Borders.LineStyle = xlContinuous
            .Borders.Weight = xlThin
        End With
    End If
    
    ' Select the target worksheet
    targetWorksheet.Select
    targetWorksheet.Cells(1, 1).Select
    
    ' Clear status bar and show completion message
    Application.StatusBar = False
    MsgBox "Data collection completed!" & vbCrLf & _
           "Files processed: " & filesProcessed & vbCrLf & _
           "Records collected: " & (nextRow - 2), vbInformation, "Collection Complete"
    
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
