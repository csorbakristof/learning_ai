Option Explicit

' Constants
Const TEMPLATE_FILENAME = "FeladatkiirasSablonAUT.docx"

' Workbook Event Handler - Register hotkeys when workbook opens
Private Sub Workbook_Open()
    ' Register Ctrl+Shift+C for CollectStudents
    Application.OnKey "^+C", "CollectStudents"
    ' Register Ctrl+Shift+G for GenerateTaskDescriptions
    Application.OnKey "^+G", "GenerateTaskDescriptions"
End Sub

' Main macro for collecting students data
Sub CollectStudents()
    On Error GoTo ErrorHandler
    
    Dim controllerWb As Workbook
    Dim terhelesWb As Workbook
    Dim controllerWs As Worksheet
    Dim terhelesWs As Worksheet
    Dim tantargyiWs As Worksheet
    Dim generaltWs As Worksheet
    
    Dim terhelesFileName As String
    Dim terhelesFilePath As String
    Dim konzultacioWsName As String
    
    Dim sourceLastRow As Long
    Dim targetRow As Long
    Dim i As Long
    
    ' Column indices for source data
    Dim colHallgatoNeve As Long
    Dim colNeptunKod As Long
    Dim colTargyKod As Long
    Dim colKonzulensNeve As Long
    
    ' Column indices for target data
    Dim targetColHallgatoNeve As Long
    Dim targetColNeptunKod As Long
    Dim targetColTargyKod As Long
    Dim targetColDolgozatMegnevezese As Long
    Dim targetColSzakMegnevezese As Long
    Dim targetColKonzulensNeve As Long
    Dim targetColKonzulensBeosztasa As Long
    Dim targetColFeladatkiirasFajlnev As Long
    
    Set controllerWb = ThisWorkbook
    
    ' Step 1: Find the Terheles excel file
    terhelesFileName = FindTerhelesFile(controllerWb.Path)
    If terhelesFileName = "" Then
        MsgBox "Hiba: Nem található 'Terheles' kezdetű Excel fájl a következő könyvtárban: " & controllerWb.Path & vbCrLf & _
               "Ellenőrizze, hogy a Terheles fájl ugyanabban a könyvtárban van-e, mint a vezérlő Excel fájl.", _
               vbCritical, "Fájl nem található"
        Exit Sub
    End If
    
    terhelesFilePath = controllerWb.Path & "\" & terhelesFileName
    
    ' Step 2: Open the Terheles excel file
    Set terhelesWb = Workbooks.Open(terhelesFilePath, ReadOnly:=True)
    
    ' Step 3: Find the konzultáció worksheet
    konzultacioWsName = FindKonzultacioWorksheet(terhelesWb)
    If konzultacioWsName = "" Then
        terhelesWb.Close False
        MsgBox "Hiba: Nem található 'konzultáció' szót tartalmazó munkalap a fájlban: " & terhelesFileName & vbCrLf & _
               "Ellenőrizze, hogy van-e olyan munkalap, amelynek nevében szerepel a 'konzultáció' szó.", _
               vbCritical, "Munkalap nem található"
        Exit Sub
    End If
    
    Set terhelesWs = terhelesWb.Worksheets(konzultacioWsName)
    
    ' Step 4: Get references to controller worksheets
    Set generaltWs = GetWorksheet(controllerWb, "GeneráltHallgatóiLista")
    If generaltWs Is Nothing Then
        terhelesWb.Close False
        MsgBox "Hiba: Nem található a 'GeneráltHallgatóiLista' munkalap a vezérlő Excel fájlban." & vbCrLf & _
               "Ellenőrizze, hogy létezik-e ilyen nevű munkalap.", _
               vbCritical, "Munkalap nem található"
        Exit Sub
    End If
    
    Set tantargyiWs = GetWorksheet(controllerWb, "Tantárgyi adatok")
    If tantargyiWs Is Nothing Then
        terhelesWb.Close False
        MsgBox "Hiba: Nem található a 'Tantárgyi adatok' munkalap a vezérlő Excel fájlban." & vbCrLf & _
               "Ellenőrizze, hogy létezik-e ilyen nevű munkalap.", _
               vbCritical, "Munkalap nem található"
        Exit Sub
    End If
    
    ' Step 5: Find column indices in source worksheet
    colHallgatoNeve = FindColumnIndex(terhelesWs, "Hallgató neve")
    colNeptunKod = FindColumnIndex(terhelesWs, "Hallg. nept")
    colTargyKod = FindColumnIndex(terhelesWs, "Tárgy nept")
    colKonzulensNeve = FindColumnIndex(terhelesWs, "Konzulens")
    
    If colHallgatoNeve = 0 Or colNeptunKod = 0 Or colTargyKod = 0 Or colKonzulensNeve = 0 Then
        terhelesWb.Close False
        MsgBox "Hiba: Nem találhatók a szükséges oszlopok a(z) '" & konzultacioWsName & "' munkalapon." & vbCrLf & _
               "Szükséges oszlopok: 'Hallgató neve', 'Hallg. nept', 'Tárgy nept', 'Konzulens'" & vbCrLf & _
               "Ellenőrizze az oszlopfejléceket.", _
               vbCritical, "Oszlopok nem találhatók"
        Exit Sub
    End If
    
    ' Step 6: Find column indices in target worksheet
    targetColHallgatoNeve = FindColumnIndex(generaltWs, "Hallgató neve")
    targetColNeptunKod = FindColumnIndex(generaltWs, "Neptun kód")
    targetColTargyKod = FindColumnIndex(generaltWs, "Tárgykód")
    targetColDolgozatMegnevezese = FindColumnIndex(generaltWs, "Dolgozat megnevezése")
    targetColSzakMegnevezese = FindColumnIndex(generaltWs, "Szak megnevezése")
    targetColKonzulensNeve = FindColumnIndex(generaltWs, "Konzulens neve")
    targetColKonzulensBeosztasa = FindColumnIndex(generaltWs, "Konzulens beosztása")
    targetColFeladatkiirasFajlnev = FindColumnIndex(generaltWs, "Feladatkiírás fájlnév")
    
    If targetColHallgatoNeve = 0 Or targetColNeptunKod = 0 Or targetColTargyKod = 0 Or _
       targetColDolgozatMegnevezese = 0 Or targetColSzakMegnevezese = 0 Or targetColKonzulensNeve = 0 Or _
       targetColKonzulensBeosztasa = 0 Or targetColFeladatkiirasFajlnev = 0 Then
        terhelesWb.Close False
        MsgBox "Hiba: Nem találhatók a szükséges oszlopok a 'GeneráltHallgatóiLista' munkalapon." & vbCrLf & _
               "Szükséges oszlopok: 'Hallgató neve', 'Neptun kód', 'Tárgykód', 'Dolgozat megnevezése', " & _
               "'Szak megnevezése', 'Konzulens neve', 'Konzulens beosztása', 'Feladatkiírás fájlnév'" & vbCrLf & _
               "Ellenőrizze az oszlopfejléceket.", _
               vbCritical, "Oszlopok nem találhatók"
        Exit Sub
    End If
    
    ' Step 7: Clear existing data in target worksheet (keep headers)
    sourceLastRow = terhelesWs.Cells(terhelesWs.Rows.Count, colHallgatoNeve).End(xlUp).Row
    If sourceLastRow < 2 Then
        terhelesWb.Close False
        MsgBox "Hiba: Nincsenek adatok a(z) '" & konzultacioWsName & "' munkalapon." & vbCrLf & _
               "Ellenőrizze, hogy vannak-e hallgatói adatok a munkalapon.", _
               vbExclamation, "Nincsenek adatok"
        Exit Sub
    End If
    
    ' Clear existing data but keep headers
    generaltWs.Range("2:" & generaltWs.Rows.Count).Delete
    
    ' Step 8: Copy data and create formulas
    targetRow = 2 ' Start from row 2 (after headers)
    
    For i = 2 To sourceLastRow
        ' Copy direct values
        generaltWs.Cells(targetRow, targetColHallgatoNeve).Value = terhelesWs.Cells(i, colHallgatoNeve).Value
        generaltWs.Cells(targetRow, targetColNeptunKod).Value = terhelesWs.Cells(i, colNeptunKod).Value
        generaltWs.Cells(targetRow, targetColTargyKod).Value = terhelesWs.Cells(i, colTargyKod).Value
        
        ' Clean up Konzulens neve by removing anything in brackets
        Dim konzulensName As String
        konzulensName = CleanKonzulensName(terhelesWs.Cells(i, colKonzulensNeve).Value)
        generaltWs.Cells(targetRow, targetColKonzulensNeve).Value = konzulensName
        
        ' Leave Konzulens beosztása empty as specified
        generaltWs.Cells(targetRow, targetColKonzulensBeosztasa).Value = ""
        
        ' Create VLOOKUP formulas for Dolgozat megnevezése
        generaltWs.Cells(targetRow, targetColDolgozatMegnevezese).Formula = _
            "=IFERROR(VLOOKUP(" & generaltWs.Cells(targetRow, targetColTargyKod).Address & _
            ",'Tantárgyi adatok'!B:D,2,FALSE),""nincs"")"
        
        ' Create VLOOKUP formulas for Szak megnevezése
        generaltWs.Cells(targetRow, targetColSzakMegnevezese).Formula = _
            "=IFERROR(VLOOKUP(" & generaltWs.Cells(targetRow, targetColTargyKod).Address & _
            ",'Tantárgyi adatok'!B:D,3,FALSE),""nincs"")"
        
        ' Create Feladatkiírás fájlnév with cleaned student name
        Dim cleanedName As String
        cleanedName = CleanStudentName(terhelesWs.Cells(i, colHallgatoNeve).Value)
        generaltWs.Cells(targetRow, targetColFeladatkiirasFajlnev).Value = cleanedName & ".docx"
        
        targetRow = targetRow + 1
    Next i
    
    ' Step 9: Close the Terheles excel file
    terhelesWb.Close False
    
    ' Success message
    MsgBox "Sikeres adatgyűjtés!" & vbCrLf & _
           "Összesen " & (sourceLastRow - 1) & " hallgató adatai lettek betöltve a 'GeneráltHallgatóiLista' munkalapon.", _
           vbInformation, "Művelet befejezve"
    
    Exit Sub
    
