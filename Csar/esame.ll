; ModuleID = "csar_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"scribe_int"(i32 %".1")

declare void @"scribe_char"(i8 %".1")

declare i32 @"legge_int"()

declare i8 @"legge_char"()

define i32 @"somma"(i32 %"a", i32 %"b")
{
entry:
  %"a.1" = alloca i32
  store i32 %"a", i32* %"a.1"
  %"b.1" = alloca i32
  store i32 %"b", i32* %"b.1"
  %"a.2" = load i32, i32* %"a.1"
  %"b.2" = load i32, i32* %"b.1"
  %"addtmp" = add i32 %"a.2", %"b.2"
  ret i32 %"addtmp"
}

define i32 @"moltiplica"(i32 %"a", i32 %"b")
{
entry:
  %"a.1" = alloca i32
  store i32 %"a", i32* %"a.1"
  %"b.1" = alloca i32
  store i32 %"b", i32* %"b.1"
  %"a.2" = load i32, i32* %"a.1"
  %"b.2" = load i32, i32* %"b.1"
  %"multmp" = mul i32 %"a.2", %"b.2"
  ret i32 %"multmp"
}

define i32 @"divisione_sicura"(i32 %"a", i32 %"b")
{
entry:
  %"a.1" = alloca i32
  store i32 %"a", i32* %"a.1"
  %"b.1" = alloca i32
  store i32 %"b", i32* %"b.1"
  %"b.2" = load i32, i32* %"b.1"
  %"cmptmp" = icmp eq i32 %"b.2", 0
  br i1 %"cmptmp", label %"then", label %"else"
then:
  call void @"scribe_char"(i8 33)
  ret i32 0
else:
  %"a.2" = load i32, i32* %"a.1"
  %"b.3" = load i32, i32* %"b.1"
  %"divtmp" = sdiv i32 %"a.2", %"b.3"
  ret i32 %"divtmp"
endif:
  ret i32 0
}

define i32 @"main"()
{
entry:
  %"scelta" = alloca i8
  store i8 32, i8* %"scelta"
  %"op1" = alloca i32
  store i32 0, i32* %"op1"
  %"op2" = alloca i32
  store i32 0, i32* %"op2"
  %"ris" = alloca i32
  store i32 0, i32* %"ris"
  %"continua" = alloca i1
  store i1 1, i1* %"continua"
  br label %"while_cond"
while_cond:
  %"continua.1" = load i1, i1* %"continua"
  br i1 %"continua.1", label %"while_body", label %"while_end"
while_body:
  call void @"scribe_char"(i8 63)
  %"calltmp" = call i8 @"legge_char"()
  store i8 %"calltmp", i8* %"scelta"
  %"scelta.1" = load i8, i8* %"scelta"
  %"cmptmp" = icmp eq i8 %"scelta.1", 113
  br i1 %"cmptmp", label %"then", label %"else"
while_end:
  ret i32 0
then:
  store i1 0, i1* %"continua"
  br label %"endif"
else:
  call void @"scribe_char"(i8 65)
  %"calltmp.1" = call i32 @"legge_int"()
  store i32 %"calltmp.1", i32* %"op1"
  call void @"scribe_char"(i8 66)
  %"calltmp.2" = call i32 @"legge_int"()
  store i32 %"calltmp.2", i32* %"op2"
  %"scelta.2" = load i8, i8* %"scelta"
  %"cmptmp.1" = icmp eq i8 %"scelta.2", 43
  br i1 %"cmptmp.1", label %"then.1", label %"else.1"
endif:
  br label %"while_cond"
then.1:
  %"op1.1" = load i32, i32* %"op1"
  %"op2.1" = load i32, i32* %"op2"
  %"calltmp.3" = call i32 @"somma"(i32 %"op1.1", i32 %"op2.1")
  store i32 %"calltmp.3", i32* %"ris"
  br label %"endif.1"
else.1:
  %"scelta.3" = load i8, i8* %"scelta"
  %"cmptmp.2" = icmp eq i8 %"scelta.3", 42
  br i1 %"cmptmp.2", label %"then.2", label %"else.2"
endif.1:
  call void @"scribe_char"(i8 61)
  %"ris.1" = load i32, i32* %"ris"
  call void @"scribe_int"(i32 %"ris.1")
  br label %"endif"
then.2:
  %"op1.2" = load i32, i32* %"op1"
  %"op2.2" = load i32, i32* %"op2"
  %"calltmp.4" = call i32 @"moltiplica"(i32 %"op1.2", i32 %"op2.2")
  store i32 %"calltmp.4", i32* %"ris"
  br label %"endif.2"
else.2:
  %"scelta.4" = load i8, i8* %"scelta"
  %"cmptmp.3" = icmp eq i8 %"scelta.4", 45
  br i1 %"cmptmp.3", label %"then.3", label %"else.3"
endif.2:
  br label %"endif.1"
then.3:
  %"op1.3" = load i32, i32* %"op1"
  %"op2.3" = load i32, i32* %"op2"
  %"subtmp" = sub i32 %"op1.3", %"op2.3"
  store i32 %"subtmp", i32* %"ris"
  br label %"endif.3"
else.3:
  %"scelta.5" = load i8, i8* %"scelta"
  %"cmptmp.4" = icmp eq i8 %"scelta.5", 47
  br i1 %"cmptmp.4", label %"then.4", label %"else.4"
endif.3:
  br label %"endif.2"
then.4:
  %"op1.4" = load i32, i32* %"op1"
  %"op2.4" = load i32, i32* %"op2"
  %"calltmp.5" = call i32 @"divisione_sicura"(i32 %"op1.4", i32 %"op2.4")
  store i32 %"calltmp.5", i32* %"ris"
  br label %"endif.4"
else.4:
  store i32 0, i32* %"ris"
  br label %"endif.4"
endif.4:
  br label %"endif.3"
}
