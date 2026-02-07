; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

declare void @scribe_char(i8) local_unnamed_addr

define i32 @main() local_unnamed_addr {
entry:
  tail call void @scribe_char(i8 79)
  tail call void @scribe_char(i8 75)
  ret i32 0
}
