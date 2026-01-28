import llvmlite.binding as llvm

def optimize_ir(ir_code_str):
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    mod = llvm.parse_assembly(ir_code_str)
    mod.verify()

    pm_builder = llvm.create_pass_manager_builder()
    pm_builder.opt_level = 3  # Livello massimo!
    pm_builder.inlining_threshold = 100

    pass_manager = llvm.create_module_pass_manager()
    pm_builder.populate(pass_manager)

    pass_manager.run(mod)
    return str(mod)