' GENPDF macro - PDF Export for Word documents
' This macro exports the Word document into 3 different PDF files:
' - Review part only (for portal upload)
' - Grade part only (for portal upload) 
' - Print version with review twice + grade (for printing)
' Shortcut: Ctrl+Shift+P

Sub ExportToPDF()
    On Error GoTo ErrorHandler
    
    ' Declare variables
    Dim doc As Document
    Dim totalPages As Integer
    Dim reviewPages As Integer
    Dim gradePages As Integer
    Dim docPath As String
    Dim docName As String
    Dim baseName As String
    Dim reviewPdfPath As String
    Dim gradePdfPath As String
    Dim printPdfPath As String
    Dim tempDoc As Document
    Dim rng As Range
    Dim isOddPages As Boolean
    
    Set doc = ActiveDocument
    
    ' Check if document is saved
    If doc.Path = "" Then
        MsgBox "A dokumentumot először menteni kell!", vbCritical
        Exit Sub
    End If
    
    ' Get document info
    docPath = doc.Path
    docName = doc.Name
    baseName = Left(docName, InStrRev(docName, ".") - 1)
    
    ' Calculate page numbers
    totalPages = doc.ComputeStatistics(wdStatisticPages)
    reviewPages = totalPages - 1
    gradePages = 1
    
    If reviewPages < 1 Then
        MsgBox "A dokumentumnak legalább 2 oldalasnak kell lennie (bírálat + jegy)!", vbCritical
        Exit Sub
    End If
    
    ' Determine if review part has odd number of pages (for print version)
    isOddPages = (reviewPages Mod 2 = 1)
    
    ' Set PDF file paths
    reviewPdfPath = docPath & "\" & baseName & "_Review.pdf"
    gradePdfPath = docPath & "\" & baseName & "_Grade.pdf"
    printPdfPath = docPath & "\" & baseName & "_Print.pdf"
    
    Application.ScreenUpdating = False
    
    ' 1. Export Review PDF (PDF_REV) - All pages except last
    Call ExportPageRange(doc, reviewPdfPath, 1, reviewPages, "Bírálat PDF")
    
    ' 2. Export Grade PDF (PDF_GRADE) - Only last page
    Call ExportPageRange(doc, gradePdfPath, totalPages, totalPages, "Jegy PDF")
    
    ' 3. Create Print PDF (PDF_PRN) - Review twice + Grade
    Call CreatePrintPDF(doc, printPdfPath, reviewPages, totalPages, isOddPages)
    
    Application.ScreenUpdating = True
    
    MsgBox "PDF fájlok sikeresen létrehozva:" & vbCrLf & _
           "- " & baseName & "_Review.pdf" & vbCrLf & _
           "- " & baseName & "_Grade.pdf" & vbCrLf & _
           "- " & baseName & "_Print.pdf", vbInformation
    
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    MsgBox "Hiba történt a PDF export során: " & Err.Description, vbCritical
End Sub

' Helper function to export a specific page range to PDF
Private Sub ExportPageRange(doc As Document, pdfPath As String, startPage As Integer, endPage As Integer, description As String)
    On Error GoTo ExportError
    
    ' Delete existing file if it exists
    If Dir(pdfPath) <> "" Then
        Kill pdfPath
    End If
    
    ' Export to PDF
    doc.ExportAsFixedFormat _
        OutputFileName:=pdfPath, _
        ExportFormat:=wdExportFormatPDF, _
        OpenAfterExport:=False, _
        OptimizeFor:=wdExportOptimizeForMinimumSize, _
        BitmapMissingFonts:=True, _
        DocStructureTags:=True, _
        CreateBookmarks:=wdExportCreateNoBookmarks, _
        Range:=wdExportFromTo, _
        From:=startPage, _
        To:=endPage
    
    Exit Sub
    
ExportError:
    MsgBox "Hiba a " & description & " exportálása során: " & Err.Description, vbWarning
End Sub

