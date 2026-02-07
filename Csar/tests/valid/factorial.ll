; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

declare void @scribe_int(i32) local_unnamed_addr

define i32 @main() local_unnamed_addr {
entry:
  tail call void @scribe_int(i32 205)
  ret i32 0
}
