; sum numbers from 1 to entered N
        default rel
        global  main
        extern  printf
        extern  scanf

section .rodata
fmt_in:     db "%ld", 0
fmt_out:    db "Sum(1..%ld) = %ld", 10, 0
prompt:     db "Enter N: ", 0

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
        lea     rdi, [rel fmt_in]
        lea     rsi, [rel n]
        xor     eax, eax
        call    scanf
        add     rsp, 8

        mov     rbx, [rel n]      ; rbx = n
        mov     rax, rbx          ; rax = n
        test    rax, 1            ; is odd?
        jnz     .odd

        ; for even do (n/2)*(n+1)
        mov     rcx, rbx          ; rcx = n
        shr     rcx, 1            ; rcx = n/2
        mov     rdx, rbx          ; rdx = n
        inc     rdx               ; rdx = n+1
        mov     rax, rcx          ; rax = n/2
        imul    rax, rdx          ; rax = (n/2)*(n+1)
        jmp     .have_sum

.odd:
        ; for odd do n*((n+1)/2)
        mov     rdx, rbx          ; rdx = n
        inc     rdx               ; rdx = n+1
        shr     rdx, 1            ; rdx = (n+1)/2
        imul    rax, rdx          ; rax = n*((n+1)/2)

.have_sum:
        sub     rsp, 8
        lea     rdi, [rel fmt_out]
        mov     rsi, rbx
        mov     rdx, rax
        xor     eax, eax
        call    printf
        add     rsp, 8

        xor     eax, eax
        ret