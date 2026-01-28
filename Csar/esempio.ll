; ModuleID = "csar_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"scribe_int"(i32 %".1")

declare void @"scribe_char"(i8 %".1")

define i32 @"fattoriale"(i32 %"n")
{
entry:
  %"n.1" = alloca i32
  store i32 %"n", i32* %"n.1"
  %"n.2" = load i32, i32* %"n.1"
  %"cmptmp" = icmp eq i32 %"n.2", 0
  br i1 %"cmptmp", label %"then", label %"else"
then:
  ret i32 1
else:
  %"n.3" = load i32, i32* %"n.1"
  %"n.4" = load i32, i32* %"n.1"
  %"subtmp" = sub i32 %"n.4", 1
  %"calltmp" = call i32 @"fattoriale"(i32 %"subtmp")
  %"multmp" = mul i32 %"n.3", %"calltmp"
  ret i32 %"multmp"
endif:
  ret i32 0
}

define i32 @"main"()
{
entry:
  %"num" = alloca i32
  store i32 5, i32* %"num"
  %"risultato" = alloca i32
  store i32 0, i32* %"risultato"
  %"num.1" = load i32, i32* %"num"
  %"calltmp" = call i32 @"fattoriale"(i32 %"num.1")
  store i32 %"calltmp", i32* %"risultato"
  call void @"scribe_char"(i8 82)
  call void @"scribe_char"(i8 61)
  %"risultato.1" = load i32, i32* %"risultato"
  call void @"scribe_int"(i32 %"risultato.1")
  ret i32 0
}
