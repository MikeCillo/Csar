; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

declare void @print_int(i32) local_unnamed_addr

define i32 @main() local_unnamed_addr {
entry:
  tail call void @print_int(i32 205)
  ret i32 0
}
