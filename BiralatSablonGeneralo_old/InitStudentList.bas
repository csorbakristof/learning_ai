Attribute VB_Name = "InitStudentList"
Option Explicit

' INITLIST macro - Initialize Student List
' This macro creates a StudentData worksheet and imports student data from an external Excel file
' Shortcut: Ctrl+Shift+I

Sub InitStudentList()
    On Error GoTo ErrorHandler
    
    ' Declare variables
    Dim sourceWorkbook As Workbook
    Dim sourceWorksheet As Worksheet
    Dim targetWorksheet As Worksheet
    Dim targetWorkbook As Workbook
    Dim filePath As String
    Dim fileDialog As FileDialog
    Dim lastRow As Long
    Dim i As Long
    Dim headerRow As Long
    Dim targyCol As Long, targyNeptCol As Long, hallgatoNeveCol As Long, hallgatoNeptCol As Long
    Dim temaCimeCol As Long
    Dim foundSheet As Boolean
    
    ' Set the current workbook as target
    Set targetWorkbook = ThisWorkbook
    
    ' Create or clear the StudentData worksheet
    On Error Resume Next
    Set targetWorksheet = targetWorkbook.Worksheets("StudentData")
    On Error GoTo ErrorHandler
    
    If targetWorksheet Is Nothing Then
        ' Create new worksheet
        Set targetWorksheet = targetWorkbook.Worksheets.Add
        targetWorksheet.Name = "StudentData"
    Else
        ' Clear existing content
        targetWorksheet.Cells.Clear
    End If
    
    ' Open file dialog to select source Excel file
    Set fileDialog = Application.FileDialog(msoFileDialogFilePicker)
    With fileDialog
        .Title = "Válassza ki a hallgatói adatokat tartalmazó Excel fájlt"
        .Filters.Clear
        .Filters.Add "Excel Files", "*.xlsx;*.xls;*.xlsm"
        .AllowMultiSelect = False
        .InitialFileName = targetWorkbook.Path
        
        If .Show = -1 Then
            filePath = .SelectedItems(1)
        Else
            MsgBox "Nem választott ki fájlt. A művelet megszakítva.", vbInformation
            Exit Sub
        End If
    End With
    
    ' Open the source workbook
    Application.ScreenUpdating = False
    Set sourceWorkbook = Workbooks.Open(filePath, ReadOnly:=True)
    
    ' Find the worksheet containing "konzultáció" in its title
    foundSheet = False
    For Each sourceWorksheet In sourceWorkbook.Worksheets
        If InStr(LCase(sourceWorksheet.Name), "konzultáció") > 0 Then
            foundSheet = True
            Exit For
        End If
    Next sourceWorksheet
    
    ' If not found, try the second worksheet
    If Not foundSheet Then
        If sourceWorkbook.Worksheets.Count >= 2 Then
            Set sourceWorksheet = sourceWorkbook.Worksheets(2)
            foundSheet = True
        End If
    End If
    
    If Not foundSheet Then
        MsgBox "Nem található 'konzultáció' szöveget tartalmazó munkalap, és nincs második munkalap sem.", vbCritical
        sourceWorkbook.Close False
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    ' Find the header row and column positions
    headerRow = 0
    For i = 1 To 10 ' Search in first 10 rows for headers
        If sourceWorksheet.Cells(i, 1).Value <> "" Then
            ' Check if this row contains our headers
            Dim j As Long
            For j = 1 To 20 ' Search in first 20 columns
                Select Case LCase(Trim(sourceWorksheet.Cells(i, j).Value))
                    Case "tárgy"
                        targyCol = j
                        headerRow = i
                    Case "tárgy nept"
                        targyNeptCol = j
                        headerRow = i
                    Case "hallgató neve"
                        hallgatoNeveCol = j
                        headerRow = i
                    Case "hallg. nept"
                        hallgatoNeptCol = j
                        headerRow = i
                    Case "téma címe"
                        temaCimeCol = j
                        headerRow = i
                End Select
            Next j
            
            ' If we found at least the required columns, break
            If targyCol > 0 And hallgatoNeveCol > 0 And hallgatoNeptCol > 0 Then
                Exit For
            End If
        End If
    Next i
    
    ' Validate that required columns were found
    If targyCol = 0 Or hallgatoNeveCol = 0 Or hallgatoNeptCol = 0 Then
        MsgBox "Nem találhatóak a szükséges oszlopfejlécek (Tárgy, Hallgató neve, Hallg. nept).", vbCritical
        sourceWorkbook.Close False
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    ' Set up target worksheet headers
    With targetWorksheet
        .Cells(1, 1).Value = "Tárgy"
        .Cells(1, 2).Value = "Tárgy nept"
        .Cells(1, 3).Value = "Hallgató neve"
        .Cells(1, 4).Value = "Hallg. nept"
        .Cells(1, 5).Value = "Téma címe"
        .Cells(1, 6).Value = "Kiválasztva"
        
        ' Format headers
        .Range("A1:F1").Font.Bold = True
        .Range("A1:F1").Interior.Color = RGB(220, 220, 220)
    End With
    
    ' Find last row with data in source worksheet
    lastRow = sourceWorksheet.Cells(sourceWorksheet.Rows.Count, targyCol).End(xlUp).Row
    
    ' Copy data from source to target
    Dim targetRow As Long
    targetRow = 2
    
    For i = headerRow + 1 To lastRow
        ' Skip empty rows
        If Trim(sourceWorksheet.Cells(i, hallgatoNeveCol).Value) <> "" Then
            targetWorksheet.Cells(targetRow, 1).Value = sourceWorksheet.Cells(i, targyCol).Value
            
            If targyNeptCol > 0 Then
                targetWorksheet.Cells(targetRow, 2).Value = sourceWorksheet.Cells(i, targyNeptCol).Value
            End If
            
            targetWorksheet.Cells(targetRow, 3).Value = sourceWorksheet.Cells(i, hallgatoNeveCol).Value
            targetWorksheet.Cells(targetRow, 4).Value = sourceWorksheet.Cells(i, hallgatoNeptCol).Value
            
            If temaCimeCol > 0 Then
                targetWorksheet.Cells(targetRow, 5).Value = sourceWorksheet.Cells(i, temaCimeCol).Value
            End If
            
            ' Leave "Kiválasztva" column empty for user input
            targetWorksheet.Cells(targetRow, 6).Value = ""
            
            targetRow = targetRow + 1
        End If
    Next i
    
    ' Auto-fit columns
    targetWorksheet.Columns("A:F").AutoFit
    
    ' Close source workbook
    sourceWorkbook.Close False
    
    ' Activate the StudentData worksheet
    targetWorksheet.Activate
    targetWorksheet.Cells(1, 1).Select
    
    Application.ScreenUpdating = True
    
    MsgBox "Hallgatói adatok sikeresen importálva! " & (targetRow - 2) & " hallgató került be a listába.", vbInformation
    
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    If Not sourceWorkbook Is Nothing Then
        sourceWorkbook.Close False
    End If
    MsgBox "Hiba történt a makró végrehajtása során: " & Err.Description, vbCritical
End Sub

' Keyboard shortcut assignment
' This should be called when the workbook opens to assign Ctrl+Shift+I
Sub AssignKeyboardShortcut()
    Application.OnKey "^+I", "InitStudentList"
End Sub

' Remove keyboard shortcut
Sub RemoveKeyboardShortcut()
    Application.OnKey "^+I"
End Sub
