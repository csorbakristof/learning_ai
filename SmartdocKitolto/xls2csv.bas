' XLS2CSV Macro: Export all rows in the active worksheet to individual CSV files
' Each CSV file is named after the value in the selected "filename column" for each row
' Assumes the first row is the header

Option Explicit

Sub ExportRowsToCSV()
    Dim ws As Worksheet
    Dim lastRow As Long, lastCol As Long
    Dim header As String
    Dim i As Long, j As Long
    Dim filenameCol As Long
    Dim filename As String
    Dim csvContent As String
    Dim fso As Object, fileOut As Object
    Dim cell As Range
    
    Set ws = ActiveSheet
    ' Prompt user to select the filename column
    On Error Resume Next
    Set cell = Application.InputBox("Select the filename column (click a cell in the column)", Type:=8)
    On Error GoTo 0
    If cell Is Nothing Then
        MsgBox "No column selected. Operation cancelled.", vbExclamation
        Exit Sub
    End If
    filenameCol = cell.Column

    ' Use the filename column to determine the last row
    lastRow = ws.Cells(ws.Rows.Count, filenameCol).End(xlUp).Row
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    
    ' Get header
    For j = 1 To lastCol
        header = header & """" & ws.Cells(1, j).Value & """"
        If j < lastCol Then header = header & ";"
    Next j
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' Export each row
    For i = 2 To lastRow
        filename = ws.Cells(i, filenameCol).Value
        If filename = "" Then
            MsgBox "Filename missing in row " & i & ". Skipping.", vbExclamation
            GoTo NextRow
        End If
        csvContent = header & vbCrLf
        For j = 1 To lastCol
            csvContent = csvContent & """" & ws.Cells(i, j).Value & """"
            If j < lastCol Then csvContent = csvContent & ";"
        Next j
        
        ' Write to file
        Set fileOut = fso.CreateTextFile(ThisWorkbook.Path & "\" & filename & ".csv", True, False)
        fileOut.Write csvContent
        fileOut.Close
NextRow:
    Next i
    
    MsgBox "CSV files exported successfully.", vbInformation
End Sub

' Macro to register Ctrl+Shift+C as a hotkey for ExportRowsToCSV
Sub RegisterHotkey()
    Application.OnKey "^+C", "ExportRowsToCSV"
    MsgBox "Hotkey Ctrl+Shift+C registered for ExportRowsToCSV macro.", vbInformation
End Sub
