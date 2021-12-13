# Abstractive Text Summarizer
## How to install ##
Steps : 
  1. Clone repository.
  2. Install dependencies using ```pip install -r requirements.txt```
  3. Run app.py using ```python app.py```

## Problem Overview : Extractive vs Abstractive Summarization
**Extraction-based Summarization:** <br>
The extractive approach involves picking up the most important phrases and lines from the documents. It then combines all the important lines to create the summary. So, in this case, every line and word of the summary actually belongs to the original document which is summarized. Extractive summaries can often be inconsistent grammatically, as sentences are stitched together haphazardly.

**Abstraction-based Summarization:** <br>
The abstractive approach involves summarization based on deep learning. So, it uses new phrases and terms, different from the actual document, while keeping the points the same, just like how we actually summarize. This results in a natural, grammatically accurate summary. This makes it much harder than the extractive approach. 

## Approach : Introducing Transformer Nueral Networks.
Text summarization is a complex NLP task which requires the model to retain the *context* of each word in the original article. <br> <br>
👉 The most simple way of achieving this is by using *Recurrent Neural Networks*. RNN's are a type of Neural Network where the output from the previous step is fed as input to the current step.
<p align="center">
  <img src="https://miro.medium.com/max/627/1*go8PHsPNbbV6qRiwpUQ5BQ.png" alt="RNN - Diagram"/>
</p>
But Recurrent Neural Networks suffer from short-term memory (read <a href="https://en.wikipedia.org/wiki/Vanishing_gradient_problem">Vanishing & Exploding gradient problem</a>). If a sequence is long enough, they’ll have a hard time carrying information from earlier time steps to later ones. This can be problematic while summarizing any news article.
<br>
<br>
👉 An improvement over RNN's are <b>LSTM and GRU</b>. LSTM ’s and GRU’s were created as the solution to short-term memory. They have internal mechanisms called gates that can regulate the flow of information.
<br>
<br>
<p align="center">
  <img src="https://user-images.githubusercontent.com/15166794/39033683-3020ce04-44ae-11e8-821f-1a9652ff5025.png" alt="LSTM - Diagram"/>
</p>
The problem with LSTM’s, is that they tend to have poor memory recall with data they’ve seen many time-steps ago, moreover these models are computationally intensive and their sequential nature prevents us from taking advantage of parallel computing.
<br>
<br>
👉 <b>Transformers based on Self-Attention </b> was first introduced in the  <a href="https://arxiv.org/abs/1706.03762"> Attention Is All You Need </a> paper by Ashish Vaswani et al. In simple words it self-attention is a mechanism that allows each input in a sequence to look at the whole sequence to compute a representation of the sequence.
<br>
<br>
<p align="center">
  <img src="https://jalammar.github.io/images/t/transformer_self-attention_visualization_3.png" alt="Self Attention - Diagram"/>
</p>
<p align="center"> Calculating Self Attention for "it" </p>
<br>

This is implemented using a Transformer. A transformer consists of an <b>Encoder and a Decoder</b>. In simple terms, the encoder is responsible for calculating the self-attention and positional encoding. The decoder uses the output of the Encoder and the Outputs (shifted right) to generate the summary. Both Encoder and Decoder are composed of modules that can be stacked on top of each other multiple times.
    <p align="center">
      <img src="https://jalammar.github.io/images/t/The_transformer_encoders_decoders.png" alt="Transformers - Diagram" style= "width : 40%"/>
    </p>
    <p align="center">Transformer Architecture</p>
</div>
<br>
Transformers solve both the disadvantages of LSTM. They can recall data they've seen from anywhere in the input article, and we can also use parallel computing in many stages.

<h2> Implementation </h2>
<br>
👉 For the Model, we will use Transfer Learning with a NLP transformer - “bart-base” and train it on InShorts and CNN-DailyMail dataset. <br> <br>
    <p align="center">
      <img src="https://user-images.githubusercontent.com/57984703/145615462-05f6717f-8da6-4801-a84c-bc90512b3a98.JPG" alt="Workflow - Diagram" style = "width : 50%"/>
    </p>
    <p align="center"> Workflow </p>
<br>
👉 For the UI, we have used the Flask framework to connect our model with the front-end. We have used AJAX to enable server-client communications.
