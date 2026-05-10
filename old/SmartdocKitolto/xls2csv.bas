' XLS2CSV Macro v2.1: Export all rows in the active worksheet to individual CSV files
' Each CSV file is named after the value in the selected "filename column" for each row
' Assumes the first row is the header
' 
' v2.0 Changes:
' - Uses UTF-8 encoding for proper Hungarian character support (á, é, í, ó, ő, ú, ű, ü)
' - ADODB.Stream replaces FileSystemObject for UTF-8 file writing
' - Compatible with csv2pdf.py encoding detection
'
' v2.1 Changes:
' - Automatic date formatting to YYYYMMDD format for SmartDoc compatibility
' - Supports SmartDoc date format requirements: n, nn, hnn, hhnn, éhhnn, ééhhnn, ééééhhnn, éééé-hh-nn, éééé.hh.nn, éééé. hh. nn

Option Explicit

' Helper function to format dates in YYYYMMDD format for SmartDoc compatibility
Function FormatDateForSmartDoc(cellValue As Variant) As String
    Dim dateValue As Date
    
    ' Check if the value is a date
    If IsDate(cellValue) Then
        dateValue = CDate(cellValue)
        ' Format as YYYYMMDD
        FormatDateForSmartDoc = Format(dateValue, "YYYYMMDD")
    Else
        ' If not a date, return the original value as string
        FormatDateForSmartDoc = CStr(cellValue)
    End If
End Function

Sub ExportRowsToCSV()
    Dim ws As Worksheet
    Dim lastRow As Long, lastCol As Long
    Dim header As String
    Dim i As Long, j As Long
    Dim filenameCol As Long
    Dim filename As String
    Dim csvContent As String
    Dim cell As Range
    Dim stream As Object
    
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
        header = header & """" & FormatDateForSmartDoc(ws.Cells(1, j).Value) & """"
        If j < lastCol Then header = header & ";"
    Next j
    
        ' Export each row
    For i = 2 To lastRow
        filename = ws.Cells(i, filenameCol).Value
        If filename = "" Then
            MsgBox "Filename missing in row " & i & ". Skipping.", vbExclamation
            GoTo NextRow
        End If
        csvContent = header & vbCrLf
        For j = 1 To lastCol
            csvContent = csvContent & """" & FormatDateForSmartDoc(ws.Cells(i, j).Value) & """"
            If j < lastCol Then csvContent = csvContent & ";"
        Next j
        
        ' Write to file using UTF-8 encoding
        Set stream = CreateObject("ADODB.Stream")
        stream.Type = 2 ' Text
        stream.Charset = "UTF-8"
        stream.Open
        stream.WriteText csvContent
        stream.SaveToFile ThisWorkbook.Path & "\" & filename & ".csv", 2 ' Overwrite existing
        stream.Close
        Set stream = Nothing
NextRow:
    Next i
    
    MsgBox "CSV files exported successfully.", vbInformation
End Sub

' Macro to register Ctrl+Shift+C as a hotkey for ExportRowsToCSV
Sub RegisterHotkey()
    Application.OnKey "^+C", "ExportRowsToCSV"
    MsgBox "Hotkey Ctrl+Shift+C registered for ExportRowsToCSV macro.", vbInformation
End Sub