ErrorHandler:
    If Not terhelesWb Is Nothing Then
        terhelesWb.Close False
    End If
    MsgBox "Hiba történt a művelet során:" & vbCrLf & vbCrLf & _
           "Hiba leírása: " & Err.Description & vbCrLf & _
           "Hiba száma: " & Err.Number & vbCrLf & vbCrLf & _
           "Ellenőrizze az adatforrásokat és próbálja újra.", _
           vbCritical, "Váratlan hiba"
End Sub

' Main macro for generating task descriptions
Sub GenerateTaskDescriptions()
    On Error GoTo ErrorHandler
    
    Dim controllerWb As Workbook
    Dim generaltWs As Worksheet
    Dim templatePath As String
    Dim outputDir As String
    
    Dim lastRow As Long
    Dim currentRow As Long
    Dim processedCount As Long
    Dim skippedCount As Long
    Dim errorCount As Long
    
    ' Column indices
    Dim colHallgatoNeve As Long
    Dim colDolgozatMegnevezese As Long
    Dim colSzakMegnevezese As Long
    Dim colKonzulensNeve As Long
    Dim colFeladatkiirasFajlnev As Long
    
    ' Word application variables
    Dim wordApp As Object
    Dim wordDoc As Object
    Dim wordStarted As Boolean
    
    ' Variables for row processing
    Dim studentName As String
    Dim dolgozatMegnevezese As String
    Dim szakMegnevezese As String
    Dim konzulensNeve As String
    Dim outputFilename As String
    Dim cleanedAdvisorName As String
    Dim fullOutputPath As String
    
    Set controllerWb = ThisWorkbook
    wordStarted = False
    
    ' Step 1: Get reference to GeneráltHallgatóiLista worksheet
    Set generaltWs = GetWorksheet(controllerWb, "GeneráltHallgatóiLista")
    If generaltWs Is Nothing Then
        MsgBox "Hiba: Nem található a 'GeneráltHallgatóiLista' munkalap a vezérlő Excel fájlban." & vbCrLf & _
               "Ellenőrizze, hogy létezik-e ilyen nevű munkalap.", _
               vbCritical, "Munkalap nem található"
        Exit Sub
    End If
    
    ' Step 2: Check if template file exists
    templatePath = controllerWb.Path & "\" & TEMPLATE_FILENAME
    If Dir(templatePath) = "" Then
        MsgBox "Hiba: Nem található a sablon fájl: " & templatePath & vbCrLf & _
               "Ellenőrizze, hogy a '" & TEMPLATE_FILENAME & "' fájl ugyanabban a könyvtárban van-e, mint a vezérlő Excel fájl.", _
               vbCritical, "Sablon fájl nem található"
        Exit Sub
    End If
    
    ' Step 3: Find column indices
    colHallgatoNeve = FindColumnIndex(generaltWs, "Hallgató neve")
    colDolgozatMegnevezese = FindColumnIndex(generaltWs, "Dolgozat megnevezése")
    colSzakMegnevezese = FindColumnIndex(generaltWs, "Szak megnevezése")
    colKonzulensNeve = FindColumnIndex(generaltWs, "Konzulens neve")
    colFeladatkiirasFajlnev = FindColumnIndex(generaltWs, "Feladatkiírás fájlnév")
    
    If colHallgatoNeve = 0 Or colDolgozatMegnevezese = 0 Or colSzakMegnevezese = 0 Or _
       colKonzulensNeve = 0 Or colFeladatkiirasFajlnev = 0 Then
        MsgBox "Hiba: Nem találhatók a szükséges oszlopok a 'GeneráltHallgatóiLista' munkalapon." & vbCrLf & _
               "Szükséges oszlopok: 'Hallgató neve', 'Dolgozat megnevezése', 'Szak megnevezése', " & _
               "'Konzulens neve', 'Feladatkiírás fájlnév'" & vbCrLf & _
               "Ellenőrizze az oszlopfejléceket.", _
               vbCritical, "Oszlopok nem találhatók"
        Exit Sub
    End If
    
    ' Step 4: Get data range
    lastRow = generaltWs.Cells(generaltWs.Rows.Count, colHallgatoNeve).End(xlUp).Row
    If lastRow < 2 Then
        MsgBox "Hiba: Nincsenek adatok a 'GeneráltHallgatóiLista' munkalapon." & vbCrLf & _
               "Futtassa először a CollectStudents makrót az adatok betöltéséhez.", _
               vbExclamation, "Nincsenek adatok"
        Exit Sub
    End If
    
    ' Step 5: Create output directory
    outputDir = controllerWb.Path & "\kiirasok"
    If Dir(outputDir, vbDirectory) = "" Then
        MkDir outputDir
    End If
    
    ' Step 6: Start Word application
    On Error Resume Next
    Set wordApp = GetObject(, "Word.Application")
    If Err.Number <> 0 Then
        Err.Clear
        Set wordApp = CreateObject("Word.Application")
        wordStarted = True
    End If
    On Error GoTo ErrorHandler
    
    wordApp.Visible = False ' Run in background for faster processing
    
    ' Step 7: Process each row
    For currentRow = 2 To lastRow
        ' Update progress
        Application.StatusBar = "Dokumentum generálás... (" & (currentRow - 1) & "/" & (lastRow - 1) & ")"
        
        ' Get values from current row
        studentName = generaltWs.Cells(currentRow, colHallgatoNeve).Value
        dolgozatMegnevezese = generaltWs.Cells(currentRow, colDolgozatMegnevezese).Value
        szakMegnevezese = generaltWs.Cells(currentRow, colSzakMegnevezese).Value
        konzulensNeve = generaltWs.Cells(currentRow, colKonzulensNeve).Value
        outputFilename = generaltWs.Cells(currentRow, colFeladatkiirasFajlnev).Value
        
        ' Skip rows with "nincs" or "0" values
        If dolgozatMegnevezese = "nincs" Or dolgozatMegnevezese = "0" Or _
           szakMegnevezese = "nincs" Or szakMegnevezese = "0" Then
            skippedCount = skippedCount + 1
            GoTo NextRow
        End If
        
        ' Create advisor subdirectory
        Dim advisorDir As String
        cleanedAdvisorName = CleanStudentName(konzulensNeve) ' Reuse the same cleaning function
        advisorDir = outputDir & "\" & cleanedAdvisorName
        
        ' Create advisor directory if it doesn't exist
        If Dir(advisorDir, vbDirectory) = "" Then
            MkDir advisorDir
        End If
        
        ' Construct full output path with advisor subdirectory
        Dim justFilename As String
        ' The filename is now just the filename without any path prefix
        justFilename = outputFilename
        fullOutputPath = advisorDir & "\" & justFilename
        
        ' Process the document
        If ProcessWordDocument(wordApp, templatePath, fullOutputPath, _
                              dolgozatMegnevezese, szakMegnevezese, konzulensNeve, studentName) Then
            processedCount = processedCount + 1
        Else
            errorCount = errorCount + 1
            GoTo ErrorInProcessing
        End If
        
