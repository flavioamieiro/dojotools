unit TestUnit;

interface
  Type Tproc = Procedure();  

  procedure StartTests();
  procedure EndTests();
  procedure StartTest(x:string);
  procedure InitTest(str:string);
  function FloatEquals(a:real; b:real):boolean;
  procedure Assert(test:boolean);
  procedure Fail();
  procedure EndTest();
  procedure TestCase(str: string; func: Tproc);
  procedure Pass();
  procedure WriteML(msg: string);



const
  EpsilonDefault : real = 0.0001;

var
  fails : integer = 0;
  tests : integer = 0;
  testfails : integer = 0;
  passes : integer = 0;
  name : string;
  reason : string;
  info : string;
  epsilon : real;
  continueTests : integer = 1;
  failMessages : string;

implementation

procedure TestCase(str: string; func: Tproc); 
begin 
  StartTest(str); 
  func; 
  EndTest;
end;

procedure StartTests();
begin
  fails := 0;
  tests := 0;
  testfails := 0;
  passes := 0;
  name := '';
  reason := '';
  info := ' ';
  epsilon := EpsilonDefault;
  continueTests := 1;
  writeln(info);
end;

procedure EndTests();
begin
  writeln();
  writeln('--- Results ---');
  writeln();
  writeln('Tests run:', tests);	
  writeln('Passes:', passes);
  writeln('Failures:', fails);
  halt(fails);	
end;

procedure StartTest(x: string);
begin
  failMessages := '';
  testfails := 0; 
  writeln('> ', x, ':');
  tests := tests + 1; 
  name := x;  
end;

procedure EndTest();
begin
  WriteML(failMessages);
  writeln('< '+name);
end;

procedure WriteML(msg: string);
var 
  i: integer;
  str: string;
begin
  writeln();
  str := '';
  for i:= 1 to length(msg) do
  begin
    str := str + msg[i];
    if msg[i] = #13 then 
    begin
      writeln(str);
      str:='';
    end;
  end;
end;

procedure InitTest(str: string);
begin
  reason := str;
end;

function FloatEquals(a:real; b:real): boolean;
begin
  FloatEquals := (ABS(a - b) <= epsilon);
end;

procedure Assert(test:boolean);
begin
  if not test then Fail else Pass;
  //reason := '';
  info := ' ';
end;

procedure Fail();
begin
  write('F');
  failMessages := failMessages + '[FAIL] ' + name + ':' + reason + #13;
  inc(fails);
  inc(testfails);
end;

procedure Pass();
begin
  write('.');
  inc(passes);
end;


end.
