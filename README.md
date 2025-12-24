VOICE AGENT CREATED USING THE SANDWICH APPROACH

This voice agent is divided into three parts:

1. SPEECH-TO-TEXT
   Assembly AI's API was used to capture streaming audio(audio in real-time and transcribe to text).
   
2. AGENT
   The transcribed text was sent to a langchain agent that makes use of OpenAI's gpt-4.1-mini model which does the reasoning and produces a text output.

3. TEXT-TO-SPEECH
   The text output gotten from the agent is sent to Cartesian's AI to convert the text to speech.

   This voice agent takes food orders from a customer.

   
   