NextRow:
    Next currentRow
    
    ' Step 8: Close Word if we started it
    If wordStarted Then
        wordApp.Quit
    End If
    
    ' Step 9: Clear status bar and show completion message
    Application.StatusBar = False
    
    MsgBox "Feladatkiírás generálás befejezve!" & vbCrLf & vbCrLf & _
           "Feldolgozott dokumentumok: " & processedCount & vbCrLf & _
           "Kihagyott sorok: " & skippedCount & vbCrLf & _
           "Hibák száma: " & errorCount & vbCrLf & vbCrLf & _
           "A dokumentumok konzulens szerint rendszerezve találhatók itt: " & outputDir & vbCrLf & _
           "Minden konzulensnek külön almappája van a tisztított nevükkel.", _
           vbInformation, "Művelet befejezve"
    
    Exit Sub
    
ErrorInProcessing:
    If wordStarted Then wordApp.Quit
    Application.StatusBar = False
    MsgBox "Hiba történt a dokumentum feldolgozása során!" & vbCrLf & vbCrLf & _
           "Hallgató: " & studentName & vbCrLf & _
           "Dolgozat megnevezése: " & dolgozatMegnevezese & vbCrLf & _
           "Szak megnevezése: " & szakMegnevezese & vbCrLf & _
           "Konzulens neve: " & konzulensNeve & vbCrLf & _
           "Konzulens mappa: " & cleanedAdvisorName & vbCrLf & _
           "Kimeneti fájl: " & fullOutputPath & vbCrLf & vbCrLf & _
           "Lehetséges okok és megoldások:" & vbCrLf & _
           "• A sablon dokumentumban hiányoznak a legördülő listák" & vbCrLf & _
           "• Az Excel adatok nem találhatók a Word legördülő listákban" & vbCrLf & _
           "• A sablon fájl nem megfelelő formátumú vagy sérült" & vbCrLf & _
           "• Nincs írási jogosultság a kimeneti könyvtárba" & vbCrLf & vbCrLf & _
           "Ellenőrizze a sablon fájlt és az adatok helyességét, majd próbálja újra.", _
           vbCritical, "Dokumentum feldolgozási hiba"
    Exit Sub
    
