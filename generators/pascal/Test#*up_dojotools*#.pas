program Test#*up_dojotools*#;
uses TestUnit, #*up_dojotools*#Unit;

procedure Test#*up_dojotools*#;
begin
  InitTest('#*up_dojotools*# de 1 deve retornar -1'); 
  Assert(#*dojotools*#(1) = -1);
end;

begin
  StartTests;
  TestCase('#*up_dojotools*#', @Test#*up_dojotools*#);		  
  EndTests;
end.
