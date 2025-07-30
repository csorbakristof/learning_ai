' =============================================================================
' HOTKEY SETUP MACROS
' =============================================================================

Sub SetupHotkey()
    ' This macro sets up the Ctrl+Shift+G hotkey
    ' Call this once to enable the hotkey functionality
    Application.OnKey "^+G", "GenerateDocumentFromCurrentCell"
    MsgBox "Hotkey Ctrl+Shift+G has been set up!" & vbCrLf & "Press Ctrl+Shift+G on any cell in columns E-F to generate a document."
End Sub

Sub RemoveHotkey()
    ' This macro removes the Ctrl+Shift+G hotkey
    Application.OnKey "^+G"
    MsgBox "Hotkey Ctrl+Shift+G has been removed."
End Sub

' =============================================================================
' MAIN HOTKEY FUNCTIONALITY
' =============================================================================

Sub GenerateDocumentFromCurrentCell()
    Dim currentCell As Range
    Dim ws As Worksheet
    Dim currentRow As Long
    Dim currentCol As Long
    Dim templateName As String
    Dim personName As String
    Dim outputFileName As String
    Dim templatePath As String
    Dim savePath As String
    Dim wordApp As Object
    Dim wordDoc As Object
    Dim headerRow As Long
    Dim i As Long
    Dim placeholderText As String
    Dim replacementValue As String
    Dim columnHeader As String
    
    ' Get current selection
    Set currentCell = ActiveCell
    Set ws = ActiveSheet
    currentRow = currentCell.Row
    currentCol = currentCell.Column
    headerRow = 1
    
    ' Check if we're in the correct worksheet
    If ws.Name <> "Data" Then
        MsgBox "Please use this hotkey only in the 'Data' worksheet."
        Exit Sub
    End If
    
    ' Check if we're in columns E or F (template columns)
    If currentCol < 5 Then ' Column E is 5, F is 6
        MsgBox "Please press Ctrl+Shift+G in columns E or F where templates are defined."
        Exit Sub
    End If
    
    ' Check if we're not in the header row
    If currentRow = headerRow Then
        MsgBox "Cannot generate document from header row. Please select a data row."
        Exit Sub
    End If
    
    ' Get template name from header row of current column
    templateName = ws.Cells(headerRow, currentCol).Value
    If templateName = "" Then
        MsgBox "No template defined in column " & Split(Cells(1, currentCol).Address, "$")(1) & ". Please add a template filename in row 1."
        Exit Sub
    End If
    
    ' Get person name from column A (Név column)
    personName = ws.Cells(currentRow, 1).Value ' Column A
    If personName = "" Then
        MsgBox "No name found in column A for row " & currentRow
        Exit Sub
    End If
    
    ' Set up paths
    templatePath = "e:\_learning_ai\Excel2DocWithTemplate\" & templateName
    savePath = "e:\_learning_ai\Excel2DocWithTemplate\output\"
    outputFileName = personName & "_" & Left(templateName, InStrRev(templateName, ".") - 1) & ".docx"
    
    ' Check if template file exists
    If Dir(templatePath) = "" Then
        MsgBox "Template file not found: " & templatePath
        Exit Sub
    End If
    
    ' Create Word instance
    On Error GoTo ErrorHandler
    Set wordApp = CreateObject("Word.Application")
    wordApp.Visible = False
    
    ' Open template
    Set wordDoc = wordApp.Documents.Open(templatePath)
    
    ' Replace all placeholders with data from current row
    ' Loop through all columns that have headers
    For i = 1 To 3 ' Assuming max 3 columns (A to C)
        columnHeader = ws.Cells(headerRow, i).Value
        If columnHeader <> "" Then
            placeholderText = "<<" & columnHeader & ">>"
            replacementValue = ws.Cells(currentRow, i).Text ' Use .Text to preserve formatting
            
            ' Replace in document
            With wordDoc.Content.Find
                .Execute FindText:=placeholderText, ReplaceWith:=replacementValue, Replace:=2
            End With
        End If
    Next i
    
    ' Save as Word document
    wordDoc.SaveAs2 savePath & outputFileName
    
    ' Export as PDF
    wordDoc.ExportAsFixedFormat OutputFileName:=savePath & Left(outputFileName, InStrRev(outputFileName, ".") - 1) & ".pdf", ExportFormat:=17
    
    ' Clean up
    wordDoc.Close SaveChanges:=False
    wordApp.Quit
    Set wordApp = Nothing
    
    MsgBox "Document generated successfully!" & vbCrLf & "File: " & outputFileName
    Exit Sub
    
ErrorHandler:
    ' Clean up in case of error
    If Not wordDoc Is Nothing Then wordDoc.Close SaveChanges:=False
    If Not wordApp Is Nothing Then wordApp.Quit
    Set wordApp = Nothing
    MsgBox "Error generating document: " & Err.Description
End Sub

' =============================================================================
' ORIGINAL BULK GENERATION MACRO (PRESERVED)
' =============================================================================

Sub GenerateWordDocs()
    Dim wordApp As Object
    Dim wordDoc As Object
    Dim templatePath As String
    Dim savePath As String
    Dim lastRow As Long
    Dim i As Long
    Dim name As String, dateValue As String
    
    ' Adjust paths here
    templatePath = "e:\_learning_ai\Excel2DocWithTemplate\DocTemplate.docx"
    savePath = "e:\_learning_ai\Excel2DocWithTemplate\output\"

    ' Create Word instance
    Set wordApp = CreateObject("Word.Application")
    wordApp.Visible = False

    With ThisWorkbook.Sheets("Data")
        lastRow = .Cells(.Rows.Count, "A").End(xlUp).Row

        For i = 2 To lastRow
            name = .Cells(i, 1).Value
            Message = .Cells(i, 2).Text  ' Keep as text to preserve format

            Set wordDoc = wordApp.Documents.Open(templatePath)
            
            With wordDoc.Content.Find
                .Execute FindText:="<<név>>", ReplaceWith:=name, Replace:=2
                .Execute FindText:="<<üzenet>>", ReplaceWith:=Message, Replace:=2
            End With

            wordDoc.SaveAs2 savePath & name & "_Letter.docx"
            wordDoc.ExportAsFixedFormat OutputFileName:=savePath & name & "_Letter.pdf", ExportFormat:=17

            wordDoc.Close SaveChanges:=False
        Next i
    End With

    wordApp.Quit
    Set wordApp = Nothing
    MsgBox "All documents generated!"
End Sub