ErrorHandler:
    If wordStarted And Not wordApp Is Nothing Then wordApp.Quit
    Application.StatusBar = False
    MsgBox "Hiba történt a feladatkiírás generálás során:" & vbCrLf & vbCrLf & _
           "Hiba leírása: " & Err.Description & vbCrLf & _
           "Hiba száma: " & Err.Number & vbCrLf & vbCrLf & _
           "Ellenőrizze a sablon fájlt és az adatokat, majd próbálja újra.", _
           vbCritical, "Váratlan hiba"
End Sub

' Helper function to process a single Word document
Private Function ProcessWordDocument(wordApp As Object, templatePath As String, outputPath As String, _
                                   dolgozat As String, szak As String, konzulens As String, student As String) As Boolean
    On Error GoTo ErrorHandler
    
    Dim wordDoc As Object
    Dim contentControls As Object
    Dim cc As Object
    Dim found As Boolean
    Dim currentDate As String
    
    ' Create Hungarian formatted date
    currentDate = "Budapest, " & Year(Date) & ". " & GetHungarianMonth(Month(Date)) & " " & Day(Date) & "."
    
    ' Open template document
    Set wordDoc = wordApp.Documents.Open(templatePath)
    
    ' Get content controls collection
    Set contentControls = wordDoc.ContentControls
    
    ' Process the first two content controls (assuming they are dropdowns)
    If contentControls.Count < 2 Then
        MsgBox "Hiba: A sablon dokumentumban nem található elegendő tartalom vezérlő elem." & vbCrLf & vbCrLf & _
               "Szükséges: legalább 2 legördülő lista (Content Control)" & vbCrLf & _
               "Találva: " & contentControls.Count & " tartalom vezérlő elem" & vbCrLf & vbCrLf & _
               "Megoldás:" & vbCrLf & _
               "1. Nyissa meg a '" & TEMPLATE_FILENAME & "' fájlt Word-ben" & vbCrLf & _
               "2. Helyezzen be 2 legördülő lista Content Control elemet" & vbCrLf & _
               "3. Az első legyen a 'Dolgozat megnevezése' számára" & vbCrLf & _
               "4. A második legyen a 'Szak megnevezése' számára" & vbCrLf & _
               "5. Adja hozzá a megfelelő opciókat mindkét listához", _
               vbCritical, "Sablon Content Control hiba"
        wordDoc.Close False
        ProcessWordDocument = False
        Exit Function
    End If
    
    ' Set first dropdown (Dolgozat megnevezése)
    Set cc = contentControls(1)
    If Not SetDropdownValue(cc, dolgozat) Then
        MsgBox "Hiba: Nem található a dolgozat megnevezés az első legördülő listában!" & vbCrLf & vbCrLf & _
               "Keresett érték: '" & dolgozat & "'" & vbCrLf & _
               "Hallgató: " & student & vbCrLf & vbCrLf & _
               "Megoldás:" & vbCrLf & _
               "1. Nyissa meg a '" & TEMPLATE_FILENAME & "' fájlt Word-ben" & vbCrLf & _
               "2. Kattintson az első legördülő listára (Dolgozat megnevezése)" & vbCrLf & _
               "3. Adja hozzá a '" & dolgozat & "' opciót a listához" & vbCrLf & _
               "4. Vagy ellenőrizze a 'Tantárgyi adatok' munkalapon az adatok helyességét", _
               vbCritical, "Dolgozat megnevezése hiba"
        wordDoc.Close False
        ProcessWordDocument = False
        Exit Function
    End If
    
    ' Set second dropdown (Szak megnevezése)
    Set cc = contentControls(2)
    If Not SetDropdownValue(cc, szak) Then
        MsgBox "Hiba: Nem található a szak megnevezés a második legördülő listában!" & vbCrLf & vbCrLf & _
               "Keresett érték: '" & szak & "'" & vbCrLf & _
               "Hallgató: " & student & vbCrLf & vbCrLf & _
               "Megoldás:" & vbCrLf & _
               "1. Nyissa meg a '" & TEMPLATE_FILENAME & "' fájlt Word-ben" & vbCrLf & _
               "2. Kattintson a második legördülő listára (Szak megnevezése)" & vbCrLf & _
               "3. Adja hozzá a '" & szak & "' opciót a listához" & vbCrLf & _
               "4. Vagy ellenőrizze a 'Tantárgyi adatok' munkalapon az adatok helyességét", _
               vbCritical, "Szak megnevezése hiba"
        wordDoc.Close False
        ProcessWordDocument = False
        Exit Function
    End If
    
    ' Replace student name
    With wordDoc.Range.Find
        .Text = "Rezeda Kázmér"
        .Replacement.Text = student
        .Execute Replace:=2 ' wdReplaceAll
    End With
    
    ' Replace consultant name
    With wordDoc.Range.Find
        .Text = "Dr. Érték Elek"
        .Replacement.Text = konzulens
        .Execute Replace:=2 ' wdReplaceAll
    End With
    
    ' Replace date
    With wordDoc.Range.Find
        .Text = "Budapest, 2020. szeptember 4."
        .Replacement.Text = currentDate
        .Execute Replace:=2 ' wdReplaceAll
    End With
    
    ' Save document
    wordDoc.SaveAs2 outputPath
    wordDoc.Close
    
    ProcessWordDocument = True
    Exit Function
    
