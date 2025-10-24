; find value in Fibonacci sequence
default rel
        global  main
        extern  printf
        extern  scanf

section .rodata
in:             db "%ld", 0
out:            db "Fibonacci sequence element with number=%ld is %ld", 10, 0
illegal_out:    db "Can't find Fibonacci sequence element with number=%ld", 10, 0
prompt:         db "Enter Fibonacci sequence element number: ", 0

section .bss
n:          resq 1

section .text
main:
        sub     rsp, 8
        lea     rdi, [rel prompt]
        xor     eax, eax
        call    printf
        add     rsp, 8

        sub     rsp, 8
        lea     rdi, [rel in]
        lea     rsi, [rel n]
        xor     eax, eax
        call    scanf
        add     rsp, 8

        mov     rbx, [rel n]    ; rbx = n
        cmp     rbx, 1
        jl      .some_illegal

        cmp     rbx, 2
        mov     rax, 1          ; rax = 1
        jle     .some_legal

        mov     rcx, rbx
        dec     rcx             ; rcx = rcx - 1
        dec     rcx             ; rcx = rcx - 1
        mov     rdx, rax        ; rdx = rax

.while:
        cmp     rcx, 0
        je     .some_legal

        dec     rcx
        mov     r10, rax        ; r10 = rax
        add     rax, rdx        ; rax = rax + rdx
        mov     rdx, r10        ; rdx = r10
        jmp     .while

.some_legal:
        sub     rsp, 8
        lea     rdi, [rel out]
        mov     rsi, rbx
        mov     rdx, rax
        xor     eax, eax
        call    printf
        add     rsp, 8

        xor     eax, eax
        ret

.some_illegal:
        sub     rsp, 8
        lea     rdi, [rel illegal_out]
        mov     rsi, rbx
        xor     eax, eax
        call    printf
        add     rsp, 8

        xor     eax, eax
        ret