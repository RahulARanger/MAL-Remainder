[Code]

var       
  DownloadPage: TDownloadWizardPage;  // downloads packages
   SettingThingsUp: TOutputMarqueeProgressWizardPage; // loading ===== progress bar 

  Downloaded: Boolean; // downloaded python or not 
  EC: Integer;   // temp for Error Code
  Prefix: String; // prefix for powershell script params
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
ResultCode: Integer;
TempResult: Boolean;

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
        SettingThingsUp.Show;

        
        ExtractTemporaryFile('setup.ps1')

        if not ShellExec('', ExpandConstant('{cmd}'), ExpandConstant('/c powershell -ExecutionPolicy ByPass -file "{tmp}/setup.ps1"'), ExpandConstant('{app}'), SW_SHOW,
         ewWaitUntilTerminated, ResultCode) then
         Result := 'It seems we can''t run setup.ps1, please raise this issue in the repo';
    
        if ResultCode = ImplicitExitCode then
          Result := 'It seems you have closed the shell script, which is necessary for setup!'
        
        else if ResultCode <> 0 then 
          Result := 'Setup Script didn''t return the favorable result. Maybe there was some unexpected error, which shouldn''t have happended causally. Please raise this issue in the repo';

      except 

        Result := AddPeriod(GetExceptionMessage);

      finally

        DownloadPage.Hide;
        SettingThingsUp.Hide;

      end;                            
    
    end;

end;

