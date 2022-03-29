[Code]
// This Script was referred from https://stackoverflow.com/a/56912589/12318454


var
  ProgressPage: TOutputProgressWizardPage;
  ProgressListBox: TNewListBox; // list box containing logs saved in a temp file
  ProgressFileName: string;



function SetTimer(
  Wnd: LongWord; IDEvent, Elapse: LongWord; TimerFunc: LongWord): LongWord;
  external 'SetTimer@user32.dll stdcall';


function KillTimer(hWnd: LongWord; uIDEvent: LongWord): BOOL;
  external 'KillTimer@user32.dll stdcall';


// does something i guess like converting to Buffer to AnsiString
function BufferToAnsi(const Buffer: string): AnsiString;

var

  W: Word;
  I: Integer;

begin

  SetLength(Result, Length(Buffer) * 2);

  for I := 1 to Length(Buffer) do
  
  begin
    W := Ord(Buffer[I]);
    Result[(I * 2)] := Chr(W shr 8); { high byte }
    Result[(I * 2) - 1] := Chr(Byte(W)); { low byte }
  end;

end;



procedure UpdateProgress;

var
  S: AnsiString;
  I, L, Max: Integer;
  Buffer: string;
  Stream: TFileStream;
  Lines: TStringList;

begin

  if not FileExists(ProgressFileName) then
    begin
      Log(Format('Progress file %s does not exist', [ProgressFileName]));
    end

  else
    begin

      try
        { Need shared read as the output file is locked for writting, }
        { so we cannot use LoadStringFromFile }
        Stream := TFileStream.Create(ProgressFileName, fmOpenRead or fmShareDenyNone);

        try
          L := Stream.Size;
          Max := 100*2014;

          if L > Max then
            begin
              Stream.Position := L - Max;
              L := Max;
            end;

          SetLength(Buffer, (L div 2) + (L mod 2));
          Stream.ReadBuffer(Buffer, L);
          S := BufferToAnsi(Buffer);

        finally
          Stream.Free;

        end;

      except
        Log(Format('Failed to read progress from file %s - %s', [
                   ProgressFileName, GetExceptionMessage]));

      end;

    end;

  if S <> '' then

  begin

    Log('Progress len = ' + IntToStr(Length(S)));
    Lines := TStringList.Create();
    Lines.Text := S;

    for I := 0 to Lines.Count - 1 do
    begin

      if I < ProgressListBox.Items.Count then
      begin
        ProgressListBox.Items[I] := Lines[I];
      end
        else
      begin
        ProgressListBox.Items.Add(Lines[I]);
      end

    end;

    ProgressListBox.ItemIndex := ProgressListBox.Items.Count - 1;
    ProgressListBox.Selected[ProgressListBox.ItemIndex] := False;
    Lines.Free;

  end;

  { Just to pump a Windows message queue (maybe not be needed) }
  // ProgressPage.SetProgress(0, 1);

end;



procedure UpdateProgressProc(
  H: LongWord; Msg: LongWord; Event: LongWord; Time: LongWord);
begin
  UpdateProgress;
end;


procedure SetUpThingsFromPowerShell(Sender: TObject);
var
  ResultCode: Integer;
  Timer: LongWord;
  AppPath: string;
  AppError: string;
  Command: string;
begin
   ProgressPage :=
    CreateOutputProgressPage(
      'Installing something', 'Please wait until this finishes...');
  ProgressPage.Show();
  ProgressListBox := TNewListBox.Create(WizardForm);
  ProgressListBox.Parent := ProgressPage.Surface;
  ProgressListBox.Top := 0;
  ProgressListBox.Left := 0;
  ProgressListBox.Width := ProgressPage.SurfaceWidth;
  ProgressListBox.Height := ProgressPage.SurfaceHeight;

  { Fake SetProgress call in UpdateProgressProc will show it, }
  { make sure that user won't see it }
  
  ProgressPage.ProgressBar.Top := -100;

  try
    Timer := SetTimer(0, 0, 250, CreateCallback(@UpdateProgressProc));

    AppPath := ExpandConstant('{app}\setup.ps1');
    ProgressFileName := ExpandConstant('{app}\logs.txt');  
  

    SaveStringToFile(ProgressFileName,'', False); // replacing to "" null string
    Log(Format('Expecting progress in %s', [ProgressFileName]));

    Command := Format('"%s" >> "%s"', [AppPath, ProgressFileName]);
    MsgBox(Command, mbInformation, MB_OK);

    if not ShellExec('', ExpandConstant('{cmd}'), '/c powershell -ExecutionPolicy ByPass -file ' + Command, ExpandConstant('{app}'), SW_HIDE,
         ewWaitUntilTerminated, ResultCode) then

    begin  
      AppError := 'Cannot start app';
    end
      else

    if ResultCode <> 0 then
    begin
      AppError := Format('App failed with code %d', [ResultCode]);
    end;
    UpdateProgress;

  finally
    { Clean up }
    KillTimer(0, Timer);
    ProgressPage.Hide;
    DeleteFile(ProgressFileName);
    ProgressPage.Free();

  end;

  if AppError <> '' then
  begin 
    { RaiseException does not work properly while TOutputProgressWizardPage is shown }
    RaiseException(AppError);
  end;
end;


// Here is were we execute setup.ps1
function SetThingsUp(): Boolean;
begin 
  Result := True
  
  if not Downloaded then begin
    SetUpThingsFromPowerShell(nil);
  end;
end;