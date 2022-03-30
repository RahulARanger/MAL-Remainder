[Code]

var       
  DownloadPage: TDownloadWizardPage;  // downloads packages

  Ask: Boolean;   // Ask is Flag for like, say we click Click button to exit setup
  // Ask = true for asking confirmation else False [we set False if we need to exit by force]

  ImplicitExitCode: Integer; // like this has ability to dected implicit closes of powershell scripts


  // handles progress for the Download Page 
function OnDownloadProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  if Progress = ProgressMax then
    Log(Format('Successfully downloaded file to {tmp}: %s', [FileName]));
  Result := True;
end;



procedure CloseSetup(CancelMsg: String);
begin 
  if Length(CancelMsg) > 0 then 
    MsgBox(CancelMsg, mbCriticalError, MB_OK);
  
  Ask := False;
  WizardForm.Close();
end;


// Checks for the Python Directory, if found it says Downloaded else it downloads it
function CheckAndDownloadPython(): String;
var
Downloaded: Boolean;

begin
    Downloaded := DirExists(ExpandConstant('{app}/python'));
    Result := '';

    if not Downloaded then
    begin
    
      DownloadPage.Clear;
      
      DownloadPage.Add('https://www.python.org/ftp/python/3.8.9/python-3.8.9-embed-amd64.zip', 'python.zip', '');
      DownloadPage.Add('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py', '');
      DownloadPage.Show;
    
      try
        
        DownloadPage.Download;
        DownloadPage.Hide;
      except 
        Result := AddPeriod(GetExceptionMessage);

      finally
        DownloadPage.Hide;

  end;
    
    end;

end;

procedure PostInstall;

var 
  ResultCode: Integer;
  ResultString: String;
  PythonPath: String;

begin
    WizardForm.Hide;
    
    repeat
    
      if not ShellExec(
      '','powershell', 
      ExpandConstant('-ExecutionPolicy ByPass -file "{app}/setup.ps1"'),
       ExpandConstant('{app}'),
        SW_SHOW,
         ewWaitUntilTerminated,
          ResultCode
      ) then
      
       ResultString := 'It seems we can''t run setup.ps1, maybe that file was not installed! anyways please raise the issue in the repo!';
      
      if ResultCode = ImplicitExitCode then
        begin
          if MsgBox('While in Verbose Mode, Powershell script is not silent and it sets things up. Since you have interprutted it, Do you want to cancel the installation ?', mbError, MB_YESNO) = IDYES then 
            begin 
              ResultCode := -1
              ResultString := 'Closed as requested'
            end;
        end
      else if ResultCode <> 0 then 
        ResultString := 'Setup Script didn''t return the favorable result. Maybe there was some unexpected error, which shouldn''t have happended causally. Please raise this issue in the repo';
 
    until ResultCode <> ImplicitExitCode

    WizardForm.Show;

    if ResultCode <> 0 then
      begin 
        PythonPath := ExpandConstant('{app}/python');

        if DirExists(PythonPath) then
          DelTree(PythonPath, True, True, True); // deleting everything that setup  did if failed
        
        CloseSetup(ResultString);
      end;
end;

function CheckAndQuit: Integer;
var
Script: String;

begin
    Script := ExpandConstant('{app}/gate.ps1');

    if FileExists(Script) then
    begin 
    
      ShellExec(
        '','powershell', 
        Format('-ExecutionPolicy ByPass -File "%s" -Mode 0', [Script]),
         ExpandConstant('{app}'),
          SW_HIDE,
           ewWaitUntilTerminated,
            Result
      );
      MsgBox(IntToStr(Result), mbInformation, MB_OK);

     
    end;
end;