' Helper function to create the print PDF with specific layout
Private Sub CreatePrintPDF(doc As Document, pdfPath As String, reviewPages As Integer, totalPages As Integer, isOddPages As Boolean)
    On Error GoTo PrintError
    
    Dim tempDoc As Document
    Dim sourceRange As Range
    Dim targetRange As Range
    
    ' Create new temporary document for print version
    Set tempDoc = Documents.Add
    
    ' Copy review content first time (preserving formatting)
    Set sourceRange = doc.Range
    sourceRange.Start = doc.Range.Start
    
    ' Get the end position more reliably
    If reviewPages = 1 Then
        ' For single page review, find the last paragraph before the grade page
        Dim lastPageStart As Long
        lastPageStart = doc.GoTo(wdGoToPage, wdGoToAbsolute, totalPages).Start
        
        ' Search backwards for the last paragraph before the grade page
        Dim i As Integer
        For i = doc.Paragraphs.Count To 1 Step -1
            If doc.Paragraphs(i).Range.Start < lastPageStart Then
                sourceRange.End = doc.Paragraphs(i).Range.End
                Exit For
            End If
        Next i
    Else
        ' For multi-page review, use a more reliable method
        ' Find content before last page starts
        Dim gradePageStart As Long
        gradePageStart = doc.GoTo(wdGoToPage, wdGoToAbsolute, totalPages).Start
        
        ' Find the last paragraph that's definitely in the review section
        Dim j As Integer
        For j = doc.Paragraphs.Count To 1 Step -1
            If doc.Paragraphs(j).Range.Start < gradePageStart Then
                sourceRange.End = doc.Paragraphs(j).Range.End
                Exit For
            End If
        Next j
    End If
    
    ' Insert review content first time
    sourceRange.Copy
    Set targetRange = tempDoc.Range
    targetRange.Paste
    
    ' Add page break after first copy
    Set targetRange = tempDoc.Range
    targetRange.Collapse wdCollapseEnd
    targetRange.InsertBreak Type:=wdPageBreak
    
    ' If review has odd pages, add one more page break to create empty page
    If isOddPages Then
        targetRange.InsertBreak Type:=wdPageBreak
    End If
    
    ' Copy review content second time
    sourceRange.Copy
    Set targetRange = tempDoc.Range
    targetRange.Collapse wdCollapseEnd
    targetRange.Paste
    
    ' Add page break after second copy
    Set targetRange = tempDoc.Range
    targetRange.Collapse wdCollapseEnd
    targetRange.InsertBreak Type:=wdPageBreak
    
    ' If review has odd pages, add one more page break to create empty page
    If isOddPages Then
        targetRange.InsertBreak Type:=wdPageBreak
    End If
    
    ' Copy grade content (last page)
    Set sourceRange = doc.Range
    sourceRange.Start = doc.GoTo(wdGoToPage, wdGoToAbsolute, totalPages).Start
    sourceRange.End = doc.Range.End
    
    sourceRange.Copy
    Set targetRange = tempDoc.Range
    targetRange.Collapse wdCollapseEnd
    targetRange.Paste
    
    ' Delete existing file if it exists
    If Dir(pdfPath) <> "" Then
        Kill pdfPath
    End If
    
    ' Export temporary document to PDF
    tempDoc.ExportAsFixedFormat _
        OutputFileName:=pdfPath, _
        ExportFormat:=wdExportFormatPDF, _
        OpenAfterExport:=False, _
        OptimizeFor:=wdExportOptimizeForMinimumSize, _
        BitmapMissingFonts:=True, _
        DocStructureTags:=True, _
        CreateBookmarks:=wdExportCreateNoBookmarks
    
    ' Close temporary document without saving
    tempDoc.Close SaveChanges:=wdDoNotSaveChanges
    Set tempDoc = Nothing
    
    Exit Sub
    
PrintError:
    If Not tempDoc Is Nothing Then
        tempDoc.Close SaveChanges:=wdDoNotSaveChanges
    End If
    MsgBox "Hiba a nyomtatási PDF létrehozása során: " & Err.Description, vbWarning
End Sub

' Assign keyboard shortcut (this should be called when document opens)
Sub AssignPdfShortcut()
    CustomizationContext = ActiveDocument
    KeyBindings.Add KeyCode:=BuildKeyCode(wdKeyControl, wdKeyShift, wdKeyP), _
                   KeyCategory:=wdKeyCategoryMacro, _
                   Command:="ExportToPDF"
End Sub

' Remove keyboard shortcut
Sub RemovePdfShortcut()
    On Error Resume Next
    CustomizationContext = ActiveDocument
    KeyBindings(BuildKeyCode(wdKeyControl, wdKeyShift, wdKeyP)).Delete
    On Error GoTo 0
End Sub

' Auto-assign shortcut when document opens
Sub AutoOpen()
    Call AssignPdfShortcut
End Sub

' Remove shortcut when document closes
Sub AutoClose()
    Call RemovePdfShortcut
End Sub
