# Emotion-based Chatbot with Music Recommendation

This project is a chatbot demo for Music-Bot that can sense user emotions and generate responses that are aligned with the user's mood. It also uses the Last.fm API to suggest songs that match the user's feelings and display them along with the chat history. This project is built on a HuggingFace Transformers backend that performs the emotion recognition and dialogue generation.

## How it works

The chatbot uses two state-of-the-art models from Hugging Face: mrm8488/t5-base-finetuned-emotion and microsoft/GODEL-v1_1-large-seq2seq. The former is a T5 model fine-tuned for emotion recognition, and the latter is a Seq2Seq model fine-tuned for open-domain dialogue generation. The chatbot first uses the T5 model to classify the user input into one of six emotions: joy, sadness, anger, fear, surprise, or neutral. Then, the Seq2Seq model is used to generate a response based on the emotion and the context of the conversation. Finally, Last.fm API is called to fetch the top songs for the detected emotion and display them in the UI.

![alt text](<Capture d’écran 2024-03-21 122332.png>)
