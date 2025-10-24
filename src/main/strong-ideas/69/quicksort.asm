; Здесь должен быть алгоритм для quicksort, но не успел его отладить (падаю с Segmentation Fault :) ). Здесь представлены только io-операции.
default rel
        global  main
        extern  printf
        extern  scanf

section .rodata
in_size:        db "%ld", 0
in:             db "%ld", 0
in_size_prompt: db "Enter array size: ", 0
in_prompt:      db "Enter element %ld: ", 0
out_prompt:     db "arr[%ld] = %ld", 10, 0

section .bss
n:      resq 1
arr:    resq 100

section .text
main:
    sub rsp, 8
    lea rdi, [rel in_size_prompt]
    xor eax, eax
    call printf
    add rsp, 8

    sub rsp, 8
    lea rdi, [rel in_size]
    lea rsi, [rel n]
    xor eax, eax
    call scanf
    add rsp, 8

    mov rbx, [rel n]
    cmp rbx, 0
    jle .done

    xor r12, r12

.read_loop:
    cmp r12, rbx
    jge .done

    sub rsp, 8
    lea rdi, [rel in_prompt]
    mov rsi, r12
    xor eax, eax
    call printf
    add rsp, 8

    mov rdx, r12
    imul rdx, 8

    sub rsp, 8
    lea rdi, [rel in]
    lea rsi, [rel arr + rdx]
    xor eax, eax
    call scanf
    add rsp, 8

    inc r12
    jmp .read_loop

.print_loop:
    xor r12, r12

.print_next:
    cmp r12, rbx
    jge .done

    mov rdx, r12
    imul rdx, 8
    mov rax, [rel arr + rdx]

    sub rsp, 8
    lea rdi, [rel out_prompt]
    mov rsi, r12
    mov rdx, rax
    xor eax, eax
    call printf
    add rsp, 8

    inc r12
    jmp .print_next

.done:
    xor eax, eax
    ret