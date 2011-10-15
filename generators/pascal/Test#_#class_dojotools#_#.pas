program Test#_#class_dojotools#_#;
uses TestUnit, #_#class_dojotools#_#Unit;

procedure Test#_#class_dojotools#_#;
begin
  InitTest('#_#class_dojotools#_# de 1 deve retornar -1'); 
  Assert(#_#class_dojotools#_#(1) = -1);
end;

begin
  StartTests;
  TestCase('#_#class_dojotools#_#', @Test#_#class_dojotools#_#);		  
  EndTests;
end.
