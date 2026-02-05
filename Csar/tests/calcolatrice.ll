; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

declare void @scribe_int(i32) local_unnamed_addr

declare i32 @legge_int() local_unnamed_addr

declare void @scribe_menu() local_unnamed_addr

declare void @chiede_int() local_unnamed_addr

declare void @annuncia_res() local_unnamed_addr

; Function Attrs: mustprogress nofree norecurse nosync nounwind readnone willreturn
define i32 @calcola(i32 %op, i32 %a, i32 %b) local_unnamed_addr #0 {
entry:
  switch i32 %op, label %common.ret [
    i32 1, label %then
    i32 2, label %then.1
    i32 3, label %then.2
    i32 4, label %then.3
  ]

common.ret:                                       ; preds = %then.3, %entry, %else.4, %then.2, %then.1, %then
  %common.ret.op = phi i32 [ %addtmp, %then ], [ %subtmp, %then.1 ], [ %multmp, %then.2 ], [ %divtmp, %else.4 ], [ 0, %entry ], [ 0, %then.3 ]
  ret i32 %common.ret.op

then:                                             ; preds = %entry
  %addtmp = add i32 %b, %a
  br label %common.ret

then.1:                                           ; preds = %entry
  %subtmp = sub i32 %a, %b
  br label %common.ret

then.2:                                           ; preds = %entry
  %multmp = mul i32 %b, %a
  br label %common.ret

then.3:                                           ; preds = %entry
  %cmptmp.4 = icmp eq i32 %b, 0
  br i1 %cmptmp.4, label %common.ret, label %else.4

else.4:                                           ; preds = %then.3
  %divtmp = sdiv i32 %a, %b
  br label %common.ret
}

define i32 @main() local_unnamed_addr {
entry:
  tail call void @scribe_menu()
  %calltmp2 = tail call i32 @legge_int()
  %cmptmp3 = icmp eq i32 %calltmp2, 0
  br i1 %cmptmp3, label %while_end, label %else

while_end:                                        ; preds = %while_body.backedge, %entry
  ret i32 0

else:                                             ; preds = %entry, %while_body.backedge
  %calltmp4 = phi i32 [ %calltmp, %while_body.backedge ], [ %calltmp2, %entry ]
  %cmptmp.1 = icmp sgt i32 %calltmp4, 4
  br i1 %cmptmp.1, label %while_body.backedge, label %else.1

else.1:                                           ; preds = %else
  tail call void @chiede_int()
  %calltmp.1 = tail call i32 @legge_int()
  tail call void @chiede_int()
  %calltmp.2 = tail call i32 @legge_int()
  switch i32 %calltmp4, label %calcola.exit [
    i32 1, label %then.i
    i32 2, label %then.1.i
    i32 3, label %then.2.i
    i32 4, label %then.3.i
  ]

then.i:                                           ; preds = %else.1
  %addtmp.i = add i32 %calltmp.2, %calltmp.1
  br label %calcola.exit

then.1.i:                                         ; preds = %else.1
  %subtmp.i = sub i32 %calltmp.1, %calltmp.2
  br label %calcola.exit

then.2.i:                                         ; preds = %else.1
  %multmp.i = mul i32 %calltmp.2, %calltmp.1
  br label %calcola.exit

then.3.i:                                         ; preds = %else.1
  %cmptmp.4.i = icmp eq i32 %calltmp.2, 0
  br i1 %cmptmp.4.i, label %calcola.exit, label %else.4.i

else.4.i:                                         ; preds = %then.3.i
  %divtmp.i = sdiv i32 %calltmp.1, %calltmp.2
  br label %calcola.exit

calcola.exit:                                     ; preds = %else.1, %then.i, %then.1.i, %then.2.i, %then.3.i, %else.4.i
  %common.ret.op.i = phi i32 [ %addtmp.i, %then.i ], [ %subtmp.i, %then.1.i ], [ %multmp.i, %then.2.i ], [ %divtmp.i, %else.4.i ], [ 0, %else.1 ], [ 0, %then.3.i ]
  tail call void @annuncia_res()
  tail call void @scribe_int(i32 %common.ret.op.i)
  br label %while_body.backedge

while_body.backedge:                              ; preds = %calcola.exit, %else
  tail call void @scribe_menu()
  %calltmp = tail call i32 @legge_int()
  %cmptmp = icmp eq i32 %calltmp, 0
  br i1 %cmptmp, label %while_end, label %else
}

attributes #0 = { mustprogress nofree norecurse nosync nounwind readnone willreturn }
