Option Explicit

' Main subroutine to count email responses
Sub CountEmailResponses()
    Dim externalWs As Worksheet
    Dim partnerWs As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim conversationID As String
    Dim direction As String
    Dim recipients As String
    Dim responseCount As Long
    
    ' Get the ExternalEmails worksheet
    Set externalWs = ActiveWorkbook.Worksheets("ExternalEmails")
    
    ' Get the PartnerEmails worksheet
    On Error Resume Next
    Set partnerWs = ActiveWorkbook.Worksheets("PartnerEmails")
    On Error GoTo 0
    
    If partnerWs Is Nothing Then
        MsgBox "PartnerEmails worksheet not found. Please run the Outlook macro first.", vbExclamation, "Missing Worksheet"
        Exit Sub
    End If
    
    ' Find the last row with data in ExternalEmails
    lastRow = externalWs.Cells(externalWs.Rows.Count, 1).End(xlUp).Row
    
    If lastRow < 2 Then
        MsgBox "No data found in the ExternalEmails worksheet.", vbExclamation, "No Data"
        Exit Sub
    End If
    
    ' Add ResponseEmailCount header if column G is empty
    If externalWs.Cells(1, 7).Value = "" Then
        externalWs.Cells(1, 7).Value = "ResponseEmailCount"
        externalWs.Cells(1, 7).Font.Bold = True
        externalWs.Cells(1, 7).Interior.Color = RGB(200, 200, 200)
    End If
    
    ' Process each row
    ' Column layout: A=Sender, B=Recipients, C=Subject, D=Date, E=ConversationID, F=Direction, G=ResponseEmailCount
    For i = 2 To lastRow
        direction = Trim(externalWs.Cells(i, 6).Value) ' Direction column (F)
        conversationID = Trim(externalWs.Cells(i, 5).Value) ' Conversation ID column (E)
        recipients = Trim(externalWs.Cells(i, 2).Value) ' Recipients column (B)
        
        ' Only count responses for sent emails with valid partners
        If LCase(direction) = "sent" Then
            If conversationID <> "" And HasValidPartners(recipients, partnerWs) Then
                responseCount = CountResponsesForConversation(externalWs, conversationID, lastRow)
                externalWs.Cells(i, 7).Value = responseCount ' ResponseEmailCount column (G)
            Else
                externalWs.Cells(i, 7).Value = 0 ' No conversation ID or no valid partners = no responses
            End If
        Else
            externalWs.Cells(i, 7).Value = "" ' Clear field for received emails
        End If
    Next i
    
    ' Format the ResponseEmailCount column
    FormatResponseColumn externalWs, 7, lastRow
    
    MsgBox "Response counting completed! The 'ResponseEmailCount' column has been updated.", vbInformation, "Process Complete"
End Sub

' Check if the recipients string contains any valid partners (Is EDIH partner = 1)
Function HasValidPartners(recipients As String, partnerWs As Worksheet) As Boolean
    Dim recipientArray As Variant
    Dim i As Integer
    Dim j As Long
    Dim emailAddress As String
    Dim partnerLastRow As Long
    
    HasValidPartners = False
    
    If recipients = "" Then Exit Function
    
    ' Get last row in partner worksheet
    partnerLastRow = partnerWs.Cells(partnerWs.Rows.Count, 1).End(xlUp).Row
    
    If partnerLastRow < 2 Then Exit Function
    
    ' Split recipients by semicolon
    recipientArray = Split(recipients, ";")
    
    ' Check each recipient
    For i = LBound(recipientArray) To UBound(recipientArray)
        emailAddress = Trim(recipientArray(i))
        
        ' Check if this email is in the partner list with "Is EDIH partner" = 1
        For j = 2 To partnerLastRow
            If LCase(Trim(partnerWs.Cells(j, 1).Value)) = LCase(emailAddress) Then
                If partnerWs.Cells(j, 2).Value = 1 Then
                    HasValidPartners = True
                    Exit Function
                End If
            End If
        Next j
    Next i
End Function

' Count responses for a specific conversation ID
Function CountResponsesForConversation(ws As Worksheet, targetConversationID As String, lastRow As Long) As Long
    Dim i As Long
    Dim currentConversationID As String
    Dim currentDirection As String
    Dim responseCount As Long
    
    responseCount = 0
    
    ' Loop through all rows to find matching conversation IDs
    For i = 2 To lastRow
        currentConversationID = Trim(ws.Cells(i, 5).Value) ' Conversation ID column (E)
        currentDirection = Trim(ws.Cells(i, 6).Value) ' Direction column (F)
        
        ' Count if it's the same conversation ID and it's a received email
        If currentConversationID = targetConversationID And LCase(currentDirection) = "received" Then
            responseCount = responseCount + 1
        End If
    Next i
    
    CountResponsesForConversation = responseCount
