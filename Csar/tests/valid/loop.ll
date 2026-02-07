; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

declare void @scribe_int(i32) local_unnamed_addr

define i32 @main() local_unnamed_addr {
entry:
  tail call void @scribe_int(i32 5)
  tail call void @scribe_int(i32 4)
  tail call void @scribe_int(i32 3)
  tail call void @scribe_int(i32 2)
  tail call void @scribe_int(i32 1)
  tail call void @scribe_int(i32 0)
  ret i32 0
}
