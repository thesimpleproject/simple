jmp.32 @_kstart

.label msg
.str "SimpleOS booting..."

.label _kstart
ldc.a.8 1
dma.port ra

ldaddr a @msg
dma.addr ra

ldc.a.8 19
dma.len ra

dma.write.sync
