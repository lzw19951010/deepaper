# deepaper demo - run with: vhs demo.tape
Output demo.gif

Set Shell "bash"
Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Catppuccin Mocha"
Set Padding 15
Set TypingSpeed 40ms

# 1. Show what deepaper does
Type "deepaper --help"
Enter
Sleep 3s

# 2. Init a new project (in temp dir)
Type "cd $(mktemp -d) && deepaper init"
Enter
Sleep 3s

# 3. Citation lookup - the killer feature (real API call)
Type "deepaper cite 1706.03762  # Attention Is All You Need"
Enter
Sleep 18s

# 4. Show an existing analyzed paper
Type "head -50 /Users/bytedance/github/paper-manager/papers/llm/pretraining/scaling-laws-for-neural-language-models.md"
Enter
Sleep 5s

Sleep 2s
