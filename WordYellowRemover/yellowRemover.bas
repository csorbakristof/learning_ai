Attribute VB_Name = "YellowRemover"
' =============================================================================
' Yellow Text Remover Macro (Optimized Version)
' =============================================================================
' This macro removes all text with yellow background (highlight or shading)
' from the current Word document using Find & Replace for speed.
' Hotkey: Ctrl+Shift+Y
' =============================================================================

Option Explicit

' Main procedure to remove yellow highlighted/shaded text
Sub RemoveYellowText()
    Dim doc As Document
    Dim removedCount As Long
    
    ' Start undo transaction
    Application.ScreenUpdating = False
    Set doc = ActiveDocument
    
    removedCount = 0
    
    ' Process yellow highlighting using Find & Replace
    removedCount = removedCount + RemoveYellowHighlight(doc)
    
    ' Process yellow shading using Find & Replace
    removedCount = removedCount + RemoveYellowShading(doc)
    
    ' Process tables separately
    removedCount = removedCount + ProcessTables(doc)
    
    Application.ScreenUpdating = True
    
    ' Show completion message
    MsgBox "Yellow text removal complete!" & vbCrLf & _
           "Items removed: " & removedCount, _
           vbInformation, "Yellow Remover"
End Sub

' Remove all text with yellow highlighting using Find
Private Function RemoveYellowHighlight(doc As Document) As Long
    Dim rng As Range
    Dim findCount As Long
    
    findCount = 0
    Set rng = doc.Content
    
    With rng.Find
        .ClearFormatting
        .Highlight = True
        .Text = ""
        .Forward = True
        .Wrap = wdFindStop
        .Format = True
        
        ' Find all yellow highlighted text
        Do While .Execute
            ' Check if it's yellow highlight
            If rng.HighlightColorIndex = wdYellow Then
                rng.Text = ""
                findCount = findCount + 1
            End If
            ' Move past current position to avoid infinite loop
            rng.Collapse wdCollapseEnd
            If rng.End = doc.Content.End Then Exit Do
        Loop
    End With
    
    RemoveYellowHighlight = findCount
End Function

' Remove all text with yellow shading using Find
Private Function RemoveYellowShading(doc As Document) As Long
    Dim rng As Range
    Dim findCount As Long
    Dim shadingColor As Long
    
    findCount = 0
    Set rng = doc.Content
    
    With rng.Find
        .ClearFormatting
        .Text = ""
        .Forward = True
        .Wrap = wdFindStop
        .Format = True
        
        ' Set yellow shading pattern
        .Replacement.ClearFormatting
        .Replacement.Shading.BackgroundPatternColor = wdColorYellow
        
        ' Find all yellow shaded text
        Do While .Execute
            ' Check if it's yellow shading
            shadingColor = rng.Shading.BackgroundPatternColor
            If IsYellowColor(shadingColor) Then
                rng.Text = ""
                findCount = findCount + 1
            End If
            ' Move past current position
            rng.Collapse wdCollapseEnd
            If rng.End = doc.Content.End Then Exit Do
        Loop
    End With
    
    RemoveYellowShading = findCount
End Function

' Process tables for yellow backgrounds
Private Function ProcessTables(doc As Document) As Long
    Dim tbl As Table
    Dim cell As cell
    Dim cellRange As Range
    Dim removedCount As Long
    
    removedCount = 0
    
    For Each tbl In doc.Tables
        For Each cell In tbl.Range.Cells
            Set cellRange = cell.Range
            ' Adjust range to exclude cell end marker
            cellRange.MoveEnd wdCharacter, -1
            
            ' Check if entire cell has yellow background
            If IsYellowColor(cell.Range.Shading.BackgroundPatternColor) Then
                ' Clear entire cell content
                cellRange.Text = ""
                removedCount = removedCount + 1
            Else
                ' Process yellow highlighted text within cell
                removedCount = removedCount + ProcessCellContent(cellRange)
            End If
        Next cell
    Next tbl
    
    ProcessTables = removedCount
End Function

' Process content within a single cell
Private Function ProcessCellContent(cellRange As Range) As Long
    Dim findCount As Long
    Dim rng As Range
    Dim shadingColor As Long
    
    findCount = 0
    Set rng = cellRange.Duplicate
    
    ' Find yellow highlighted text in cell
    With rng.Find
        .ClearFormatting
        .Highlight = True
        .Text = ""
        .Forward = True
        .Wrap = wdFindStop
        .Format = True
        
        Do While .Execute
            If rng.HighlightColorIndex = wdYellow Then
                rng.Text = ""
                findCount = findCount + 1
            End If
            rng.Collapse wdCollapseEnd
            If rng.End >= cellRange.End - 1 Then Exit Do
        Loop
    End With
    
    ' Find yellow shaded text in cell
    Set rng = cellRange.Duplicate
    With rng.Find
        .ClearFormatting
        .Text = ""
        .Forward = True
        .Wrap = wdFindStop
        .Format = True
        
        Do While .Execute
            shadingColor = rng.Shading.BackgroundPatternColor
            If IsYellowColor(shadingColor) Then
                rng.Text = ""
                findCount = findCount + 1
            End If
            rng.Collapse wdCollapseEnd
            If rng.End >= cellRange.End - 1 Then Exit Do
        Loop
    End With
    
    ProcessCellContent = findCount
End Function

' Check if a color is yellow or a yellow variation
Private Function IsYellowColor(colorValue As Long) As Boolean
    ' Check for yellow color (RGB yellow or close to yellow)
    ' Yellow is RGB(255, 255, 0) = 65535 in VBA
    If colorValue = wdColorYellow Or _
       colorValue = 65535 Or _
       colorValue = RGB(255, 255, 0) Or _
       colorValue = RGB(255, 255, 102) Or _
       colorValue = RGB(255, 255, 153) Then
        IsYellowColor = True
    Else
        IsYellowColor = False
    End If
End Function
