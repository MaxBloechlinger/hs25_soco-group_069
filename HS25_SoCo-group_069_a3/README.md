## mkfs method:

- creates new filesystem, populates header, fills out file entries with 0s for 32 entries and includes values for header metadata

**Max Prompts**:

- "please explain what they exactly want from us give a few steps to stategically conquer this complex task"
- "put the steps in a pdf i can share with the team"
- "the file structure graph is confusing me, is this supposed to be a single file or is the graph showing the system?"
- "so it means there's 32 entries with 64 bytes each to describe the file? whats the header for then"
- "but whats the exact structure the graph is so unclear. explain like im an idiot"
- "https://docs.python.org/3/library/struct.html explain to me briefly what struct does in context to the zvfs asg i shared"
- "which format chars can i choose for file offset and why?"
- "what are the next steps tell me socratically)"
- "how can we store the fs in the most simple way, please no classes"
- "what does seek() do"

**Abraham Prompts**:

"What are some good api documentations for this project?"
"Can you summarize this: https://docs.python.org/3/library/io.html"
"Can you summarise this: https://docs.python.org/3/library/struct.html"
"Summarise and explain thuroughly this chapter of the source material: **Chapter 17, Software design by example**
"Explain the difference between rb and r"
"Explaint the format my friend used and explain it: **pasted a snipped of the code**
