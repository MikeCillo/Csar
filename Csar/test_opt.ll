; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

declare void @scribe_int(i32) local_unnamed_addr

; Function Attrs: mustprogress nofree norecurse nosync nounwind readnone willreturn
define i32 @calcolo_inutile() local_unnamed_addr #0 {
entry:
  ret i32 30
}

define i32 @main() local_unnamed_addr {
entry:
  tail call void @scribe_int(i32 30)
  ret i32 0
}

attributes #0 = { mustprogress nofree norecurse nosync nounwind readnone willreturn }
