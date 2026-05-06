Category 1: Filesystem & Storage

Q1: What happens to the physical bits of a file on a hard drive when you "delete" it from the trash bin?

A) Every bit is immediately overwritten with a random sequence of 1s and 0s.

B*) The bits remain, but the filesystem marks the space as available for new data.

C) The hardware physically demagnetizes that section of the disk to clear it.

D) I do not know.

Category 2: OS & Processes

Q2: How can a computer with a single-core CPU appear to run dozens of applications at the exact same time?

A) The applications are compressed into tiny segments that fit in the cache together.

B*) The OS rapidly switches the CPU's attention between programs (context switching).

C) Most applications are "paused" and only run when you move the mouse over them.

D) I do not know.

Category 3: Hardware-Software Interface

Q3: Which of the following storage locations is the FASTEST for a CPU to read from?

A) L3 Cache.

B) System RAM.

C*) CPU Registers.

D) I do not know.

Category 4: Network Fundamentals

Q4: If an application is listening on 127.0.0.1:8080, who can connect to it?

A*) Only users/processes on the same physical computer.

B) Anyone on the same Local Area Network (LAN).

C) Anyone on the public internet who knows the IP.

D) I do not know.

Category 5: Build & Runtime

Q5: What is the primary purpose of JIT (Just-In-Time) compilation in the .NET environment?

A) To check the source code for syntax errors while the user is typing.

B) To compress the .dll files so they take up less space on the disk.

C*) To convert Intermediate Language (IL) into native machine code at runtime.

D) I do not know.

Category 6: Git & Versioning

Q6: What is the actual consequence of deleting the hidden .git folder inside your project directory?

A) The project is deleted from GitHub's servers immediately.

B*) The project is no longer a Git repository; all local history and branches are lost.

C) All your source code files (.cs, .html) are permanently deleted.

D) I do not know.

Category 7: Memory Management

Q7: In a 64-bit C# application, what is the size of a reference variable (a "pointer" to an object)?

A) 4 bytes (32 bits).

B*) 8 bytes (64 bits).

C) It depends on the size of the object it points to.

D) I do not know.

Category 8: Threading & Event Loop

Q8: Why does a long-running while(true) loop on the UI Thread make a WinUI window "freeze" and stop responding to clicks?

A*) The UI Thread is busy executing the loop and cannot process the "click" events in the queue.

B) The CPU detects an infinite loop and shuts down the application's graphics.

C) Windows automatically lowers the priority of busy windows to save energy.

D) I do not know.

Category 9: Data Representation

Q9: Why might the expression (0.1 + 0.2 == 0.3) return false in many programming languages?

A) The + operator has a higher priority than the == operator in this context.

B) Computers use base-10 math internally which cannot represent 0.3 exactly.

C*) Floating-point numbers are stored in binary, leading to tiny rounding imprecisions.

D) I do not know.

Category 10: Managed Runtime

Q10: What does it mean for code to be "Managed" in the context of .NET?

A) The code is written and maintained by a professional project manager.

B*) The runtime (CLR) handles memory management and provides a layer of security.

C) The code can only be executed if the user has Administrator privileges.

D) I do not know.

Category 11: Archives & Terminal

Q11: Why is it often impossible to run a complex application directly from inside a .zip file without extracting it first?

A*) The app needs to write temporary files or load DLLs from the relative path on the real disk.

B) The .zip format encrypts the executable so the CPU cannot read the instructions.

C) Windows prevents running files from "Red" colored folders for security reasons.

D) I do not know.

Category 12: Shells & Kernels

Q12: Which statement best describes the relationship between a Terminal (like CMD) and the OS Kernel?

A) The Terminal is the core part of the Kernel that controls the hardware directly.

B) The Terminal is a hardware-based chip that translates keyboard input into code.

C*) The Terminal is a user-mode app that sends requests (system calls) to the Kernel.

D) I do not know.

Category 13: Toolchains & Deployment

Q13: When you "Publish" a .NET app as "Self-Contained," what is included in the output folder?

A) Only the source code files so the user can compile them on their own.

B*) The executable plus all the necessary .NET runtime libraries to run on a clean PC.

C) A link to the Microsoft website where the user must download the runtime.

D) I do not know.