ErrorHandler:
    If Not wordDoc Is Nothing Then wordDoc.Close False
    ProcessWordDocument = False
End Function

' Helper function to set dropdown value in content control
Private Function SetDropdownValue(contentControl As Object, value As String) As Boolean
    On Error GoTo ErrorHandler
    
    Dim i As Integer
    Dim dropdownItems As Object
    
    ' Check if it's a dropdown list content control
    If contentControl.Type <> 3 Then ' wdContentControlDropdownList
        SetDropdownValue = False
        Exit Function
    End If
    
    Set dropdownItems = contentControl.DropdownListEntries
    
    ' Look for matching value
    For i = 1 To dropdownItems.Count
        If dropdownItems(i).Text = value Then
            contentControl.Range.Text = value
            SetDropdownValue = True
            Exit Function
        End If
    Next i
    
    ' Value not found
    SetDropdownValue = False
    Exit Function
    
ErrorHandler:
    SetDropdownValue = False
End Function

' Helper function to get Hungarian month name
Private Function GetHungarianMonth(monthNumber As Integer) As String
    Select Case monthNumber
        Case 1: GetHungarianMonth = "január"
        Case 2: GetHungarianMonth = "február"
        Case 3: GetHungarianMonth = "március"
        Case 4: GetHungarianMonth = "április"
        Case 5: GetHungarianMonth = "május"
        Case 6: GetHungarianMonth = "június"
        Case 7: GetHungarianMonth = "július"
        Case 8: GetHungarianMonth = "augusztus"
        Case 9: GetHungarianMonth = "szeptember"
        Case 10: GetHungarianMonth = "október"
        Case 11: GetHungarianMonth = "november"
        Case 12: GetHungarianMonth = "december"
        Case Else: GetHungarianMonth = "ismeretlen"
    End Select
