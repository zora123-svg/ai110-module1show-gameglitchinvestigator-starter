# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

The first bug I identified is that the "New Game" button does not work. The second bug is 
that the generated number is not constrained between 1 and 100, and the logic that 
indicates whether a guess is too low or too high is incorrect. Additionally, the game ends 
prematurely before the last attempt is reached and reveals the secret number. Finally, there may be an issue with the difficulty settings, specifically regarding number ranges and the number of attempts allowed.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude for this project. One example when a AI sugesstion was right is when it fixed the new game button by adding the session status state to playing in the new_game function. I verified that it was correct by going to my app and hitting the new game button to see if i worked. A time when I was incorrect is when I prompt it to fix the errpr where the game ends before the attempts reaches zero. It changed one line of code and then I went to my app and I was wondering why the error still remained. After watching closely I found out that the first wrong attempt will not decrement the attempts left. So I speffically asked claude to target this and it did and I fixed the error.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
---
For the new game button error in order to verify if the bug was fixed I manualy went into my app and clicked on the button in various settings and degrees to make sure that each time a click it will reset the game.

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire script from top to bottom on every user interaction — every keypress, button click, or widget change. Without st.session_state, a plain variable like secret = random.randint(low, high) would be re-evaluated on each rerun, generating a brand new random number every time the user typed or clicked anything. A session.state is the state of an application and based on that state it will act a cetain way. The way I changed it was to make the random.randint() run only once.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One key takeaway from this project is the importance of thinking concisely before engaging with AI. This means having a clear understanding of the problem before prompting — knowing 
exactly what needs to be done reduces back-and-forth and avoids the need for excessive follow-up prompts to arrive at the correct result. One thing I would do differently is to be more specific and deliberate with my prompts from the start.

Prior to this project, I had never used AI to generate code, but I now see its value as a collaborative tool. When used effectively, AI can serve as a teammate to help refactor code, 
assist with testing, and overall improve the efficiency of a project's development lifecycle.
