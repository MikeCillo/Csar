; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

declare void @scribe_int(i32) local_unnamed_addr

declare i32 @legge_int() local_unnamed_addr

define i32 @main() local_unnamed_addr {
entry:
  %calltmp = tail call i32 @legge_int()
  %multmp = shl i32 %calltmp, 1
  tail call void @scribe_int(i32 %multmp)
  ret i32 0
}