End Function

' Format the ResponseEmailCount column
Sub FormatResponseColumn(ws As Worksheet, responseCol As Integer, lastRow As Long)
    Dim responseRange As Range
    
    ' Set range for the ResponseEmailCount column (excluding header)
    Set responseRange = ws.Range(ws.Cells(2, responseCol), ws.Cells(lastRow, responseCol))
    
    ' Format as numbers, center aligned
    With responseRange
        .NumberFormat = "0"
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
    End With
    
    ' Auto-fit the column
    ws.Columns(responseCol).AutoFit
    
    ' Add conditional formatting to highlight emails with responses
    With responseRange
        .FormatConditions.Delete ' Clear existing conditional formatting
        
        ' Highlight cells with value > 0 in light green
        With .FormatConditions.Add(Type:=xlCellValue, Operator:=xlGreater, Formula1:="0")
            .Interior.Color = RGB(198, 239, 206) ' Light green
            .Font.Color = RGB(0, 97, 0) ' Dark green text
        End With
        
        ' Highlight cells with value = 0 in light red
        With .FormatConditions.Add(Type:=xlCellValue, Operator:=xlEqual, Formula1:="0")
            .Interior.Color = RGB(255, 199, 206) ' Light red
            .Font.Color = RGB(156, 0, 6) ' Dark red text
        End With
    End With
End Sub

' Helper function to create summary statistics
Sub CreateSummaryStatistics()
    Dim externalWs As Worksheet
    Dim lastRow As Long
    Dim totalSentEmails As Long
    Dim emailsWithResponses As Long
    Dim totalResponses As Long
    Dim conversionRate As Double
    Dim summaryRow As Long
    Dim i As Long
    Dim direction As String
    Dim responseCount As Long
    
    Set externalWs = ActiveWorkbook.Worksheets("ExternalEmails")
    lastRow = externalWs.Cells(externalWs.Rows.Count, 1).End(xlUp).Row
    
    ' Calculate statistics
    For i = 2 To lastRow
        direction = Trim(externalWs.Cells(i, 6).Value) ' Direction column (F)
        If LCase(direction) = "sent" Then
            totalSentEmails = totalSentEmails + 1
            responseCount = externalWs.Cells(i, 7).Value ' ResponseEmailCount column (G)
            If responseCount > 0 Then
                emailsWithResponses = emailsWithResponses + 1
                totalResponses = totalResponses + responseCount
            End If
        End If
    Next i
    
    ' Calculate conversion rate
    If totalSentEmails > 0 Then
        conversionRate = (emailsWithResponses / totalSentEmails) * 100
    Else
        conversionRate = 0
    End If
    
    ' Add summary section
    summaryRow = lastRow + 3
    
    externalWs.Cells(summaryRow, 1).Value = "SUMMARY STATISTICS"
    externalWs.Cells(summaryRow, 1).Font.Bold = True
    externalWs.Cells(summaryRow, 1).Font.Size = 12
    
    externalWs.Cells(summaryRow + 1, 1).Value = "Total Sent Emails:"
    externalWs.Cells(summaryRow + 1, 2).Value = totalSentEmails
    
    externalWs.Cells(summaryRow + 2, 1).Value = "Emails with Responses:"
    externalWs.Cells(summaryRow + 2, 2).Value = emailsWithResponses
    
    externalWs.Cells(summaryRow + 3, 1).Value = "Total Responses Received:"
    externalWs.Cells(summaryRow + 3, 2).Value = totalResponses
    
    externalWs.Cells(summaryRow + 4, 1).Value = "Conversion Rate:"
    externalWs.Cells(summaryRow + 4, 2).Value = Format(conversionRate, "0.00") & "%"
    
    ' Format summary section
    With externalWs.Range("A" & (summaryRow + 1) & ":B" & (summaryRow + 4))
        .Font.Bold = True
        .Borders.LineStyle = xlContinuous
        .Borders.Weight = xlThin
    End With
    
    MsgBox "Summary statistics have been added to the worksheet." & vbCrLf & vbCrLf & _
           "Total Sent Emails: " & totalSentEmails & vbCrLf & _
           "Emails with Responses: " & emailsWithResponses & vbCrLf & _
           "Total Responses: " & totalResponses & vbCrLf & _
           "Conversion Rate: " & Format(conversionRate, "0.00") & "%", _
           vbInformation, "Summary Statistics"
End Sub