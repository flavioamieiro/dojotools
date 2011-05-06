program Test#*class_dojotools*#;
uses TestUnit, #*class_dojotools*#Unit;

procedure Test#*class_dojotools*#;
begin
  InitTest('#*class_dojotools*# de 1 deve retornar -1'); 
  Assert(#*class_dojotools*#(1) = -1);
end;

begin
  StartTests;
  TestCase('#*class_dojotools*#', @Test#*class_dojotools*#);		  
  EndTests;
end.
