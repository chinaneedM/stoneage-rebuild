# R52 architectural qualification sources

These processor references qualify architectural effects of already authenticated numeric instruction shapes. They are not evidence for StoneAge's runtime input values, historical save format or processor algorithm.

- [Intel 64 and IA-32 SDM Volume 1](https://www.intel.com/content/dam/support/us/en/documents/processors/pentium4/sb/25366521.pdf), section7.3.1.6, printed page7-10 (PDF page190): CDQ extends the EAX sign into EDX. The EAX input remains the low half of the signed dividend. This supports a separate architectural EDX-write/EAX-preservation overlay; the original decoder's EAX/EDX write observations remain unchanged.
- [Intel SDM Volume 2A](https://cdrdv2-public.intel.com/789581/325383-sdm-vol-2abcd.pdf), IDIV entry, Table3-51, printed page3-498: for the32-bit divisor form, the dividend is EDX:EAX, quotient register EAX and remainder register EDX. Register and memory divisor operands remain distinct. No original quotient, remainder, divisor value or successful division is calculated or assumed.

Retrieved2026-10-15. The full Volume2 PDF exceeds the browser fetch bound; its indexed Intel instruction table supplies the register-role reference. Volume1 was opened and its conversion section read directly. No manual payload is copied into the repository. The qualification is limited to operandless CDQ with EAX read and expected EDX or EAX/EDX decoder writes, within the pinned32-bit client context; CWD/CQO or unexpected register effects are not silently qualified.