End Function

' Helper function to find Terheles file in the directory
Private Function FindTerhelesFile(directoryPath As String) As String
    Dim fileName As String
    fileName = Dir(directoryPath & "\Terheles*.xls*")
    
    Do While fileName <> ""
        If Left(fileName, 1) <> "~" Then ' Skip temporary files
            FindTerhelesFile = fileName
            Exit Function
        End If
        fileName = Dir()
    Loop
    
    FindTerhelesFile = ""
End Function

' Helper function to find konzultáció worksheet
Private Function FindKonzultacioWorksheet(wb As Workbook) As String
    Dim ws As Worksheet
    
    For Each ws In wb.Worksheets
        If InStr(1, ws.Name, "konzultáció", vbTextCompare) > 0 Then
            FindKonzultacioWorksheet = ws.Name
            Exit Function
        End If
    Next ws
    
    FindKonzultacioWorksheet = ""
End Function

' Helper function to get worksheet by name
Private Function GetWorksheet(wb As Workbook, wsName As String) As Worksheet
    On Error Resume Next
    Set GetWorksheet = wb.Worksheets(wsName)
    On Error GoTo 0
End Function

' Helper function to find column index by header name
Private Function FindColumnIndex(ws As Worksheet, headerName As String) As Long
    Dim lastCol As Long
    Dim i As Long
    
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    
    For i = 1 To lastCol
        If Trim(ws.Cells(1, i).Value) = headerName Then
            FindColumnIndex = i
            Exit Function
        End If
    Next i
    
    FindColumnIndex = 0
End Function

' Helper function to clean student names for file system compatibility with PascalCasing
Private Function CleanStudentName(studentName As String) As String
    Dim cleanName As String
    Dim words As Variant
    Dim i As Integer
    Dim word As String
    Dim result As String
    
    ' First, replace accented characters with English letters
    cleanName = Trim(studentName)
    cleanName = Replace(cleanName, "Á", "A")
    cleanName = Replace(cleanName, "á", "a")
    cleanName = Replace(cleanName, "É", "E")
    cleanName = Replace(cleanName, "é", "e")
    cleanName = Replace(cleanName, "Í", "I")
    cleanName = Replace(cleanName, "í", "i")
    cleanName = Replace(cleanName, "Ó", "O")
    cleanName = Replace(cleanName, "ó", "o")
    cleanName = Replace(cleanName, "Ö", "O")
    cleanName = Replace(cleanName, "ö", "o")
    cleanName = Replace(cleanName, "Ő", "O")
    cleanName = Replace(cleanName, "ő", "o")
    cleanName = Replace(cleanName, "Ú", "U")
    cleanName = Replace(cleanName, "ú", "u")
    cleanName = Replace(cleanName, "Ü", "U")
    cleanName = Replace(cleanName, "ü", "u")
    cleanName = Replace(cleanName, "Ű", "U")
    cleanName = Replace(cleanName, "ű", "u")
    
    ' Remove problematic characters and replace with spaces for word separation
    cleanName = Replace(cleanName, "-", " ")
    cleanName = Replace(cleanName, ".", " ")
    cleanName = Replace(cleanName, ",", " ")
    cleanName = Replace(cleanName, "(", " ")
    cleanName = Replace(cleanName, ")", " ")
    
    ' Split by spaces and apply PascalCasing
    words = Split(cleanName, " ")
    result = ""
    
    For i = LBound(words) To UBound(words)
        word = Trim(words(i))
        If Len(word) > 0 Then
            ' Capitalize first letter, lowercase the rest
            word = UCase(Left(word, 1)) & LCase(Mid(word, 2))
            result = result & word
        End If
    Next i
    
    CleanStudentName = result
End Function

' Helper function to clean consultant names by removing text in brackets
Private Function CleanKonzulensName(konzulensName As String) As String
    Dim cleanName As String
    Dim bracketPos As Long
    
    cleanName = Trim(konzulensName)
    
    ' Find the position of the first opening bracket
    bracketPos = InStr(cleanName, "(")
    
    ' If there's a bracket, remove everything from that point onwards
    If bracketPos > 0 Then
        cleanName = Trim(Left(cleanName, bracketPos - 1))
    End If
    
    CleanKonzulensName = cleanName
End Function